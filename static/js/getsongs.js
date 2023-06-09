async function getUserTrackData(offset) {
    response = await fetch('https://api.spotify.com/v1/me/tracks?limit=50&offset='+offset,{headers:header}).then(res => res.json());
    if (response.next == null) {
        is_next = false;
    } else {
        is_next = true;
    };
    let query_url = 'https://api.spotify.com/v1/audio-features?ids=' + ids.toString();
    let a = await fetch(query_url,{headers:header}).then(res => res.json());
    let audio_data = a.audio_features;

    let user_tracks = track_data.map((track,i) => ({
                    'explicit': track.track.explicit,
                    'track_popularity': track.track.popularity,
                    'artist_genres': track.track.artists[0].genres,
                    'artist_popularity':track.track.artists[0].popularity,
                    'release_date': track.track.album.release_date,
                    'album_genres': track.track.album.genres,
                    'album_popularity': track.track.album.popularity,

                    'acousticness': audio_data[i].acousticness,
                    'danceability': audio_data[i].danceability,
                    'duration': audio_data[i].duration_ms,
                    'energy': audio_data[i].energy,
                    'instrumentalness': audio_data[i].instrumentalness,
                    'key': audio_data[i].key,
                    'liveness': audio_data[i].liveness,
                    'loudness': audio_data[i].loudness,
                    'mode': audio_data[i].mode,
                    'speechiness': audio_data[i].speechiness,
                    'tempo': audio_data[i].tempo,
                    'time_signature': audio_data[i].time_signature,
                    'valence': audio_data[i].valence
                }));
    return user_tracks, is_next;
}