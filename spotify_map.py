import webbrowser

spotify_playlists = {
    "happy": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
    "sad": "https://open.spotify.com/playlist/37i9dQZF1DWVrtsSlLKzro",
    "angry": "https://open.spotify.com/playlist/37i9dQZF1DX1rVvRgjX59F",
    "neutral": "https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6",
    "surprise": "https://open.spotify.com/playlist/37i9dQZF1DX1BzILRveYHb",
    "fear": "https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6"
}

def open_spotify(emotion):
    emotion = emotion.lower()
    if emotion in spotify_playlists:
        print(f"[SPOTIFY] Opening playlist for emotion: {emotion}")
        webbrowser.open(spotify_playlists[emotion])
    else:
        print("[SPOTIFY] No playlist mapped for this emotion")
