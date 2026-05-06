from pathlib import Path

APP = Path(__file__).resolve().parents[1] / "app" / "index.html"
HTML = APP.read_text(encoding="utf-8")


def test_industry_selector_and_catalog_exist():
    assert 'id="industry-select"' in HTML
    assert 'const industryCatalog' in HTML
    for industry in [
        "food_packaging",
        "mining_metals",
        "oil_gas_chemicals",
        "apparel_textiles",
        "electronics_batteries",
        "automotive_industrial",
        "construction_materials",
    ]:
        assert industry in HTML
    for framework in [
        "Walmart THESIS",
        "Project Gigaton",
        "IRMA",
        "TSM",
        "Copper Mark",
        "Higg FEM",
        "RBA",
        "Drive Sustainability SAQ",
        "LEED documentation",
    ]:
        assert framework in HTML


def test_upload_inputs_support_expected_file_formats_and_visible_lists():
    assert 'id="questionnaire-file-list"' in HTML
    assert 'id="document-file-list"' in HTML
    assert 'id="metadata-file-list"' in HTML
    assert 'renderFileList' in HTML
    assert 'formatFileSize' in HTML
    for extension in [
        ".pdf",
        ".xlsx",
        ".xls",
        ".csv",
        ".docx",
        ".txt",
        ".md",
        ".eml",
        ".mbox",
        ".png",
        ".jpg",
        ".jpeg",
        ".tiff",
        ".zip",
        ".json",
        ".yaml",
        ".yml",
    ]:
        assert extension in HTML


def test_company_enrichment_updates_drawer_with_structured_fields():
    assert 'const mockCompanyEnrichment' in HTML
    assert 'data-company-field="website"' in HTML
    assert 'data-company-field="industry"' in HTML
    assert 'data-company-field="location"' in HTML
    assert 'data-company-field="confidence"' in HTML
    assert 'id="company-sources"' in HTML
    assert 'updateCompanyDrawer' in HTML
    assert 'enrichment-state' in HTML


def test_process_button_has_intake_validation_hooks():
    assert 'validateIntake' in HTML
    assert 'intake-status' in HTML
    assert 'questionnaireFiles' in HTML
    assert 'metadataFiles' in HTML
    assert 'documentFiles' in HTML
