from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


def test_site_files_exist():
    for filename in ["index.html", "styles.css", "buyers.html", "suppliers.html", "vision.html", "demo/index.html", "yc-demo/index.html", "app/index.html"]:
        assert (ROOT / filename).exists(), filename


def test_home_page_is_artifact_led_request_desk():
    html = read("index.html")
    for phrase in [
        "SupplierProof",
        "Send the messy customer request",
        "review-ready packet",
        "embedded request desk",
        "What you send",
        "What we handle",
        "What you get back",
        "Send a redacted request",
        "Nothing is sent without your approval",
        "Redacted files are welcome",
    ]:
        assert phrase in html


def test_home_page_shows_service_labor_not_just_ui():
    html = read("index.html")
    for phrase in [
        "SupplierProof activity",
        "Parsed retailer request",
        "Asked finance for facility utility bills",
        "Supplier declaration requested",
        "Unsupported claim flagged",
        "Draft response ready for approval",
        "We chase the missing evidence",
        "You approve the final package",
    ]:
        assert phrase in html


def test_home_page_names_concrete_food_packaging_workflows():
    html = read("index.html")
    for phrase in [
        "CDP",
        "Walmart Gigaton",
        "EcoVadis",
        "packaging claims",
        "Food safety certificate",
        "Palm or fiber sourcing proof",
        "Packaging recycled content",
        "GFSI / SQF / BRCGS certificate",
        "RSPO / FSC certificate or supplier declaration",
        "Packaging spec and supplier proof",
    ]:
        assert phrase in html


def test_home_page_avoids_stale_or_jargony_positioning():
    html = read("index.html")
    forbidden = [
        "buyer-sponsored",
        "AI-native",
        "evidence operations",
        "evidence pack",
        "gap map",
        "Scope 3 platform",
        "For investors",
        "See investor page",
        "vision.html",
    ]
    for phrase in forbidden:
        assert phrase not in html


def test_pages_have_seo_and_shared_styles():
    for filename in ["index.html", "buyers.html", "suppliers.html", "vision.html", "demo/index.html", "yc-demo/index.html"]:
        html = read(filename)
        assert "meta name=\"description\"" in html
        assert "meta name=\"viewport\"" in html
        assert "styles.css" in html


def test_styles_define_new_case_file_visual_system():
    css = read("styles.css")
    for token in [
        "linear-gradient",
        "box-shadow",
        "@media",
        "--lemon: #e7ff4f",
        "--deep-green: #0f3d2a",
        ".case-board",
        ".paper-email",
        ".activity-log",
        ".package-preview",
        ".operator-note",
        ".handoff-strip",
        ".boundary-grid",
    ]:
        assert token in css


def test_demo_is_a_case_file_not_a_product_tour():
    html = read("demo/index.html")
    for phrase in [
        "../styles.css",
        "site-shell demo-shell",
        "brand-mark",
        "Public demo, private proof in real pilots",
        "Case file",
        "Forwarded request",
        "SupplierProof working log",
        "Approval packet",
        "What happens when proof is missing",
        "Ready for review",
        "customer request desk",
    ]:
        assert phrase in html
    assert "not the product; it is the control center" not in html
    assert "View public-artifact demo" not in html


def test_customer_demo_is_scrollable_three_step_walkthrough():
    html = read("demo/index.html")
    css = read("styles.css")
    for phrase in [
        "demo-step-nav",
        "Step 1",
        "Step 2",
        "Step 3",
        "id=\"step-1\"",
        "id=\"step-2\"",
        "id=\"step-3\"",
        "Step 1: Send us the customer request",
        "Step 2: We work the evidence desk",
        "Step 3: You approve the response package",
        "What you scroll through",
        "sticky-step-rail",
    ]:
        assert phrase in html
    for token in [
        ".walkthrough-step",
        ".step-number",
        ".sticky-step-rail",
        ".demo-step-nav",
    ]:
        assert token in css


def test_yc_demo_shows_service_to_agent_loop():
    html = read("yc-demo/index.html")
    for phrase in [
        "SupplierProof Evidence Agent",
        "Service now. Agent over time.",
        "Walmart THESIS detected",
        "scanned Gmail, Drive, and NetSuite",
        "Current readiness 42/100",
        "After priority gaps 78/100",
        "Evidence memory created",
        "CDP reuse",
        "EcoVadis reuse",
        "human approval required",
        "AI-native service company",
        "company brain for supplier evidence",
    ]:
        assert phrase in html


