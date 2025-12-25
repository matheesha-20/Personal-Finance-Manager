# Personal Finance Manager

A small Flask-based Personal Finance Manager web app to track and edit transactions.

This repository contains a minimal Flask application with templates and static assets.

## Features

- View a list of transactions
- Edit transactions via a simple form
- Lightweight, file-based code structure for learning and extension

## Requirements

- Python 3.8 or newer
- pip

Optional: create a virtual environment for local development.

## Quick start (Windows PowerShell)

From the repository root:

```powershell
cd finance_app
python -m venv .venv
.\.venv\Scripts\Activate.ps1
# If you have a requirements.txt, install it; otherwise install Flask directly
if (Test-Path requirements.txt) { pip install -r requirements.txt } else { pip install flask }
python app.py

# Open http://127.0.0.1:5000 in your browser
```

If the app is structured to use the `flask` command instead, you can also:

```powershell
cd finance_app
$env:FLASK_APP = 'app.py'
flask run
```

## Project structure

The repository contains the following important files and folders:

- `finance_app/`
  - `app.py` - Flask application entrypoint
  - `templates/` - HTML templates (`index.html`, `edit.html`, `base.html`)
- `static/` - static assets (CSS, JS, images)

## How to modify

- HTML templates: edit files under `finance_app/templates/`.
- Static assets: place CSS/JS in the `static/` folder and reference them from templates.

## Notes

- This README is intentionally minimal. If you'd like, I can add a `requirements.txt`, a `.gitignore`, or expand the README with screenshots, example data, and development tasks.

## License

Add a license file if you intend to publish or share this project.

---

If you'd like the README to include more details (example screenshots, API endpoints, tests, or CI), tell me what you'd like and I will extend it.
