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


def test_app_prototype_is_full_application_shell_not_landing_page():
    html = read("app/index.html")
    css = read("styles.css")
    for phrase in [
        "SupplierProof Ops Console",
        "app-shell",
        "app-sidebar",
        "app-topbar",
        "data-screen=\"inbox\"",
        "data-screen=\"connectors\"",
        "data-screen=\"evidence\"",
        "data-screen=\"agents\"",
        "data-screen=\"approvals\"",
        "data-screen=\"settings\"",
        "Connectors",
        "Evidence Memory",
        "Always-on agents",
    ]:
        assert phrase in html
    for forbidden in ["Start with one request", "Schedule demo", "Book a demo", "hero", "landing"]:
        assert forbidden not in html
    for token in [".app-shell", ".app-sidebar", ".app-topbar", ".app-screen", ".app-screen.is-active", ".connector-card"]:
        assert token in css


def test_app_has_connector_onboarding_for_min_friction_sources():
    html = read("app/index.html")
    for phrase in [
        "Gmail",
        "Outlook",
        "Google Drive",
        "SharePoint",
        "NetSuite",
        "EcoVadis",
        "CDP",
        "Walmart Retail Link",
        "read-only scan",
        "selected folders only",
        "no outbound without approval",
        "data-connector=\"gmail\"",
        "data-connector=\"outlook\"",
        "data-connector=\"drive\"",
        "data-connector=\"sharepoint\"",
        "data-connector=\"netsuite\"",
    ]:
        assert phrase in html


def test_app_clickable_navigation_and_state_hooks_exist():
    html = read("app/index.html")
    for phrase in [
        "const appState",
        "function setScreen",
        "function selectRequest",
        "function toggleConnector",
        "function openEvidence",
        "function approveAction",
        "addEventListener",
        "data-request=\"walmart-thesis\"",
        "data-request=\"ecovadis-refresh\"",
        "data-request=\"cdp-climate\"",
        "data-evidence=\"brc-cert\"",
        "data-evidence=\"utility-bills\"",
        "data-action=\"approve\"",
        "app-toast",
    ]:
        assert phrase in html


def test_app_surfaces_proactive_ops_layer_not_only_reactive_packet():
    html = read("app/index.html")
    for phrase in [
        "Detected customer request",
        "Certificate expires in 24 days",
        "NetSuite production volume changed",
        "Proactive readiness",
        "watch inbox for new customer asks",
        "monitor certificate expiries",
        "reuse approved answers",
        "scan ERP changes",
        "Agent activity",
        "Readiness moved",
    ]:
        assert phrase in html
    assert "forward us everything" not in html.lower()
    assert "give them a packet" not in html.lower()


def test_app_can_be_linked_from_existing_yc_demo():
    html = read("yc-demo/index.html") + read("index.html")
    assert "app/index.html" in html
    assert "Ops console" in html or "full app" in html