def test_yc_demo_has_mock_interactive_dashboard_components():
    html = read("yc-demo/index.html")
    css = read("styles.css")
    for phrase in [
        "agent-dashboard",
        "request-card active",
        "scan-console",
        "readiness-panel",
        "evidence-memory-grid",
        "agent-action-queue",
        "framework-reuse-strip",
    ]:
        assert phrase in html or phrase in css
    for token in [
        ".agent-dashboard",
        ".scan-console",
        ".readiness-meter",
        ".memory-card",
        ".reuse-pill",
    ]:
        assert token in css


def test_yc_demo_is_clickable_not_only_static_page():
    html = read("yc-demo/index.html")
    css = read("styles.css")
    for phrase in [
        "data-request=\"walmart\"",
        "data-request=\"cdp\"",
        "data-request=\"ecovadis\"",
        "data-kpi=\"energy\"",
        "data-kpi=\"packaging\"",
        "data-action=\"approve\"",
        "data-action=\"replay-scan\"",
        "demoState",
        "renderRequest",
        "renderKpiDetail",
        "addEventListener",
    ]:
        assert phrase in html
    for token in [
        ".kpi-row.is-selected",
        ".demo-toast",
        ".approval-preview",
        ".clicked-hint",
    ]:
        assert token in css


def test_yc_demo_separates_dashboard_state_from_transcript_copy():
    html = read("yc-demo/index.html")
    css = read("styles.css")
    for phrase in [
        "demoTranscript",
        "data-caption-key",
        "data-field=\"status\"",
        "data-field=\"owner\"",
        "data-field=\"due\"",
        "data-field=\"next\"",
        "data-step-state=\"hidden\"",
        "data-step-state=\"visible\"",
    ]:
        assert phrase in html
    for terse_state in ["Detected", "Matched", "Reused", "Blocked", "Drafted"]:
        assert terse_state in html
    for verbose_dashboard_copy in [
        "SupplierProof starts as a managed evidence desk",
        "We sell the outcome first",
        "Click other KPI rows to show the source evidence",
        "Walmart THESIS email detected in Gmail",
        "Agent loaded prior THESIS evidence objects",
        "This is the product vision, grounded in the service wedge",
    ]:
        assert verbose_dashboard_copy not in html
    for token in [
        ".transcript-only",
        ".step-hidden",
        ".field-grid",
        ".dashboard-drawer",
        ".yc-app-body .memory-section",
    ]:
        assert token in css


def test_app_request_page_is_clean_upload_workspace():
    html = read("app/index.html")
    css = read("styles.css")
    for phrase in [
        "SupplierProof",
        "Company",
        "Acme Corporation",
        "Company details",
        "Questionnaire",
        "Acme’s Walmart THESIS questionnaire",
        "Walmart THESIS Sustainability Assessment",
        "Upload questionnaire",
        "Documents",
        "Upload documents",
        "Metadata file",
        "Upload metadata file",
        "department owners, supplier contacts, annual production volume, supplier list, reporting year, and preferred follow-up channels",
        "Process questionnaire",
        "data-action=\"toggle-company\"",
        "company-drawer",
    ]:
        assert phrase in html
    assert "Process Acme’s Walmart THESIS questionnaire" not in html
    assert "plain-eyebrow" not in html
    for forbidden in ["YC 60", "AI-native", "orchestrator", "OAuth", "Connectors", "NetSuite", "fixed-fee assessment package"]:
        assert forbidden not in html
    for token in [".clean-app", ".request-layout", ".upload-card", ".company-drawer", ".simple-nav"]:
        assert token in css


def test_app_contains_documents_metadata_and_company_context():
    html = read("app/index.html")
    for phrase in [
        "Walmart THESIS notification email",
        "12-month electricity bill",
        "12-month natural gas bill",
        "Quarterly water bill",
        "Waste hauler annual summary",
        "BRC food safety certificate",
        "Environmental policy",
        "Packaging spec sheet",
        "Past THESIS response",
        "Supplier email thread",
        "Facilities Manager",
        "HR/EHS",
        "Quality Manager",
        "TruPak Packaging Co contact",
        "PT Sawit Indo contact",
        "4,200 metric tons production volume",
        "23 active suppliers",
        "one overwhelmed sustainability owner",
    ]:
        assert phrase in html


