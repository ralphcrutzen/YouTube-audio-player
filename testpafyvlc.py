import pafy
import vlc

print("Initialiseer")
instance = vlc.Instance("-A alsa")
player = instance.media_player_new()
player.audio_set_volume(50)

print("Open playlist url")
# Hieronder kun je eventueel een andere playlist url zetten
playlist = pafy.get_playlist("https://www.youtube.com/playlist?list=PLLQdvrCajN7QJeclf7blmZJgM7TCzP_AI")

title = playlist['title']
author = playlist['author']
nItems = len(playlist['items']) # aantal video's in playlist

for i in range(nItems):
    print("Track: " + str(i + 1))
    trackinfo = playlist['items'][i]['pafy']
    print (trackinfo)
    print("Ophalen link naar audio url...")
    url = playlist['items'][i]['pafy'].getbestaudio().url
    media = instance.media_new(url)
    player.set_media(media)
    print("Afspelen")
    player.play()
    # wacht tot video afgelopen is
    while player.get_state() != 6:
        continue
