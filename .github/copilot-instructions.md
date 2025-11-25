<!-- Copilot / AI agent instructions for the Group-Project repo -->
# Copilot instructions — Group-Project

Purpose: Give AI coding agents immediate, actionable context for working in this repository.

**Repo Overview**
- **Type:** Small Flask web app (single-process) with a template UI and JSON API endpoints, expanding to CRUD inventory system.
- **Key files:** `app.py` (Flask app and routes), `templates/index.html` (UI), `requirements.txt`, `test_app.py` (pytest tests), `.github/workflows/auto.yml` (CI/CD with GitHub Actions + Azure VM deploy).

**Big-picture architecture**
- Single Flask application instance defined in `app.py`. Current routes:
  - `/` serves `templates/index.html` via `render_template`.
  - `/api/health` returns a JSON health payload.
  - `/api/info` returns project metadata JSON.
- CRUD expansion: Will add routes for `/items` (list), `/items/<id>` (detail), `/items/new` (create form), edit/delete operations.
- No separate packages, no database yet (TBD: SQLite + SQLAlchemy or lightweight storage). Deployment expects a WSGI server (`gunicorn` in `requirements.txt`).

**CI/CD Pipeline (GitHub Actions)**
- File: `.github/workflows/auto.yml`
- **Build job:** Checks out code, sets up Python 3.10, installs `requirements.txt`.
- **Test job:** Runs `pytest` on every push to `main` and PRs. Pipeline **fails** if tests fail (strict mode).
- **Deploy job** (runs on successful test + `main` branch push only):
  - Copies app code to Azure VM via SCP.
  - Installs dependencies and restarts gunicorn on the VM.
  - Requires three GitHub repository secrets (Settings > Secrets and Variables > Actions):
    - `AZURE_VM_IP`: Public IP or hostname of the Azure VM.
    - `AZURE_VM_USER`: SSH username (e.g., `azureuser`).
    - `AZURE_SSH_KEY`: Private SSH key (newline-delimited, base64-encoded if needed).

**Developer workflows & useful commands**
- Install dependencies and run tests (PowerShell):
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest
```
- Run the app locally (uses `PORT` env var if set):
```powershell
$env:PORT=5000; python .\app.py
```
- CI: `.github/workflows/auto.yml` runs on every `main` push and PR. Tests must pass for deploy to trigger.

**Project-specific patterns & conventions**
- Tests import the Flask `app` directly from `app.py` (see `test_app.py`). When changing route names or response shapes, update `test_app.py` accordingly.
- `app.run(...)` is used for local runs with `debug=False`. Avoid relying on `debug=True` behavior.
- HTML is in `templates/` (Jinja2). Static assets are not present — add `static/` if you introduce JS/CSS files.
- Deployment uses `gunicorn app:app -b 0.0.0.0:5000` on the Azure VM; app listens on port 5000.

**Integration points & external deps**
- `requirements.txt` lists runtime and test deps: `Flask`, `pytest`, `pytest-flask`, `gunicorn`.
- CI integration: GitHub Actions workflow at `.github/workflows/auto.yml`.
- Azure deployment: SSH-based via GitHub Actions secrets (see **CI/CD Pipeline** above).
- The UI mentions Azure in copy; deployment configuration is now in place (secrets-based).

**How AI agents should make changes**
- Preserve tests: run `pytest` locally after edits. Update tests when the API contract intentionally changes.
- Keep `app.py` as the single Flask entrypoint. If splitting into a package, update tests and imports consistently.
- When adding dependencies, also update `requirements.txt` and ensure CI still installs them.
- When changing deployment logic (gunicorn args, VM paths), update `.github/workflows/auto.yml` accordingly.

**Examples of typical edits**
- Add a new API endpoint `/api/metrics`:
  - Add route to `app.py`.
  - Add unit tests to `test_app.py` that exercise the new endpoint.
- Add CRUD routes for inventory items:
  - Add models (e.g., `Item` class) and persistence layer (SQLite + SQLAlchemy recommended).
  - Add routes (`/items`, `/items/<id>`, `/items/new`, edit, delete) to `app.py`.
  - Create templates: `templates/list.html`, `templates/detail.html`, `templates/form.html`.
  - Add integration tests to `test_app.py`.
- Make HTML changes in `templates/index.html`; no build step required.

**Files to review for context**
- `app.py` — app routes and run behavior.
- `test_app.py` — test expectations and fixtures.
- `.github/workflows/auto.yml` — CI/CD pipeline steps, Python version, deploy job, and secrets.
- `requirements.txt` — pinned dependencies used by CI and runtime.

**Azure VM Setup Checklist (for team)**
- [ ] Create Azure VM with SSH access enabled.
- [ ] Get VM IP, username, and SSH private key.
- [ ] In GitHub repo Settings > Secrets and Variables > Actions, add:
  - `AZURE_VM_IP`
  - `AZURE_VM_USER`
  - `AZURE_SSH_KEY` (private key content)
- [ ] Ensure gunicorn is listed in `requirements.txt`.
- [ ] Test SSH access locally before relying on GitHub Actions deploy.

If anything here is unclear or you want additional guidance (for example, preferred commit message style or storage choice), tell me what to add and I will iterate.
