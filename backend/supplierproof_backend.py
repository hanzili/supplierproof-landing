from __future__ import annotations

import csv
import hashlib
import io
import json
import mimetypes
import re
import shutil
import uuid
import zipfile
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree

try:
    from fastapi import FastAPI, File, Form, HTTPException, UploadFile
    from fastapi.middleware.cors import CORSMiddleware
except Exception:  # pragma: no cover - lets storage/parser helpers run without API deps
    FastAPI = None

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STORAGE_ROOT = REPO_ROOT / "storage"
SAFE_SEGMENT = re.compile(r"[^a-zA-Z0-9._-]+")
ALLOWED_UPLOAD_EXTENSIONS = {
    ".pdf", ".xlsx", ".xls", ".csv", ".docx", ".txt", ".md", ".json", ".yaml", ".yml",
    ".eml", ".mbox", ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".zip",
}
UPLOAD_BUCKETS = {"questionnaires", "documents", "metadata"}


@dataclass(frozen=True)
class RequestCase:
    tenant_id: str
    request_id: str
    company_name: str
    industry: str
    framework: str
    created_at: str
    storage_prefix: str


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_segment(value: str, fallback: str = "item") -> str:
    cleaned = SAFE_SEGMENT.sub("-", (value or "").strip()).strip("._-").lower()
    return cleaned[:80] or fallback


def safe_filename(filename: str) -> str:
    name = Path(filename or "upload.bin").name.replace("\x00", "")
    stem = safe_segment(Path(name).stem, "upload")
    suffix = Path(name).suffix.lower()
    if suffix not in ALLOWED_UPLOAD_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {suffix or 'none'}")
    return f"{stem}{suffix}"


def request_root(storage_root: Path, tenant_id: str, request_id: str) -> Path:
    tenant = safe_segment(tenant_id, "demo")
    request = safe_segment(request_id, "request")
    return storage_root / "tenants" / tenant / "requests" / request


def create_request_case(
    *,
    company_name: str,
    industry: str,
    framework: str,
    tenant_id: str = "demo",
    storage_root: Path = DEFAULT_STORAGE_ROOT,
) -> RequestCase:
    tenant = safe_segment(tenant_id, "demo")
    request_id = f"req_{uuid.uuid4().hex[:12]}"
    root = request_root(storage_root, tenant, request_id)
    for relative in [
        "raw/questionnaires",
        "raw/documents",
        "raw/metadata",
        "parsed/text",
        "parsed/tables",
        "runs",
        "packet",
    ]:
        (root / relative).mkdir(parents=True, exist_ok=True)
    case = RequestCase(
        tenant_id=tenant,
        request_id=request_id,
        company_name=company_name.strip(),
        industry=industry,
        framework=framework,
        created_at=utc_now(),
        storage_prefix=f"tenants/{tenant}/requests/{request_id}/",
    )
    write_json(root / "request.json", asdict(case))
    write_json(root / "manifest.json", build_manifest(case))
    return case


def build_manifest(case: RequestCase) -> dict:
    return {
        "tenant_id": case.tenant_id,
        "request_id": case.request_id,
        "company_snapshot": {"name": case.company_name},
        "industry": case.industry,
        "framework": case.framework,
        "questionnaire_files": [],
        "document_files": [],
        "metadata_files": [],
        "allowed_storage_prefix": case.storage_prefix,
    }


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def assert_request_scoped(storage_root: Path, tenant_id: str, request_id: str, path: Path) -> None:
    root = request_root(storage_root, tenant_id, request_id).resolve()
    target = path.resolve()
    if root != target and root not in target.parents:
        raise ValueError("Path escaped request storage scope")


def save_upload_stream(
    *,
    stream,
    filename: str,
    tenant_id: str,
    request_id: str,
    bucket: str,
    storage_root: Path = DEFAULT_STORAGE_ROOT,
) -> dict:
    if bucket not in UPLOAD_BUCKETS:
        raise ValueError(f"Unknown upload bucket: {bucket}")
    safe_name = safe_filename(filename)
    root = request_root(storage_root, tenant_id, request_id)
    destination_dir = root / "raw" / bucket
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / f"{uuid.uuid4().hex[:8]}-{safe_name}"
    assert_request_scoped(storage_root, tenant_id, request_id, destination)
    with destination.open("wb") as out:
        shutil.copyfileobj(stream, out)
    parsed = parse_file_to_text(destination)
    parsed_path = root / "parsed" / "text" / f"{destination.stem}.txt"
    parsed_path.write_text(parsed["text"], encoding="utf-8")
    result = {
        "filename": safe_name,
        "stored_path": str(destination.relative_to(storage_root)),
        "parsed_text_path": str(parsed_path.relative_to(storage_root)),
        "mime_type": mimetypes.guess_type(destination.name)[0] or "application/octet-stream",
        "size_bytes": destination.stat().st_size,
        "sha256": sha256_file(destination),
        "parser": parsed["parser"],
        "text_preview": parsed["text"][:600],
    }
    if bucket == "questionnaires":
        result["questionnaire_analysis"] = extract_questionnaire_requirements(parsed["text"])
    append_manifest_upload(storage_root, tenant_id, request_id, bucket, result)
    return result


