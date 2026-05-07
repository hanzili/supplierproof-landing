# SupplierProof prototype backend

This backend lives inside the existing `supplierproof-landing` git repo. We do **not** need a separate git project yet.

Why here for now:
- the current product is still a single thin prototype,
- the frontend in `app/index.html` can be wired to this API without cross-repo deployment work,
- request-scoped storage lives under `storage/tenants/{tenant_id}/requests/{request_id}/`, matching the architecture plan.

## Run locally

```bash
cd /home/hanzi/projects/supplierproof-landing
python3 -m uvicorn backend.supplierproof_backend:app --reload --port 8765
```

Health check:

```bash
curl http://127.0.0.1:8765/health
```

## Prototype API

Create a request:

```bash
curl -X POST http://127.0.0.1:8765/requests \
  -F company_name='Acme Corporation' \
  -F industry='food_packaging' \
  -F framework='walmart_thesis' \
  -F tenant_id='demo'
```

Upload a file:

```bash
curl -X POST http://127.0.0.1:8765/requests/demo/{request_id}/uploads/questionnaires \
  -F file=@questionnaire.pdf
```

Buckets:
- `questionnaires`
- `documents`
- `metadata`

## Current parser coverage

Implemented now:
- TXT/MD/CSV/JSON/YAML/EML/MBOX text extraction
- DOCX extraction via zipped Word XML
- XLSX lightweight shared-string/sheet extraction
- ZIP manifest extraction
- PDF/image placeholders with stored file paths, ready for pypdf/OCR later

Questionnaire uploads also run a first-pass evidence extractor. The response includes `questionnaire_analysis` with:
- `question_count`
- `requirements[]` for detected evidence such as ISO 14001, IATF 16949, emissions workbooks, utility bills, recycled-content declarations, audit reports, safety records, food safety certificates, CMRT/EMRT, and EPD/HPD
- `preview`

The same analysis is appended into `manifest.json` under `questionnaire_files[]`, so each request keeps its own parsed questionnaire outputs.

## Safety model

- filenames are sanitized,
- file extensions are allowlisted,
- uploads are written only under one request folder,
- path-scope checks prevent escaping `storage/tenants/{tenant_id}/requests/{request_id}/`.
