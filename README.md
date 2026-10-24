# karao.ke

**The TV karaoke website.** karao.ke is a Django web app for running karaoke on a TV. You pick a song by saying its name out loud, and the site handles the rest. It is the Group 7 project for **CSCI 4250**.

> **Status: Milestone 1 (M1).** The Django site is set up with a styled landing page, and voice song selection works as a standalone proof of concept. The two are not connected yet. See [Roadmap](#roadmap).

---

## Table of contents

- [Features](#features)
- [Tech stack](#tech-stack)
- [Getting started](#getting-started)
- [Running the website](#running-the-website)
- [Running the voice recognition test](#running-the-voice-recognition-test)
- [Project structure](#project-structure)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [Changelog](#changelog)
- [References](#references)


---

## Features

**Working now**
- Django site with a shared base layout: banner, logo, menu icon and footer
- Welcome page at `/hello/`
- Django admin at `/admin/`
- Voice song selection test (`Testing/songSelectionTest.py`), which:
  - calibrates the microphone for background noise
  - listens for a song name and turns it into text with Google Speech Recognition
  - recognizes two sample songs: *Pump Up the Jam* and *Doctor Worm*
  - handles silence, speech it can't understand, and network errors, and lets you try again

**Planned**
- See [Roadmap](#roadmap)

---

## Tech stack

| Area | Technology |
|------|------------|
| Language | Python 3.14 |
| Web framework | Django 6.1.2 |
| Database | SQLite (default for development) |
| Front end | Django templates, HTML and CSS |
| Speech to text | [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) (Google Web Speech API) |
| Microphone access | PyAudio |

---

## Getting started

### Prerequisites

- **Python 3.14** ([python.org/downloads](https://www.python.org/downloads/))
- **Git**
- A **microphone** and an **internet connection**, for the voice test only

### 1. Clone the repository

```bash
git clone https://github.com/brewInstallMetroid/karao.ke.git
cd karao.ke
```

### 2. Create and activate a virtual environment

The virtual environment folder is already listed in `.gitignore`, so it won't be committed.

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install "django==6.1.2" SpeechRecognition pyaudio
```

> **TODO:** Add a `requirements.txt` so this becomes `pip install -r requirements.txt`.

**If PyAudio fails to install:**
- **macOS:** run `brew install portaudio` first, then install PyAudio again.
- **Linux (Debian/Ubuntu):** run `sudo apt install portaudio19-dev python3-dev` first.
- **Windows:** `pip install pyaudio` normally installs a prebuilt version. If it fails, check that your Python version is one PyAudio supports.

---

## Running the website

Run these commands **from inside the `proj/` folder.** The template paths in `settings.py` are relative, so the site won't find its pages if you start it from anywhere else.

```bash
cd proj
python manage.py migrate
python manage.py runserver
```

Then open:

| URL | Page |
|-----|------|
| http://127.0.0.1:8000/hello/ | Welcome page |
| http://127.0.0.1:8000/admin/ | Django admin |

> There is no homepage at `/` yet, so that address shows a 404 page.

To log in to the admin, create an account first:

```bash
python manage.py createsuperuser
```

---

## Running the voice recognition test

This is a command-line demo and is not part of the website yet. From the repository root:

```bash
python Testing/songSelectionTest.py
```

1. Stay quiet for about a second while it calibrates the microphone.
2. Press **Enter**, then say a song name. It listens for up to 5 seconds and records up to 8 seconds.
3. It prints what it heard and whether it found a match.
4. Type **Q** and press Enter to quit.

Songs it knows: **"Pump Up the Jam"** and **"Doctor Worm"**.

| Message | Meaning |
|---------|---------|
| `Couldn't hear you. Say it again.` | No speech detected before the timeout |
| `That's on me. What'd you say?` | Speech was detected but couldn't be understood |
| `I wasn't able to connect...` | Couldn't reach Google's speech service. Check your internet connection. |
| `Couldn't use the mic...` | No microphone found, or permission was denied |

> **Privacy note:** recorded audio is sent to Google's speech service to be turned into text.

---

## Project structure

```
karao.ke/
├── README.md
├── .gitignore
├── Testing/
│   └── songSelectionTest.py      # Voice song selection proof of concept
└── proj/                         # Django project root (run manage.py from here)
    ├── manage.py
    └── karao/
        └── ke/                   # Django project package (settings: karao.ke.settings)
            ├── settings.py
            ├── urls.py           # Routes: /admin/, /hello/
            ├── views.py          # hello view
            ├── asgi.py
            ├── wsgi.py
            ├── templates/
            │   ├── base.html     # Shared layout: banner, logo, menu, footer
            │   └── hello/
            │       └── hello.html
            └── static/
                ├── css/style.css
                └── images/hamburger.png
```

These are not committed to the repo: `db.sqlite3`, `__pycache__/`, `.venv/`, `.vscode/`, `.idea/`, `*.log` and the `keys` file. See `.gitignore`.

---

## Contributing

1. **Branch from `main`.** Use a descriptive branch name, for example `yourname-feature`.
2. **Start commit messages with a type prefix:**
   - `IMPL:` for features and implementation
   - `DEVOPS:` for build, config and repository maintenance
   - `DOCS:` for documentation
   - `TEST:` for tests
3. **Open a pull request** into `main` with a short description of what changed and how you tested it.
4. **Don't commit** secrets, `db.sqlite3`, cache files or editor settings. Put secrets in the ignored `keys` file.

> **Security note:** the Django `SECRET_KEY` is currently written directly in `settings.py`. Move it to an environment variable or the `keys` file before the site is deployed anywhere.

---

## Roadmap

- [ ] Homepage at `/`
- [ ] Create a Django app for karaoke features, with models such as Song and Queue
- [ ] Song library: title, artist, audio file and lyrics
- [ ] Connect voice song selection to the website
- [ ] Lyrics display and audio playback on the TV screen
- [ ] Song queue
- [ ] Phone as a controller (`tyrone-phone-controller`)
- [ ] Working menu behind the hamburger icon
- [ ] Layout that works on phone screens
- [ ] `requirements.txt`
- [ ] Automated tests

_TODO: add milestone due dates (M2, M3, …) from the course schedule._

---

## Changelog

Built from the commit history on `main`. Newest first.

### M1

| Date | Change | Author | PR |
|------|--------|--------|----|
| 2026-10-19 | **UI update:** stylesheet, purple banner, logo, hamburger icon and fixed footer. Fixed static files not loading. | Christopher Thompson, Audra | [#5](https://github.com/brewInstallMetroid/karao.ke/pull/5) |
| 2026-10-18 | Base template layout: banner, logo and footer | Audra | [#2](https://github.com/brewInstallMetroid/karao.ke/pull/2) |
| 2026-10-18 | README: added tutorial links for the voice test | Pokey, mjtko314 | [#3](https://github.com/brewInstallMetroid/karao.ke/pull/3) |
| 2026-10-11 | **DevOps:** removed committed database and cache files, and extended `.gitignore` | brewInstallMetroid | none |
| 2026-10-11 | Removed `.vscode/settings.json` from the repo | brewInstallMetroid | none |
| 2026-10-11 | **Voice test v2:** request loop, mic calibration, timeouts, and handling for unknown songs and errors | tyronemjohnsonii | [#1](https://github.com/brewInstallMetroid/karao.ke/pull/1) |
| 2026-10-09 | **Voice test v1:** first proof of concept for speech recognition | mjtko314 | none |
| 2026-10-09 | Added `.gitignore` | brewInstallMetroid | none |
| 2026-10-09 | **Django site created:** project skeleton, `/hello/` page and base template | brewInstallMetroid | none |
| 2026-10-03 | Repository created | Christopher Thompson | none |

---

## References

- Voice recognition tutorial we followed: https://www.youtube.com/watch?v=MRugVs73cVA
- SpeechRecognition library: https://pypi.org/project/SpeechRecognition/
- Django documentation: https://docs.djangoproject.com/en/6.1/

---
