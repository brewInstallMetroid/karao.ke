# karao.ke

**A voice-controlled karaoke website for a TV and a phone.**

karao.ke is Group 7's project for **CSCI 4250**. The idea is to make karaoke something you can start from a browser rather than needing a dedicated karaoke machine. The TV or desktop displays the karaoke experience, while a phone is planned to act as the microphone and handle voice commands and song selection.

> **Project status — Milestone 3 (November 2026):** The website now has a working **Speak button** that lets you move between Home and Recently Played by voice, right in the browser. The standalone speech-recognition test now asks you to confirm each song request. A usability test plan is ready. Adding songs by voice, a queue, phone controls, and YouTube playback are **not implemented in the website yet**. The sections below separate what works in code from what is still planned or in progress.

## Contents

- [What's working now](#whats-working-now)
- [In progress on branches](#in-progress-on-branches)
- [Design and prototype](#design-and-prototype)
- [Usability testing](#usability-testing)
- [Tech stack](#tech-stack)
- [Local setup](#local-setup)
- [Running the website](#running-the-website)
- [Using voice navigation](#using-voice-navigation)
- [Running the voice-recognition test](#running-the-voice-recognition-test)
- [Recently Played: developer notes](#recently-played-developer-notes)
- [Project structure](#project-structure)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [Project progress](#project-progress)
- [References](#references)

---

## What's working now

Everything in this section is merged into `main`.

### Django website

- A homepage at **`/`**, also available at **`/hello/`**, with a "Your Karaoke Queue" heading and a Recently Played section.
- A shared purple-and-white layout with a header, Home and Recently Played navigation links, a **Speak** button, and a footer.
- Basic responsive styling for smaller screens.
- A **Recently Played** section that displays song titles and links to their YouTube videos.
- Session-based song history: the backend keeps up to **8 recently played songs per browser session**, with the newest entry first. Recording the same YouTube video again moves it to the top instead of creating a duplicate.
- A **Clear history** button when there are songs in the list.
- Django's built-in admin page at **`/admin/`**.

### Voice navigation (new in Milestone 3)

The **Speak** button in the header listens for one spoken command using the browser's built-in Web Speech API:

| Say | Result |
| --- | --- |
| "home" | Goes to the homepage |
| "recently played" | Jumps to the Recently Played section |
| anything else | Shows what was heard and suggests saying "recently played" or "home" |

The status text next to the button shows "Listening…", the action taken, or an error. If the browser doesn't support speech recognition, the button is disabled and a message explains why. See [Using voice navigation](#using-voice-navigation).

**Important:** Recently Played is still a section of the homepage, not a separate page. The "Your Karaoke Queue" heading is a placeholder; there is no working queue yet. Voice navigation does not add or play songs, and nothing automatically fills Recently Played yet.

### Speech-recognition proof of concept

`Testing/songSelectionTest.py` is a separate command-line program that uses a microphone and Google's speech-recognition service to recognize two sample song requests:

- *Pump Up the Jam*
- *Doctor Worm*

After it hears a request, it now asks **"Is that right? (Y/N)"** and lets you retry if it misheard. It calibrates for background noise and handles timeouts, unclear speech, microphone problems, and connection errors. The team tested it successfully with TV audio playing in the background. It prints the result in the terminal; it does **not** start playback or communicate with the Django website.

---

## In progress on branches

This work exists in the repository but has **not been merged into `main`**, so it is not part of the running site:

| Branch | What it adds |
| --- | --- |
| `IMPL-mobile-device-routing` | A business-logic helper class (`proj/karao/ke/bl/HelperBL.py`) as groundwork for detecting mobile vs. desktop devices and showing each a different template; footer fixes |
| `tyrone-queue-followup` | A separate Queue page (currently an empty placeholder) and voice navigation to it |
| `tyrone-phone-controller` | A request loop, spoken feedback, and better handling of unknown songs and errors in the voice test |

Update this table as branches are merged or deleted.

---

## Design and prototype

For Milestone 2, the team created an interactive PowerPoint prototype and a demonstration video showing how the finished experience is expected to work. **These screens describe the design, not features that are all running in Django today.** The prototype and video were submitted with the team's milestone materials; they are not part of this repository.

| Prototype feature | Intended behavior | Current state |
| --- | --- | --- |
| Home screen | Show the karaoke interface, player indicators, a queue, and a short Recently Played list | Homepage and Recently Played section exist; queue is a heading only; player indicators not implemented |
| Player indicators | Show up to 5 players; empty slots are white and occupied slots are green | Prototype only |
| Navigation | Move between Home and a dedicated Recently Played view | Links and voice commands work, but Recently Played is a section of the homepage |
| Phone interface | Give phone users a mobile layout and use the phone as the microphone | Basic responsive page exists; mobile-device detection is on a branch; phone controller not implemented |
| Speak button | Let a user start listening and move through options by voice | **Implemented for Home/Recently Played navigation** on the website; song selection by voice is not |
| Song queue | Add songs by voice, see who is singing next, and remove songs | Not implemented; empty Queue page is on a branch |
| Now Playing/loading | Show a transition while the chosen YouTube video loads | Prototype only |
| YouTube playback | Embed the selected video and return home when it ends or is stopped | Not implemented; Recently Played entries link out to YouTube |

### Changes since the first paper prototype

- Added a Recently Played area to the planned home screen.
- Expanded the planned navigation/menu behavior for phone and TV/desktop layouts.
- Worked out a clearer flow from requesting a song, to selecting it, to loading and playback, and then returning home.
- Replaced the open-ended add-player idea with a **maximum of 5 players** in the design.

---

## Usability testing

The team has written a usability test plan for the application.

**Tasks participants will attempt:**

1. Connect their phones to the TV.
2. Use voice recognition to add multiple songs to the queue.
3. Delete songs from the queue.
4. Start a song and use their phone as a microphone.
5. View the recently played songs.

**Setup:** Sessions run over a Discord call with a webcam. Participants are recruited from a group of testers Audra has arranged.

| Role | Team member |
| --- | --- |
| Facilitator | Mason |
| Observer | Christopher |
| Computer | Dominic |

Most of these tasks depend on features that are not built yet (see the table above), so they will be run against the prototype or partly simulated by the "Computer" role until the features are implemented.

---

## Tech stack

| Area | Technology |
| --- | --- |
| Language | Python 3.14 (the version used in the existing setup instructions) |
| Web framework | Django 6.1.2 |
| Database and sessions | SQLite and Django sessions in local development |
| Frontend | Django templates, HTML, CSS, and a small amount of JavaScript |
| In-browser voice navigation | Web Speech API (`SpeechRecognition` / `webkitSpeechRecognition`) |
| Speech recognition test | [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) using Google Web Speech API |
| Microphone access (test) | PyAudio |
| Planned playback | Embedded YouTube videos (not yet integrated) |

There is currently **no `requirements.txt`** in the repository. Install the dependencies manually as shown below.

---

## Local setup

### Requirements

- Python 3.14
- Git
- A microphone for voice features, plus internet access for the speech services
- A browser that supports the Web Speech API (such as Chrome or Edge) for voice navigation

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

Django is all you need for the website; SpeechRecognition and PyAudio are only for the command-line voice test.

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

**What to expect:** Initially, the Recently Played section will say no songs have been played. This is normal until something posts a valid song to the recording endpoint. The page does not currently let users search for, queue, or play a song.

---

## Using voice navigation

1. Run the website as above and open `http://127.0.0.1:8000/` in a supported browser. Microphone access works on `localhost`/`127.0.0.1`; on other addresses the browser will usually require HTTPS.
2. Click **Speak** and allow microphone access if prompted.
3. When the status says "Listening…", say **"recently played"** or **"home"**.
4. The page navigates, and the status text confirms what happened. The button is disabled while listening and re-enables when recognition ends.

> **Privacy:** In Chrome, the Web Speech API sends audio to Google's servers for recognition. It is not offline.

---

## Running the voice-recognition test

Open another terminal at the **repository root** (not inside `proj/`) with your virtual environment active:

```bash
python Testing/songSelectionTest.py
```

1. Allow the program to calibrate the microphone for about a second.
2. Press **Enter** when prompted ("What song are we singing?"), then say *Pump Up the Jam* or *Doctor Worm*.
3. It listens for up to 5 seconds for speech, with a phrase limit of 8 seconds.
4. When asked **"Is that right? (Y/N)"**, type `Y` to accept or `N` to try again.
5. Read the response in the terminal, or press **Q** then Enter to quit.

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

The voice-navigation script lives in `proj/karao/ke/templates/base.html`. It finds the Home and Recently Played links by their `id`s (`home-link`, `recently-played-link`) and clicks them when a matching command is heard, so keep those IDs if you change the header. New commands can be added in the `recognition.onresult` handler.

---

## Project structure

```text
karao.ke/
├── README.md
├── .gitignore
├── Testing/
│   └── songSelectionTest.py       # Standalone voice-recognition demo (with Y/N confirmation)
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
            │   ├── base.html      # Shared layout, Speak button, voice-navigation script
            │   └── hello/
            │       └── hello.html # Homepage and Recently Played section
            └── static/
                ├── css/style.css
                └── images/         # Static image assets
```

This is a guide to the main source files on `main`, not a listing of every generated Python or Django file. Branch work (for example, `bl/HelperBL.py` and `queue.html`) will appear here once merged.

---

## Contributing

1. Create a branch from `main` using a descriptive name (for example, `isaac-readme-update`).
2. Use the team's commit-message prefixes: `IMPL:`, `DEVOPS:`, `DOCS:`, and `TEST:`.
3. Open a pull request into `main`, include a short description, and explain how the changes were checked. Follow whichever review/merge process the team is currently using.
4. Avoid committing local databases, virtual environments, Python caches, IDE configuration, and secrets. See `.gitignore`.
5. Keep this README updated when a prototype feature becomes an implemented website feature or a branch is merged.

**Before deployment:** `settings.py` currently contains a development `SECRET_KEY`, has `DEBUG = True`, and does not have production hosts configured. These settings are for local development and need to be secured before publishing the app. Microphone access in the browser will also require HTTPS once the site is served from a real domain.

---

## Roadmap

- [x] Create the Django project and initial site layout
- [x] Build a standalone voice-recognition proof of concept
- [x] Add a homepage at `/`
- [x] Add a session-based Recently Played backend and homepage display
- [x] Create and demonstrate the Milestone 2 interactive paper prototype
- [x] Add Y/N confirmation and improved prompts to the voice-recognition test
- [x] Add a Speak button with voice navigation between Home and Recently Played
- [x] Write the usability test plan
- [ ] Merge mobile-device detection and show separate phone and TV/desktop templates
- [ ] Merge the Queue page, then add songs to and remove songs from the queue by voice
- [ ] Connect voice song selection to Django and the Recently Played endpoint
- [ ] Use the phone as the microphone and voice controller
- [ ] Build the player indicators (up to 5 players)
- [ ] Add the Now Playing/loading view and embedded YouTube playback
- [ ] Create the full Recently Played view
- [ ] Run usability tests and act on the findings
- [ ] Add a `requirements.txt` and application-level automated tests
- [ ] Prepare production configuration and deployment setup

Completed prototype tasks are design milestones; they do not mean the corresponding feature is already functional in the Django site.

---

## Project progress

### Milestone 3 — current

- **Implementation:** Added a Speak button with in-browser voice navigation between Home and Recently Played (merged). Added Y/N confirmation, clearer prompts, and better retry handling to the voice test, which was tested successfully with TV audio in the background (merged). Started a business-logic helper class for mobile vs. desktop template routing and worked on the footer (on a branch).
- **Usability:** Wrote a usability test plan covering connecting phones, queuing and deleting songs by voice, singing with the phone as a microphone, and viewing recently played songs.
- **Video:** Recorded an implementation progress demo showing the homepage and voice navigation.
- **Documentation:** Documented the runnable prototype's features and the differences between the original paper prototype and the newer design, and updated this README for Milestone 3.
- **Remaining integration:** voice song selection, the queue, phone controls, and embedded playback are not yet connected into a complete working site.

### Milestone 2

- Created an interactive paper prototype covering the phone and TV/desktop navigation and the song-request-to-playback flow, plus a demonstration video.
- Refined the design with Recently Played, a five-player limit, and clearer navigation.
- Added a working homepage route and server-side Recently Played storage, including recording and clearing entries.
- Completed a UI overhaul and basic smaller-screen support.
- Connected Discord to GitHub for commit and pull request updates.

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
- [Web Speech API (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)
- [Django documentation](https://docs.djangoproject.com/en/6.1/)
