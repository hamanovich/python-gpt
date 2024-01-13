import argparse
import datetime
import json
import os
import spotipy

from dotenv import load_dotenv
from openai import OpenAI


def bold(text):
    bold_start = "\033[1m"
    bold_end = "\033[0m"
    return bold_start + text + bold_end


def get_playlist(prompt, count=10):
    example_json = """
    [
      {"song": "Everybody Hurts", "artist": "R.E.M."},
      {"song": "Hurt", "artist": "Johnny Cash"},
      {"song": "Yesterday", "artist": "The Beatles"}
    ]
    """
    messages = [
        {"role": "system", "content": """You are a helpful playlist generating assistant. 
        You should generate a list of songs and their artists according to a text prompt.
        Your should return a JSON array, where each element follows this format: {"song": <song_title>, "artist": <artist_name>}
        """
         },
        {"role": "user", "content": "Generate a playlist of 3 songs based on this prompt: sad songs"},
        {"role": "assistant", "content": example_json},
        {"role": "user", "content": f"Generate a playlist of {
            count} songs based on this prompt: {prompt}"},
    ]

    response = client.chat.completions.create(
        messages=messages,
        model="gpt-3.5-turbo",
        max_tokens=400
    )

    playlist = json.loads(response.choices[0].message.content)
    return playlist


def generate_playlist(user, playlist):
    track_uris = []

    for item in playlist:
        artist, song = item["artist"], item["song"]

        advanced_query = f"artist:({artist}) track:({song})"
        basic_query = f"{song} {artist}"

        for query in [advanced_query, basic_query]:
            search_results = sp.search(q=query, limit=10, type="track")

            if not search_results["tracks"]["items"] or search_results["tracks"]["items"][0]["popularity"] < 20:
                continue
            else:
                good_guess = search_results["tracks"]["items"][0]
                print(f"Found: {good_guess['name']} [{good_guess['id']}]")
                track_uris.append(good_guess["id"])
                break

        else:
            print(f"Queries {advanced_query} and {
                  basic_query} returned no good results. Skipping.")

    created_playlist = sp.user_playlist_create(
        user["id"],
        public=False,
        name=f"{args.p} ({datetime.datetime.now().strftime('%c')})",
    )

    sp.user_playlist_add_tracks(
        user["id"], created_playlist["id"], track_uris)

    print(f"\nCreated playlist name: {bold(created_playlist['name'])}")
    print(bold(created_playlist["external_urls"]["spotify"]))


def main():
    current_user = sp.current_user()
    assert current_user is not None

    print("Loading... Please wait a bit ⏰")

    playlist = get_playlist(args.p, args.n)
    generate_playlist(current_user, playlist)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simple command line song utility")
    parser.add_argument("-p", type=str, default="fun songs",
                        help="The prompt to describe the playlist")
    parser.add_argument("-n", type=int, default=10,
                        help="The number of songs to add to the playlist")
    parser.add_argument("-envfile", type=str, default=".env", required=False,
                        help='A dotenv file with your environment variables: "SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET", "OPENAI_API_KEY"')
    args = parser.parse_args()

    load_dotenv(args.envfile)

    if any([x not in os.environ for x in ("SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET", "OPENAI_API_KEY")]):
        raise ValueError(
            "Error: missing environment variables. Please check your env file.")
    if args.n not in range(1, 50):
        raise ValueError("Error: n should be between 0 and 50")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    sp = spotipy.Spotify(
        auth_manager=spotipy.SpotifyOAuth(
            client_id=os.getenv("SPOTIFY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
            scope="playlist-modify-private"
        )
    )

    main()
