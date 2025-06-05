import os

import discord
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

# discord stuff
intents = discord.Intents.default()
intents.message_content = True


client = discord.Client(intents=intents)
guild = discord.Guild

# spoofy stuff
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_KEY"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope="user-library-read, playlist-modify-public",
        open_browser=False,
    )
)


@client.event
async def on_ready():
    print("Hello {0.user} !".format(client))
    await client.change_presence(
        activity=discord.CustomActivity("Sugma ligma stinky boy")
    )


@client.event
async def on_message(message):
    if message.content.startswith("https://open.spotify.com"):
        # use spotify API to add to playlist :)
        track_id = message.content.removeprefix(
            "https://open.spotify.com/track/"
        ).split("?")[0]
        track = sp.track(track_id)
        sp.playlist_add_items(os.getenv("PLAYLIST_ID"), [track_id])
        print(track["name"], "by", track["artists"][0]["name"], "added to playlist")


if __name__ == "__main__":
    client.run(os.getenv("DISCORD_API_TOKEN"))
