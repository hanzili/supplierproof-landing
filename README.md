# SupplierProof landing page

Quick static MVP landing page for SupplierProof.

## Files

- `index.html` — landing page content and SEO metadata
- `styles.css` — responsive visual design
- `tests/test_landing.py` — basic content/asset tests
- `supplierproof-preview.png` — desktop screenshot
- `supplierproof-mobile-preview.png` — mobile screenshot

## Run locally

```bash
cd /home/hanzi/projects/supplierproof-landing
python3 -m http.server 4177
```

Open: http://127.0.0.1:4177

## Verify

```bash
python3 -m pytest tests -q
```