def parse_file_to_text(path: Path) -> dict:
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md", ".csv", ".json", ".yaml", ".yml", ".eml", ".mbox"}:
        text = path.read_text(encoding="utf-8", errors="replace")
        if suffix == ".csv":
            text = csv_to_markdown(text)
        elif suffix == ".json":
            try:
                text = json.dumps(json.loads(text), indent=2, sort_keys=True)
            except json.JSONDecodeError:
                pass
        return {"parser": f"text/{suffix.lstrip('.')}", "text": text}
    if suffix == ".docx":
        return {"parser": "docx/zip-xml", "text": docx_to_text(path)}
    if suffix == ".xlsx":
        return {"parser": "xlsx/zip-xml", "text": xlsx_to_text(path)}
    if suffix == ".pdf":
        return {"parser": "pdf-placeholder", "text": "PDF uploaded and stored. Text extraction will use pypdf or OCR in the production parser."}
    if suffix in {".png", ".jpg", ".jpeg", ".tif", ".tiff"}:
        return {"parser": "image-placeholder", "text": "Image uploaded and stored. OCR is queued for the production parser."}
    if suffix == ".zip":
        names = []
        with zipfile.ZipFile(path) as zf:
            names = zf.namelist()[:200]
        return {"parser": "zip-manifest", "text": "ZIP uploaded with files:\n" + "\n".join(names)}
    return {"parser": "unknown", "text": "File uploaded and stored; parser not available yet."}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def append_manifest_upload(storage_root: Path, tenant_id: str, request_id: str, bucket: str, upload: dict) -> None:
    root = request_root(storage_root, tenant_id, request_id)
    manifest_path = root / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    key = {"questionnaires": "questionnaire_files", "documents": "document_files", "metadata": "metadata_files"}[bucket]
    manifest.setdefault(key, []).append(upload)
    write_json(manifest_path, manifest)


def extract_questionnaire_requirements(text: str) -> dict:
    compact = re.sub(r"\s+", " ", text or " ").strip()
    lines = [line.strip(" |\t-") for line in (text or "").splitlines() if line.strip(" |\t-")]
    question_markers = [line for line in lines if re.search(r"(^question\b|^q\d+\b|^\d+[.)]|\?)", line, re.I)]
    evidence_lines = [line for line in lines if re.search(r"attach|provide|upload|certificate|emissions?|declaration|records?|report|policy|audit", line, re.I)]
    question_count = max(len(question_markers), len(evidence_lines)) or min(len(lines), 1 if compact else 0)
    rules = [
        ("iso-14001-certificate", "ISO 14001 certificate", r"iso\s*14001"),
        ("iatf-16949-certificate", "IATF 16949 certificate", r"iatf\s*16949"),
        ("scope-emissions-workbook", "Scope 1/2 emissions workbook", r"scope\s*[12]|emissions?|ghg|greenhouse"),
        ("energy-bills", "Energy bills / utility records", r"energy|electricity|natural\s+gas|utility"),
        ("water-records", "Water bills or withdrawal records", r"water"),
        ("waste-records", "Waste hauler or diversion records", r"waste|landfill|recycl"),
        ("material-recycled-content", "Material / recycled-content declarations", r"recycled\s+content|material\s+declaration|pcr"),
        ("supplier-code-policy", "Supplier code / policy evidence", r"supplier\s+code|policy|human\s+rights|ethics"),
        ("audit-report", "Audit report or corrective-action plan", r"audit|corrective\s+action|cap"),
        ("safety-records", "Worker safety records", r"safety|osha|trir|incident"),
        ("food-safety-certificate", "Food safety certificate", r"brc|sqf|food\s+safety"),
        ("cmrt-emrt-template", "CMRT / EMRT minerals template", r"cmrt|emrt|conflict\s+minerals?|cobalt|mica|smelter"),
        ("epd-hpd-document", "EPD / HPD product transparency document", r"\bepd\b|\bhpd\b|environmental\s+product\s+declaration"),
    ]
    requirements = []
    for req_id, title, pattern in rules:
        if re.search(pattern, compact, re.I):
            requirements.append({"id": f"parsed-{req_id}", "title": title, "source": "Parsed from uploaded questionnaire"})
    if compact and not requirements:
        requirements.append({"id": "parsed-questionnaire-specific-evidence", "title": "Questionnaire-specific evidence named in upload", "source": "Parsed from uploaded questionnaire"})
    return {
        "question_count": question_count,
        "requirements": requirements,
        "preview": compact[:800],
    }


