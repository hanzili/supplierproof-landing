import io
import json
from pathlib import Path

from backend.supplierproof_backend import (
    create_request_case,
    extract_questionnaire_requirements,
    parse_file_to_text,
    request_root,
    safe_filename,
    save_upload_stream,
)


def test_create_request_case_creates_request_scoped_folders(tmp_path):
    case = create_request_case(
        company_name="Acme Corporation",
        industry="food_packaging",
        framework="walmart_thesis",
        tenant_id="Demo Org",
        storage_root=tmp_path,
    )
    root = request_root(tmp_path, case.tenant_id, case.request_id)
    assert case.tenant_id == "demo-org"
    assert (root / "raw/questionnaires").is_dir()
    assert (root / "raw/documents").is_dir()
    assert (root / "raw/metadata").is_dir()
    manifest = json.loads((root / "manifest.json").read_text())
    assert manifest["allowed_storage_prefix"].startswith("tenants/demo-org/requests/req_")


def test_safe_filename_allowlist_and_sanitization():
    assert safe_filename("../../Questionnaire FINAL.xlsx") == "questionnaire-final.xlsx"
    try:
        safe_filename("evil.html")
    except ValueError as exc:
        assert "Unsupported" in str(exc)
    else:
        raise AssertionError("html upload should be blocked")


def test_save_upload_stream_parses_text_and_stays_in_request_scope(tmp_path):
    case = create_request_case(
        company_name="Acme Corporation",
        industry="food_packaging",
        framework="walmart_thesis",
        storage_root=tmp_path,
    )
    saved = save_upload_stream(
        stream=io.BytesIO(b"question,answer\nScope 1 emissions,123"),
        filename="questionnaire.csv",
        tenant_id=case.tenant_id,
        request_id=case.request_id,
        bucket="questionnaires",
        storage_root=tmp_path,
    )
    assert saved["stored_path"].startswith(f"tenants/{case.tenant_id}/requests/{case.request_id}/raw/questionnaires/")
    assert saved["parser"] == "text/csv"
    assert "Scope 1 emissions" in saved["text_preview"]
    assert (tmp_path / saved["parsed_text_path"]).exists()


def test_parse_json_file_pretty_prints(tmp_path):
    path = tmp_path / "meta.json"
    path.write_text('{"owner":"Maya","year":2026}', encoding="utf-8")
    parsed = parse_file_to_text(path)
    assert parsed["parser"] == "text/json"
    assert '"owner": "Maya"' in parsed["text"]


def test_extract_questionnaire_requirements_from_parsed_questions():
    analysis = extract_questionnaire_requirements(
        """
        Question: Provide current ISO 14001 certificate.
        2. Attach IATF 16949 certification and latest audit report.
        3. Upload Scope 1 and Scope 2 emissions workbook with energy bills.
        4. Do you have recycled content material declarations?
        """
    )
    titles = [item["title"] for item in analysis["requirements"]]
    assert analysis["question_count"] == 4
    assert "ISO 14001 certificate" in titles
    assert "IATF 16949 certificate" in titles
    assert "Scope 1/2 emissions workbook" in titles
    assert "Material / recycled-content declarations" in titles


def test_questionnaire_upload_returns_analysis_and_updates_manifest(tmp_path):
    case = create_request_case(
        company_name="Tesla Supplier",
        industry="automotive_industrial",
        framework="drive_sustainability_saq",
        storage_root=tmp_path,
    )
    saved = save_upload_stream(
        stream=io.BytesIO(b"question\nAttach ISO 14001 certificate\nProvide IATF 16949 certificate"),
        filename="saq.csv",
        tenant_id=case.tenant_id,
        request_id=case.request_id,
        bucket="questionnaires",
        storage_root=tmp_path,
    )
    assert saved["questionnaire_analysis"]["question_count"] >= 2
    assert any(req["title"] == "ISO 14001 certificate" for req in saved["questionnaire_analysis"]["requirements"])
    manifest = json.loads((request_root(tmp_path, case.tenant_id, case.request_id) / "manifest.json").read_text())
    assert manifest["questionnaire_files"][0]["filename"] == "saq.csv"
    assert manifest["questionnaire_files"][0]["questionnaire_analysis"]["requirements"]