def test_app_processing_page_has_plain_agent_trace_and_routing():
    html = read("app/index.html")
    for phrase in [
        "Processing questionnaire",
        "Agent trace",
        "SupplierProof is reading the uploaded files, calculating answers, and finding missing information.",
        "Reading Walmart THESIS questionnaire",
        "Found 14 required items",
        "Reading electricity bill",
        "Found 2,850,000 kWh",
        "Reading natural gas bill",
        "Found 78,000 therms",
        "Reading production data from metadata file",
        "Found 4,200 metric tons FY2024",
        "Calculated from utility bills using EPA emission factors",
        "Scope 2: 1,100 tCO2e",
        "Scope 1 partial: 413 tCO2e",
        "Checking metadata file",
        "Found Facilities Manager contact",
        "Found TruPak Packaging Co contact",
        "Preparing follow-ups",
        "function renderFeedStep",
        "function updateKpiTracker",
        "Answered 9 of 14 questionnaire items",
        "statusRows = kpis.map",
        "progress-card is-waiting",
        "progress-panel",
        "Trace complete — results ready",
        "function revealProgress",
    ]:
        assert phrase in html
    assert "statusRows = [" not in html


def test_app_results_page_has_precise_ghg_method_and_scope_boundary():
    html = read("app/index.html")
    assert "const kpis = [" in html
    assert html.count("kpiId:") == 14
    for phrase in [
        "Results",
        "9 / 14 answered",
        "58 / 100 estimated score",
        "82 / 100 if missing items are resolved",
        "32 / 100 last year",
        "Estimated GHG emissions from available data",
        "Scope 2 (electricity): 1,100 tCO2e",
        "Scope 1 (natural gas): 413 tCO2e",
        "Scope 1 is incomplete — refrigerant data not provided",
        "These estimates use EPA published emission factors and are suitable for THESIS reporting.",
        "For verified carbon accounting or SBTi target-setting, consult a carbon accounting specialist.",
        "Calculated from utility bills using EPA emission factors",
        "2,850,000 kWh × 0.000386 tCO2e/kWh",
        "78,000 therms × 0.005302 tCO2e/therm",
        "This is not a verified GHG inventory, audit, assurance statement, or SBTi target-setting analysis.",
        "All questionnaire items",
        "Question",
        "Answer",
        "Proof",
        "Method",
        "Question: What were Acme’s Scope 1 and Scope 2 GHG emissions for FY2024?",
        "Answer: Scope 2 electricity is 1,100 tCO2e; Scope 1 natural gas is 413 tCO2e; refrigerants are missing.",
        "Proof: 12-month electricity bill, 12-month natural gas bill, and metadata reporting year FY2024.",
        "data-kpi=\"supplier-ghg-reporting\"",
        "results-main-column",
        "scrollIntoView",
    ]:
        assert phrase in html
    assert html.index('class="results-layout"') < html.index('class="plain-card all-items"') < html.index('class="plain-card result-detail"')
    assert "GHG Emissions: 1,513 tCO2e" not in html


def test_app_followups_are_expandable_and_clean():
    html = read("app/index.html")
    for phrase in [
        "Follow-ups",
        "SupplierProof found the missing information needed to complete the questionnaire.",
        "data-action=\"toggle-draft\"",
        "data-action=\"email-now\"",
        "data-action=\"schedule-call\"",
        "impact-badge high",
        "impact-badge medium",
        "Draft email",
        "Request refrigerant records",
        "Acme Facilities Manager",
        "Request packaging recycled content",
        "TruPak Packaging Co",
        "Request RSPO documentation",
        "PT Sawit Indo",
        "Voice follow-up scheduled Day 7",
        "If no response by Day 7, SupplierProof will call using the supplier contact from the metadata file.",
        "What this also helps with",
        "Framework reuse",
        "CDP 45% · EcoVadis 52%",
        "Score lift",
        "Resolving the top 3 missing items could raise the estimate from 58 to 72.",
    ]:
        assert phrase in html
    assert "human approval queue" not in html.lower()
    for token in [".followup-card h2", ".action-row", ".impact-badge.high", ".impact-badge.medium", ".followup-cta"]:
        assert token in read("styles.css")


def test_app_can_be_linked_from_existing_yc_demo():
    html = read("yc-demo/index.html") + read("index.html")
    assert "app/index.html" in html
    assert "Ops console" in html or "full app" in html
