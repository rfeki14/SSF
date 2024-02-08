import spotipy
from spotipy.oauth2 import SpotifyOAuth
from typing import Optional
import whosampled_scrape

def get_uri(url: str) -> Optional[str]:
    """
    Get the Spotify URI for a given URL.

    :param url: The URL to get the Spotify URI for.
    :return: The Spotify URI, or None if the URL is not a valid Spotify song URL.
    """
    if not url.startswith("https://open.spotify.com/track/"):
        return None
    return f"spotify:track:{(url.split("?")[0]).split("/")[4]}"

def get_info(sp: spotipy.Spotify, uri: str) -> dict:
    """
    Get information about a song using the Spotify API.

    :param sp: A Spotify object authenticated with the Spotify API.
    :param uri: The Spotify URI for the song.
    :return: A dictionary containing information about the song.
    """
    return sp.track(uri)

def run_prog():
    # Authenticate with the Spotify API
    client_id = "9044c95b995c4e39bcf13b0f872fab29"
    client_secret = "eaa20f3c178f4f1b97092cc11a5de496"
    redirect_uri = "http://localhost:8888"
    scope = "user-library-read user-top-read"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope))

    # Get the Spotify URI for the user-inputted song URL
    url = input("Type the URL of the song you want to get information about: ")
    uri = get_uri(url)
    if uri is None:
        print("Invalid URL. Please enter a valid Spotify song URL.")
        return
    print(uri)
    # Get information about the song
    song = get_info(sp, uri)

    # Print out the name and artist of the song
    print(f"{song['name']} by {song['artists'][0]['name']}")

    # Print out other information about the song, such as its album, release date, and popularity
    print(f"Album: {song['album']['name']}")
    print(f"Release date: {song['album']['release_date']}")
    print(f"Popularity: {song['popularity']}")
    # Get the samples used in the song
    whosampled_scrape.who_sampled(song)
run_prog()