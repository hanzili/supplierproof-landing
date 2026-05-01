from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


def test_site_has_public_audience_navigation_and_hidden_investor_page():
    for filename in ["index.html", "buyers.html", "suppliers.html", "vision.html", "styles.css"]:
        assert (ROOT / filename).exists(), filename

    html = read("index.html")
    for phrase in [
        "SupplierProof",
        "One workflow, two entry points",
        "For buyers",
        "For suppliers",
        "buyers.html",
        "suppliers.html",
        "Talk about a pilot",
    ]:
        assert phrase in html
    assert "For investors" not in html
    assert "See investor page" not in html
    assert "vision.html" not in html


def test_home_page_has_external_facing_positioning_not_meta_copy():
    html = read("index.html")
    for phrase in [
        "Supplier documentation support for buyers and suppliers",
        "Not another ESG platform",
        "Start from either side",
        "a buyer can sponsor support for selected suppliers",
        "a supplier can use SupplierProof to respond better to customer requests",
        "One workflow, different incentives",
        "A buyer can initiate support for selected suppliers",
        "a supplier can initiate support to respond to customer requests",
        "Private prep and redactions make the workflow feel like support, not surveillance",
    ]:
        assert phrase in html
    assert "The home page should route people" not in html


def test_buyer_page_has_sample_output_scope_and_trust():
    html = read("buyers.html")
    for phrase in [
        "For procurement, supplier governance, and ESG teams",
        "Stop decoding every supplier reply yourself",
        "Sample triage output",
        "Supplier A",
        "We check",
        "We do not",
        "Buyer retains final decision",
        "NDA available",
        "No AI training on supplier documents without permission",
    ]:
        assert phrase in html


def test_supplier_page_has_private_until_submitted_controls():
    html = read("suppliers.html")
    for phrase in [
        "For participating suppliers",
        "Respond to customer ESG and compliance requests without starting from zero",
        "Private until submitted",
        "What your customer can and cannot see",
        "Draft answers",
        "Final response you approve",
        "We flag missing, expired, or weak evidence to you first",
        "Your documents remain yours",
    ]:
        assert phrase in html


def test_vision_page_has_source_backed_evidence_memory_story():
    html = read("vision.html")
    for phrase in [
        "For investors and early design partners",
        "source-backed evidence memory",
        "Buyer-led and supplier-led requests are the wedge",
        "How the wedge works",
        "Why two entry points work",
        "Compounding loop",
        "Manual today",
        "No fake ESG magic",
    ]:
        assert phrase in html


def test_pages_have_seo_and_shared_styles():
    for filename in ["index.html", "buyers.html", "suppliers.html", "vision.html"]:
        html = read(filename)
        assert "meta name=\"description\"" in html
        assert "meta name=\"viewport\"" in html
        assert "styles.css" in html


def test_styles_define_polished_multi_page_visual_system():
    css = read("styles.css")
    for token in [
        "linear-gradient",
        "box-shadow",
        "@media",
        ".audience-grid",
        ".split-hero",
        ".artifact-card",
        ".nav-links",
        ".sample-table",
        ".comparison-grid",
    ]:
        assert token in css
