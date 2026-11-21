import html
import json
import os
import urllib.error
import urllib.parse
import urllib.request


OUTPUT_FILE = "spotify-card.svg"


def api_request(url, access_token=None, data=None):
    headers = {"Accept": "application/json"}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    request = urllib.request.Request(
        url,
        data=urllib.parse.urlencode(data).encode() if data else None,
        headers=headers,
        method="POST" if data else "GET",
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode())


def get_playback():
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
    refresh_token = os.environ.get("SPOTIFY_REFRESH_TOKEN")
    if not all((client_id, client_secret, refresh_token)):
        return None

    credentials = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }).encode()
    request = urllib.request.Request(
        "https://accounts.spotify.com/api/token",
        data=credentials,
        method="POST",
    )
    import base64
    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    request.add_header("Authorization", f"Basic {auth}")
    request.add_header("Content-Type", "application/x-www-form-urlencoded")

    with urllib.request.urlopen(request, timeout=20) as response:
        token_data = json.loads(response.read().decode())
    access_token = token_data["access_token"]

    try:
        request = urllib.request.Request(
            "https://api.spotify.com/v1/me/player/currently-playing",
            headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        if error.code != 204:
            raise
        return None


def escape(value):
    return html.escape(str(value), quote=True)


def card_svg(track=None):
    if track:
        item = track.get("item") or {}
        title = item.get("name") or "Tocando no Spotify"
        artists = ", ".join(
            artist.get("name", "") for artist in item.get("artists", [])
        ) or "Spotify"
        album = item.get("album") or {}
        status = "Tocando agora"
        images = album.get("images") or []
        cover = images[0]["url"] if images else ""
    else:
        title = "Offline"
        artists = "Spotify"
        status = "Nada tocando agora"
        cover = ""

    image = ""
    if cover:
        image = (
            f'<image href="{escape(cover)}" x="22" y="22" width="116" '
            'height="116" clip-path="url(#coverClip)"/>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="520" height="160" viewBox="0 0 520 160" role="img" aria-label="{escape(status)}: {escape(title)} por {escape(artists)}">
  <rect width="520" height="160" rx="16" fill="#121212"/>
  <clipPath id="coverClip"><rect x="22" y="22" width="116" height="116" rx="12"/></clipPath>
{image}
  <circle cx="470" cy="35" r="10" fill="#1DB954"/>
  <path d="M464 31c7 4 13 4 19 1M465 35c6 3 12 3 17 1M466 39c5 2 10 2 14 0" fill="none" stroke="#121212" stroke-width="2" stroke-linecap="round"/>
  <text x="158" y="48" fill="#1DB954" font-family="Arial, sans-serif" font-size="14" font-weight="700">{escape(status)}</text>
  <text x="158" y="82" fill="#ffffff" font-family="Arial, sans-serif" font-size="22" font-weight="700">{escape(title[:38])}</text>
  <text x="158" y="112" fill="#b3b3b3" font-family="Arial, sans-serif" font-size="16">{escape(artists[:52])}</text>
</svg>
'''


def main():
    try:
        track = get_playback()
    except Exception as error:
        print(f"Nao foi possivel consultar o Spotify: {error}")
        track = None

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(card_svg(track))


if __name__ == "__main__":
    main()
