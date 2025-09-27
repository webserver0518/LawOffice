# LawOffice — Dev Notes (Private)

**Audience:** Me (Matan) only. This repository is private and contains internal notes and scaffolding for my law‑office management app (Flask).

> TL;DR: `python -m venv .venv && pip install -r requirements.txt && python run.py`

---

## Repo Shape (current)

```
app/
  __init__.py            # Flask app factory: create_app(env=...)
  routes/
    client.py            # Client-related endpoints (Blueprint)
  utils/
    s3_management.py      # S3 helper (boto3) - upload/list/delete
  templates/             # Jinja2 templates
  static/                # CSS / JS / images
run.py                   # WSGI entrypoint: app = create_app(...)
requirements.txt
.env                     # (local only; never commit) 
README.md                # (this file)
LICENSE                  # Private license
```

Notes:
- Admin page for user analytics is named **Users Statistics** (not `admin_stats`).
- I renamed `admin.html` → `user_management.html` (keep consistent everywhere).
- CSS is being split by page; `base_dashboard` dynamically loads per‑page CSS. Keep that pattern.

---

## Python & Tooling

- Python **3.10+**. I currently have **3.13.1 (64‑bit)** installed and added to PATH.
- Use **.venv** in repo root. Do *not* use the global interpreter.
- Editor: VS Code. Select the `.venv` interpreter after creation.

Create / activate venv:

```bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

Install deps:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

If `boto3` is missing → the requirements weren’t installed.

---

## Run

```bash
# 1) Environment (use .env or export)
# 2) Launch
python run.py
# or
flask run --port 5000
```

Default dev URL: http://127.0.0.1:5000/

Production-ish (manual):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

---

## Environment (local)

Create a **.env** from `.env.example` and fill values. Minimal set:

```
FLASK_ENV=development
SECRET_KEY=dev-change-me

AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=eu-central-1
S3_BUCKET_NAME=
S3_PREFIX=uploads/
APP_LOG_LEVEL=INFO
```

**Security:** Never commit real secrets. `.env` is git‑ignored.

---

## AWS / S3

- S3 bucket per environment (dev/prod). Keep prefixes per feature if useful.
- IAM: programmatic access restricted to the specific bucket ARN.
- If `AccessDenied`, triple‑check: account, region, bucket name, and credentials in `.env`.

Minimum policy (adjust the ARN):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "LawOfficeS3Access",
      "Effect": "Allow",
      "Action": ["s3:PutObject","s3:GetObject","s3:DeleteObject","s3:ListBucket"],
      "Resource": ["arn:aws:s3:::YOUR_BUCKET_NAME", "arn:aws:s3:::YOUR_BUCKET_NAME/*"]
    }
  ]
}
```

---

## Git Workflow (two machines)

- Always stash/commit before switching machines.
- Prefer **rebase** pulls to keep history clean:
  ```bash
  git pull --rebase origin main
  ```
- Keep `.env` local; never push secrets. Use `git update-index --assume-unchanged .env` if needed.

---

## Quality (optional but recommended)

```bash
pip install black ruff mypy
black .
ruff check .
mypy app
```

Set up pre‑commit (optional):

```bash
pip install pre-commit
pre-commit install
```

---

## Troubleshooting

- **`ModuleNotFoundError: boto3`** → `pip install -r requirements.txt`
- **Windows “No Python at ...WindowsApps\PythonSoftware”** → Reinstall Python, add to PATH, recreate `.venv`
- **Flask cannot find app** → ensure `create_app` exists in `app/__init__.py` and `run.py` does `app = create_app(env=...)`
- **S3 upload fails** → wrong region, wrong bucket, missing permissions, or invalid creds

---

## Roadmap / TODO (personal)

- [ ] Users Statistics dashboard: avg session duration, active hours, login counts.
- [ ] Persist login events (user + timestamp); later: aggregate stats queries.
- [ ] S3 file lifecycle rules (auto‑archive old uploads).
- [ ] Optional DB on AWS (RDS or DynamoDB) for users + audit logs.
- [ ] Basic test suite (pytest) and CI (GitHub Actions) for lint + tests.
- [ ] Dockerfile + Compose for local dev parity.
- [ ] Simple role‑based access control (admin vs user).

---

## Notes

- This README is **for me**; terseness > polish.
- Keep repo private and treat all data as confidential.
