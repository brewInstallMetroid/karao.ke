'''
Purpose: This is a general helper class to direct user actions in the application
Created: 11/9/26, Christopher Thompson
'''
from urllib.parse import parse_qs, urlparse
import re


class HelperBL:
    # If you have something that would be beneficial for this object to keep track of,
    # feel free to add it to this constructor!
    # some of the properties I will likely move to the Django session once we have way more pages
    def __init__(self, request):
        self.request = request
        self.userIsMobile = self.request.GET.get("mobile") == "1"

    def getUserLayout(self):
        """Returns string based on current value of self.userIsMobile"""
        return "mobile" if self.userIsMobile else "desktop"

    @staticmethod
    def get_youtube_video_id(url):
        """Return a YouTube video ID from common YouTube URL formats. Relocated from views.py
        Params: url - string
        Raises: AttributeError, ValueError
        Returns: None or video_id (str)
        """
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





