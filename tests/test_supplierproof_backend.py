import io
import json
from pathlib import Path

from backend.supplierproof_backend import (
    create_request_case,
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
