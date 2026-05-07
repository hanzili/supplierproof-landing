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


def test_document_requirements_change_by_industry_and_framework():
    assert 'id="document-requirement-list"' in HTML
    assert 'const documentRequirementCatalog' in HTML
    assert 'function currentDocumentRequirements' in HTML
    assert 'function renderDocumentRequirements' in HTML
    assert "documentRequirementCatalog[`${industry.id}:${framework.id}`]" in HTML
    assert 'data-requirement-id' in HTML
    for evidence in [
        "Drive Sustainability SAQ response export",
        "ISO 14001 certificate",
        "IATF 16949 certificate",
        "CMRT / EMRT minerals template",
        "Walmart THESIS notification email",
        "BRC or SQF food safety certificate",
        "Packaging recycled-content declaration",
        "EPD / HPD product transparency document",
    ]:
        assert evidence in HTML


def test_uploaded_custom_questionnaire_adds_questionnaire_specific_requirement():
    assert 'inferQuestionnaireRequirements' in HTML
    assert 'Custom uploaded questionnaire' in HTML
    assert 'Uploaded questionnaire sections / screenshots' in HTML
    assert 'Questionnaire-specific evidence named in upload' in HTML
    assert 'renderDocumentRequirements();' in HTML


def test_frontend_has_questionnaire_parsing_api_pipeline():
    assert 'const API_BASE_URL' in HTML
    assert 'async function ensureBackendRequest' in HTML
    assert 'async function uploadQuestionnaireForParsing' in HTML
    assert 'applyParsedQuestionnaireRequirements' in HTML
    assert 'questionnaireParseStatus' in HTML
    assert 'fetchWithTimeout(`${API_BASE_URL}/requests`' in HTML
    assert 'uploads/questionnaires' in HTML
    assert 'parsedQuestionnaireRequirements' in HTML
    assert 'Parsed from uploaded questionnaire' in HTML
    assert 'AbortController' in HTML
    assert 'Parsing timed out' in HTML
