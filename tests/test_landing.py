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


def test_app_is_yc_acme_thesis_agent_demo_not_connector_dashboard():
    html = read("app/index.html")
    css = read("styles.css")
    for phrase in [
        "SupplierProof YC Demo",
        "Acme Corporation",
        "frozen baked goods manufacturer",
        "Walmart THESIS",
        "due November 15",
        "Process evidence package",
        "internal Hermes-style orchestrator",
        "Human reviews and approves",
        "9 of 14 KPIs answered",
        "58/100",
        "82/100",
        "32/100",
    ]:
        assert phrase in html
    for forbidden in [
        "data-screen=\"connectors\"",
        "Connector setup",
        "Connectors",
        "OAuth",
        "read-only scan",
        "NetSuite",
    ]:
        assert forbidden not in html
    for token in [".yc-demo-app", ".demo-stage", ".agent-feed", ".kpi-tracker", ".score-gauge", ".followup-card"]:
        assert token in css


def test_app_contains_ten_messy_documents_and_internal_data():
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
        "Past THESIS response from last year",
        "Supplier email thread",
        "2,850,000 kWh",
        "78,000 therms",
        "18,200,000 gallons",
        "840 tons total",
        "62% diverted",
        "4,200 metric tons",
        "23 active suppliers",
    ]:
        assert phrase in html


def test_app_has_timed_agent_processing_feed_and_calculations():
    html = read("app/index.html")
    for phrase in [
        "setTimeout",
        "processEvidencePackage",
        "Processing ConEdison electricity bill",
        "Extracted: 2,850,000 kWh across 12 months",
        "Processing PSE&G natural gas bill",
        "Extracted: 78,000 therms across 12 months",
        "Calculating energy intensity",
        "923 kWh per metric ton",
        "Calculating GHG emissions",
        "Scope 2: 1,100 tCO2e",
        "Scope 1 (partial): 413 tCO2e",
        "Refrigerant data missing",
        "EXPIRES IN 30 DAYS",
        "Recycled content: NOT SPECIFIED",
    ]:
        assert phrase in html


def test_app_has_four_screen_flow_and_clickable_state_hooks():
    html = read("app/index.html")
    for phrase in [
        "data-view=\"intake\"",
        "data-view=\"processing\"",
        "data-view=\"assessment\"",
        "data-view=\"actions\"",
        "function setView",
        "function expandKpi",
        "function expandAction",
        "function renderFeedStep",
        "function updateKpiTracker",
        "data-kpi=\"energy-intensity\"",
        "data-kpi=\"packaging-recycled-content\"",
        "data-kpi=\"palm-oil-rspo\"",
        "data-action=\"send-draft\"",
        "data-action=\"schedule-voice\"",
        "demo-toast",
    ]:
        assert phrase in html


def test_app_has_fourteen_kpis_but_spotlights_only_key_cards():
    html = read("app/index.html")
    assert "const kpis = [" in html
    assert html.count("kpiId:") == 14
    for phrase in [
        "Facility KPIs",
        "Category KPIs",
        "Supply Chain KPIs",
        "Energy intensity",
        "GHG emissions",
        "Waste diversion",
        "Packaging recycled content",
        "Palm oil RSPO certification",
        "Worker safety TRIR",
        "hover or click for detail",
        "showing 5 spotlight cards; all 14 are tracked",
    ]:
        assert phrase in html


def test_app_has_followups_after_x_days_and_proactive_insights():
    html = read("app/index.html")
    for phrase in [
        "Email follow-up now",
        "Voice follow-up scheduled Day 7",
        "Acme Facilities Manager",
        "TruPak Packaging Co",
        "PT Sawit Indo",
        "Acme HR/EHS",
        "Acme Quality Manager",
        "BRC certificate expires March 14",
        "Same evidence library covers 45% of your CDP requirements",
        "52% of EcoVadis requirements",
        "3 quick wins could raise your score from 58 to 72",
        "THESIS rewards improvement trajectories",
    ]:
        assert phrase in html


def test_app_can_be_linked_from_existing_yc_demo():
    html = read("yc-demo/index.html") + read("index.html")
    assert "app/index.html" in html
    assert "Ops console" in html or "full app" in html
