import json
import re
from urllib.parse import parse_qs, urlparse

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

MAX_RECENT_SONGS = 8
SESSION_KEY = "recently_played_songs"


def hello(request):
    """Render the homepage with only the recently played section."""
    return render(
        request,
        "hello/hello.html",
        {"recent_songs": request.session.get(SESSION_KEY, [])},
    )


def get_youtube_video_id(url):
    """Return a YouTube video ID from common YouTube URL formats."""
    try:
        parsed = urlparse((url or "").strip())
    except (AttributeError, ValueError):
        return None

    host = (parsed.hostname or "").lower()
    if host in {"youtu.be", "www.youtu.be"}:
        video_id = parsed.path.strip("/").split("/")[0]
    elif host in {"youtube.com", "www.youtube.com", "m.youtube.com", "music.youtube.com"}:
        if parsed.path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [""])[0]
        else:
            match = re.match(r"^/(?:embed|shorts)/([^/?]+)", parsed.path)
            video_id = match.group(1) if match else ""
    else:
        return None

    return video_id if re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id or "") else None


@require_POST
def record_recent_song(request):
    """Record a song after the voice-selection flow has selected and played it.

    The voice-selection code should POST `title` and `youtube_url` here.
    """
    if request.content_type == "application/json":
        try:
            payload = json.loads(request.body or b"{}")
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({"ok": False, "error": "Invalid JSON."}, status=400)
    else:
        payload = request.POST

    title = str(payload.get("title", "")).strip()[:100]
    youtube_url = str(payload.get("youtube_url", "")).strip()[:500]
    video_id = get_youtube_video_id(youtube_url)

    if not title or not video_id:
        return JsonResponse(
            {"ok": False, "error": "A song title and valid YouTube link are required."},
            status=400,
        )

    song = {
        "title": title,
        "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
        "video_id": video_id,
    }
    recent_songs = request.session.get(SESSION_KEY, [])
    recent_songs = [item for item in recent_songs if item.get("video_id") != video_id]
    recent_songs.insert(0, song)
    request.session[SESSION_KEY] = recent_songs[:MAX_RECENT_SONGS]
    request.session.modified = True

    if request.content_type == "application/json":
        return JsonResponse({"ok": True, "recent_songs": request.session[SESSION_KEY]})

    messages.success(request, f'Added "{title}" to Recently Played.')
    return redirect("home")


@require_POST
def clear_recent(request):
    """Clear the recently played list for the current browser session."""
    request.session.pop(SESSION_KEY, None)
    messages.success(request, "Recently played songs have been cleared.")
    return redirect("home")