def csv_to_markdown(text: str) -> str:
    rows = list(csv.reader(io.StringIO(text)))
    if not rows:
        return ""
    header, body = rows[0], rows[1:50]
    out = ["| " + " | ".join(header) + " |", "| " + " | ".join(["---"] * len(header)) + " |"]
    out.extend("| " + " | ".join(row) + " |" for row in body)
    return "\n".join(out)


def docx_to_text(path: Path) -> str:
    with zipfile.ZipFile(path) as zf:
        xml = zf.read("word/document.xml")
    root = ElementTree.fromstring(xml)
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    paragraphs = []
    for para in root.iter(f"{ns}p"):
        words = [node.text or "" for node in para.iter(f"{ns}t")]
        if words:
            paragraphs.append("".join(words))
    return "\n".join(paragraphs)


def xlsx_to_text(path: Path) -> str:
    # Lightweight shared-string extraction for prototype. Full table parsing can use openpyxl later.
    with zipfile.ZipFile(path) as zf:
        shared = []
        if "xl/sharedStrings.xml" in zf.namelist():
            root = ElementTree.fromstring(zf.read("xl/sharedStrings.xml"))
            ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
            for si in root.iter(f"{ns}si"):
                shared.append("".join(t.text or "" for t in si.iter(f"{ns}t")))
        sheets = [name for name in zf.namelist() if name.startswith("xl/worksheets/sheet") and name.endswith(".xml")]
        lines = []
        ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
        for sheet in sheets[:5]:
            root = ElementTree.fromstring(zf.read(sheet))
            lines.append(f"# {sheet}")
            for row in root.iter(f"{ns}row"):
                values = []
                for cell in row.iter(f"{ns}c"):
                    value = cell.find(f"{ns}v")
                    if value is None or value.text is None:
                        continue
                    if cell.attrib.get("t") == "s" and value.text.isdigit() and int(value.text) < len(shared):
                        values.append(shared[int(value.text)])
                    else:
                        values.append(value.text)
                if values:
                    lines.append(" | ".join(values))
        return "\n".join(lines)


def enrich_company_snapshot(company_name: str, industry: str, framework: str) -> dict:
    return {
        "name": company_name.strip(),
        "industry": industry,
        "likely_frameworks": [framework],
        "confidence": "prototype",
        "sources": ["user input", "industry/framework catalog"],
        "note": "Backend placeholder. Wire to web/company-data APIs in the next production pass.",
    }


if FastAPI is not None:
    app = FastAPI(title="SupplierProof Prototype Backend")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:8000", "http://127.0.0.1:8000",
            "http://localhost:8005", "http://127.0.0.1:8005",
            "https://hanzili.github.io", "null",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health() -> dict:
        return {"ok": True, "storage_root": str(DEFAULT_STORAGE_ROOT)}

    @app.post("/requests")
    def create_request(company_name: str = Form(...), industry: str = Form(...), framework: str = Form(...), tenant_id: str = Form("demo")) -> dict:
        case = create_request_case(company_name=company_name, industry=industry, framework=framework, tenant_id=tenant_id)
        return {"request": asdict(case), "manifest": build_manifest(case)}

    @app.post("/requests/{tenant_id}/{request_id}/uploads/{bucket}")
    async def upload_file(tenant_id: str, request_id: str, bucket: str, file: UploadFile = File(...)) -> dict:
        if not request_root(DEFAULT_STORAGE_ROOT, tenant_id, request_id).exists():
            raise HTTPException(status_code=404, detail="Request not found")
        try:
            return save_upload_stream(stream=file.file, filename=file.filename or "upload.bin", tenant_id=tenant_id, request_id=request_id, bucket=bucket)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/enrich")
    def enrich(company_name: str, industry: str, framework: str) -> dict:
        return enrich_company_snapshot(company_name, industry, framework)
