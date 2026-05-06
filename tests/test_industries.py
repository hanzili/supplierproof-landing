from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


INDUSTRY_PAGES = [
    "industries/index.html",
    "industries/epr.html",
    "industries/food-packaging.html",
    "industries/mining.html",
    "industries/plastics-registry.html",
]


def test_industry_pages_exist_and_are_external_facing():
    for filename in INDUSTRY_PAGES + ["industries/styles.css"]:
        assert (ROOT / filename).exists(), filename


def test_pages_do_not_include_internal_discovery_language():
    forbidden = [
        "Questions we want to ask operators",
        "What we think is happening",
        "Agent/service hypothesis",
        "hypothesis",
        "operator interviews",
        "Internal discovery hub",
        "ask smart workflow questions",
        "we built ESG AI",
        "is this real",
        "where is it wrong",
        "Best advisor/channel signal",
        "Best current ICP fit",
        "Regulatory tailwind",
        "Clean Farms-like",
    ]
    for filename in INDUSTRY_PAGES:
        html = read(filename)
        for phrase in forbidden:
            assert phrase not in html, f"{phrase} leaked into {filename}"


def test_industry_hub_is_prospect_facing():
    html = read("industries/index.html")
    for phrase in [
        "Turn messy compliance data requests into review-ready evidence",
        "SupplierProof helps teams collect missing data",
        "Human review before anything is sent",
        "How we usually start",
        "Start with one live or recent request",
        "EPR / producer responsibility reporting",
        "Food & packaging customer evidence requests",
        "Mining assurance evidence",
        "Plastics reporting readiness",
    ]:
        assert phrase in html


def test_epr_page_names_external_member_reporting_workflow():
    html = read("industries/epr.html")
    for phrase in [
        "What SupplierProof helps manage",
        "Producer reporting gets stuck",
        "product categories, sales volume, weights, province or region",
        "finance handoff",
        "Common reporting bottlenecks",
        "Start with one sample",
        "Blank reporting form or member agreement",
    ]:
        assert phrase in html


def test_food_packaging_page_names_external_customer_request_objects():
    html = read("industries/food-packaging.html")
    for phrase in [
        "Customer sustainability requests are messy",
        "What SupplierProof helps manage",
        "CDP",
        "Walmart Gigaton",
        "EcoVadis",
        "THESIS-like assessments",
        "packaging claims",
        "RSPO/FSC",
        "approval-ready response package",
        "Start with one sample",
    ]:
        assert phrase in html


def test_mining_page_names_external_assurance_evidence_workflow():
    html = read("industries/mining.html")
    for phrase in [
        "One set of site evidence often has to support several mining standards",
        "What SupplierProof helps manage",
        "TSM",
        "ICMM-aligned standards",
        "Copper Mark/IRMA-like frameworks",
        "Common evidence bottlenecks",
        "Start with one sample",
        "Redacted evidence index",
    ]:
        assert phrase in html


def test_plastics_page_names_external_registry_data_workflow():
    html = read("industries/plastics-registry.html")
    for phrase in [
        "Plastic reporting requires data from more than one spreadsheet",
        "What SupplierProof helps manage",
        "resin categories",
        "products placed on market",
        "facilities, franchisees, vendors, or service providers",
        "submission support packet",
        "Start with one sample",
    ]:
        assert phrase in html


def test_industry_styles_are_polished_and_responsive():
    css = read("industries/styles.css")
    for token in ["linear-gradient", "box-shadow", "border-radius", "@media", "--lemon", "--green"]:
        assert token in css
