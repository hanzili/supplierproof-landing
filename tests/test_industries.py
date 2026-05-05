from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


def test_industry_pages_exist_and_are_static_discovery_pages():
    for filename in [
        "industries/index.html",
        "industries/epr.html",
        "industries/food-packaging.html",
        "industries/mining.html",
        "industries/plastics-registry.html",
        "industries/styles.css",
    ]:
        assert (ROOT / filename).exists(), filename


def test_industry_hub_positions_research_before_demo():
    html = read("industries/index.html")
    for phrase in [
        "Internal discovery hub",
        "Use the right page for the right compliance data workflow",
        "SupplierProof helps teams collect, check, reuse, and package supplier or member evidence",
        "EPR / producer responsibility reporting",
        "Food & packaging customer evidence requests",
        "Mining voluntary assurance",
        "Federal Plastics Registry readiness",
        "ask smart workflow questions",
        "we built ESG AI",
    ]:
        assert phrase in html


def test_epr_page_names_member_reporting_workflow():
    html = read("industries/epr.html")
    for phrase in [
        "Producer reporting gets stuck",
        "member reports",
        "product type, volume, weight, province/region",
        "fee-impacting corrections",
        "missing sales data",
        "reporting desk",
        "finance/audit",
    ]:
        assert phrase in html


def test_food_packaging_page_names_customer_request_objects():
    html = read("industries/food-packaging.html")
    for phrase in [
        "Customer sustainability requests",
        "CDP",
        "Walmart Gigaton",
        "EcoVadis",
        "THESIS-like assessments",
        "packaging claims",
        "RSPO/FSC",
        "approval-ready response package",
    ]:
        assert phrase in html


def test_mining_page_names_assurance_and_framework_overlap():
    html = read("industries/mining.html")
    for phrase in [
        "Mining voluntary assurance",
        "same evidence across frameworks",
        "TSM",
        "ICMM-aligned standards",
        "Copper Mark/IRMA-like",
        "assurance gaps",
        "site-owner follow-ups",
    ]:
        assert phrase in html


def test_plastics_page_names_registry_data_exchange():
    html = read("industries/plastics-registry.html")
    for phrase in [
        "Federal Plastics Registry",
        "resin categories",
        "products placed on market",
        "waste generated",
        "service-provider data",
        "facility/vendor responses",
        "submission support packet",
    ]:
        assert phrase in html


def test_industry_styles_are_polished_and_responsive():
    css = read("industries/styles.css")
    for token in ["linear-gradient", "box-shadow", "border-radius", "@media", "--lemon", "--green"]:
        assert token in css
