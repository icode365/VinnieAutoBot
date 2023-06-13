import spotipy as sp

class InvalidResultsError(Exception):
    pass

def searchSongUri(spotify: sp, song):

    orig = song
    song = song.replace(' ', '+')

    results = spotify.search(q=song, limit=1, offset=0, type='track')

    if not results['tracks']['items']:
        return None
    trackUri = results['tracks']['items'][0]['uri']
    return trackUri

def searchArtist(spotify: sp, artist):

    orig = artist
    artist = artist.replace(' ', '+')

    results = spotify.search(q=artist, limit=1, offset=0, type='artist')

    if not results['artists']['items']:
        raise InvalidResultsError(f'Could not Find {orig}.')

    artistUri = results['artists']['items'][0]['uri']
    return artistUri

def searchAlbum(spotify: sp, album):

    orig = album
    album = album.replace(' ', '+')

    results = spotify.search(q=album, limit=1, offset=0, type='playlist')

    if not results['playlists']['item']:
        raise InvalidResultsError(f'Could not Find {orig}.')

    playlistUri = results['playlists']['items'][0]['uri']
    return playlistUri


def play_track(spotify=None, uri=None):
    spotify.start_playback(uris=[uri])

def play_artist(spotify=None, uri=None):
    spotify.start_playback(context_uri=uri)

def play_album(spotify=None, uri=None):
    spotify.start_playback(context_uri=uri)
