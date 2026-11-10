# karao.ke

**A voice-controlled karaoke website for a TV and a phone.**

karao.ke is Group 7's project for **CSCI 4250**. The idea is to make karaoke something you can start from a browser rather than needing a dedicated karaoke machine. The TV or desktop displays the karaoke experience, while a phone is planned to handle voice commands and song selection.

> **Project status — Milestone 2 (November 2026):** The team has completed a runnable *paper prototype* showing the intended user flow. The GitHub repository contains the Django website and a standalone speech-recognition proof of concept, but **the complete voice-to-playback flow is not implemented in the website yet**. The sections below separate what works in code from what is currently represented in the prototype.

## Contents

- [What's working now](#whats-working-now)
- [Milestone 2 prototype](#milestone-2-prototype)
- [Tech stack](#tech-stack)
- [Local setup](#local-setup)
- [Running the website](#running-the-website)
- [Running the voice-recognition test](#running-the-voice-recognition-test)
- [Recently Played: developer notes](#recently-played-developer-notes)
- [Project structure](#project-structure)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [Project progress](#project-progress)
- [References](#references)

---

## What's working now

### Django website

- A homepage at **`/`**, also available at **`/hello/`**.
- A shared purple-and-white layout with a header, Home and Recently Played navigation links, and a footer.
- Basic responsive styling for smaller screens.
- A **Recently Played** section that displays song titles and links to their YouTube videos.
- Session-based song history: the backend keeps up to **8 recently played songs per browser session**, with the newest entry first. Recording the same YouTube video again moves it to the top instead of creating a duplicate.
- A **Clear history** button when there are songs in the list.
- Django's built-in admin page at **`/admin/`**.

**Important:** The Recently Played backend is in place, but the site does not yet have a finished song-selection/playback feature that automatically fills the list. The voice-recognition test described below is still a separate command-line program.

### Speech-recognition proof of concept

`Testing/songSelectionTest.py` uses a microphone and Google's speech-recognition service to recognize two sample song requests:

- *Pump Up the Jam*
- *Doctor Worm*

The test calibrates for background noise and handles timeouts, unclear speech, microphone problems, and connection errors. It prints the result in the terminal; it does **not** start video playback or communicate with the Django website yet.

---

## Milestone 2 prototype

For Milestone 2, the team created an interactive PowerPoint prototype and a demonstration video to show how the finished experience is expected to work. **These screens describe the design, not features that are all running in Django today.**

| Prototype feature | Intended behavior | Current state |
| --- | --- | --- |
| Home screen | Show the karaoke interface, player indicators, and a short Recently Played list | Django homepage and Recently Played section exist; player indicators are not implemented |
| Player indicators | Show up to 5 players; empty slots are white and occupied slots are green | Prototype only |
| Navigation | Move between Home and a dedicated Recently Played view | Current site has navigation links, but Recently Played is a section of the homepage, not a separate page |
| Phone interface | Give phone users a mobile layout with access to the same main areas | Basic responsive webpage exists; dedicated phone-controller flow is not implemented |
| Speak button | Let a phone user start listening and move through options with voice commands | Prototype only; the terminal-based voice test is separate |
| Now Playing/loading | Show a transition while the chosen YouTube video loads | Prototype only |
| YouTube playback | Embed the selected video and return home when it ends or is stopped | Not implemented in the website; Recently Played entries currently link out to YouTube |

### Changes since the first paper prototype

- Added a Recently Played area to the planned home screen.
- Expanded the planned navigation/menu behavior for phone and TV/desktop layouts.
- Worked out a clearer flow from requesting a song, to selecting it, to loading and playback, and then returning home.
- Replaced the open-ended add-player idea with a **maximum of 5 players** in the design.

The runnable prototype and demo video were submitted with the team's Milestone 2 materials; they are not part of the Django application in this repository.

---

## Tech stack

| Area | Technology |
| --- | --- |
| Language | Python 3.14 (the version used in the existing setup instructions) |
| Web framework | Django 6.1.2 |
| Database and sessions | SQLite and Django sessions in local development |
| Frontend | Django templates, HTML, and CSS |
| Speech recognition test | [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) using Google Web Speech API |
| Microphone access | PyAudio |
| Planned playback | Embedded YouTube videos (not yet integrated) |

There is currently **no `requirements.txt`** in the repository. Install the dependencies manually as shown below.

---

## Local setup

### Requirements

- Python 3.14
- Git
- A microphone and internet access if you want to run the separate voice test

### 1. Clone the repository

```bash
git clone https://github.com/brewInstallMetroid/karao.ke.git
cd karao.ke
```

### 2. Create a virtual environment

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
python -m pip install "django==6.1.2" SpeechRecognition pyaudio
```

If PyAudio fails to install, it may need PortAudio development libraries on your system:

- macOS (Homebrew): `brew install portaudio`
- Debian/Ubuntu: `sudo apt install portaudio19-dev python3-dev`
- Windows: first try `python -m pip install pyaudio`; available wheels depend on the Python version and platform.

The `.venv/` directory is ignored by Git and should not be committed.

---

## Running the website

Start from the repository root, then move into the **`proj/`** directory. The current template configuration uses relative paths, so running Django from this folder matters.

```bash
cd proj
python manage.py migrate
python manage.py runserver
```

Open one of these addresses:

| URL | Purpose |
| --- | --- |
| `http://127.0.0.1:8000/` | Main homepage and Recently Played section |
| `http://127.0.0.1:8000/hello/` | Alternate route to the same homepage |
| `http://127.0.0.1:8000/admin/` | Django admin |

You can create a local admin account with:

```bash
python manage.py createsuperuser
```

**What to expect:** Initially, the Recently Played section will say no songs have been played. This is normal until something posts a valid song to the recording endpoint. The page does not currently let users search for or play a song directly.

---

## Running the voice-recognition test

Open another terminal at the **repository root** (not inside `proj/`) with your virtual environment active:

```bash
python Testing/songSelectionTest.py
```

1. Allow the program to calibrate the microphone for about a second.
2. Press **Enter** when prompted, then say *Pump Up the Jam* or *Doctor Worm*.
3. It listens for up to 5 seconds for speech, with a phrase limit of 8 seconds.
4. Read the recognized request and response in the terminal, or press **Q** and Enter to quit.

If nothing is heard, the words cannot be understood, or the speech service is unavailable, the program prints an error message and allows another attempt.

> **Privacy:** The test uses Google's online recognition service, so microphone audio is sent to that service for transcription. It is not an offline recognition tool.

---

## Recently Played: developer notes

The homepage uses Django sessions to store the current browser's song history. The relevant logic is in `proj/karao/ke/views.py` and the routes are in `proj/karao/ke/urls.py`.

| Route | Method | Behavior |
| --- | --- | --- |
| `/` and `/hello/` | GET | Display the homepage and this session's recently played entries |
| `/recent/record/` | POST | Record a song title and YouTube URL |
| `/recent/clear/` | POST | Clear the current session's history |

To record a song, send the following fields to **`/recent/record/`** as form data or JSON:

```json
{
  "title": "Example song",
  "youtube_url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

Replace `VIDEO_ID` with an actual 11-character YouTube video ID. The backend accepts standard YouTube watch links as well as supported short, embed, and Shorts URL formats. Missing or invalid information returns an error; a successful JSON request returns the updated list, while a form submission redirects to the homepage.

The history is limited to **8 entries per session**, not 8 total users or 8 songs shared across the whole site. Django's CSRF protection applies to these POST routes. Recording a song is intended to happen after the voice-selection/playback flow is connected; that connection has not been implemented yet.

---

## Project structure

```text
karao.ke/
├── README.md
├── .gitignore
├── Testing/
│   └── songSelectionTest.py       # Standalone voice-recognition demo
└── proj/                          # Run manage.py from here
    ├── manage.py
    └── karao/
        └── ke/
            ├── settings.py        # Django configuration
            ├── urls.py            # Home, admin, record/clear routes
            ├── views.py           # Home and Recently Played session logic
            ├── asgi.py
            ├── wsgi.py
            ├── templates/
            │   ├── base.html
            │   └── hello/
            │       └── hello.html
            └── static/
                ├── css/style.css
                └── images/         # Static image assets
```

This is a guide to the main source files, not a listing of every generated Python or Django file.

---

## Contributing

1. Create a branch from `main` using a descriptive name (for example, `isaac-readme-update`).
2. Use the team's commit-message prefixes: `IMPL:`, `DEVOPS:`, `DOCS:`, and `TEST:`.
3. Open a pull request into `main`, include a short description, and explain how the changes were checked. Follow whichever review/merge process the team is currently using.
4. Avoid committing local databases, virtual environments, Python caches, IDE configuration, and secrets. See `.gitignore`.
5. Keep this README updated when a prototype feature becomes an implemented website feature.

**Before deployment:** `settings.py` currently contains a development `SECRET_KEY`, has `DEBUG = True`, and does not have production hosts configured. These settings are for local development and need to be secured before publishing the app.

---

## Roadmap

- [x] Create the Django project and initial site layout
- [x] Build a standalone voice-recognition proof of concept
- [x] Add a homepage at `/`
- [x] Add a session-based Recently Played backend and homepage display
- [x] Create and demonstrate the Milestone 2 interactive paper prototype
- [ ] Connect voice recognition/song selection to Django and the Recently Played endpoint
- [ ] Implement the phone Speak control and intended voice navigation
- [ ] Build the player indicators (up to 5 players)
- [ ] Add the Now Playing/loading view and embedded YouTube playback
- [ ] Create the full Recently Played view and planned navigation behavior
- [ ] Finish the mobile/TV interaction and test the full end-to-end flow
- [ ] Add a `requirements.txt` and application-level automated tests
- [ ] Prepare production configuration and deployment setup

Completed prototype tasks are design milestones; they do not mean the corresponding feature is already functional in the Django site.

---

## Project progress

### Milestone 2 — current

- Created an interactive paper prototype covering the phone and TV/desktop navigation and the song-request-to-playback flow.
- Refined the design with Recently Played, a five-player limit, and clearer navigation.
- Added a working homepage route and server-side Recently Played storage to the codebase, including recording and clearing entries.
- Updated the site's layout for the Recently Played page and basic smaller-screen support.
- **Remaining integration:** voice selection, phone controls, and embedded playback are not yet connected into a complete working site.

### Milestone 1

- Set up the Django project, base template, initial page, and Git repository.
- Built and tested standalone microphone-based song recognition.
- Added initial site styling and repository cleanup rules.
- Submitted the first paper prototype, tutorial code, and demonstration.

---

## References

- [Project repository](https://github.com/brewInstallMetroid/karao.ke)
- [Voice-recognition tutorial](https://www.youtube.com/watch?v=MRugVs73cVA)
- [SpeechRecognition documentation](https://pypi.org/project/SpeechRecognition/)
- [Django documentation](https://docs.djangoproject.com/en/6.1/)
