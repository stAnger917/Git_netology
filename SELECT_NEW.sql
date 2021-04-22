SELECT genres.gener_name, COUNT(genre_artist.artist_id) FROM genres
JOIN genre_artist ON genre_artist.genre_id = genres.genre_id
GROUP BY genres.gener_name

SELECT COUNT(tracks.track_id) FROM tracks 
JOIN albums ON albums.album_id = tracks.album_id 
WHERE albums.album_year BETWEEN 2019 AND 2020

SELECT albums.album_name, AVG(tracks.track_length) FROM albums 
JOIN tracks ON tracks.album_id = albums.album_id 
GROUP BY albums.album_name

SELECT artists.artist_name FROM artists 
INNER JOIN participants ON participants.artist_id = artists.artist_id 
INNER JOIN albums ON albums.album_id = participants.album_id
WHERE albums.album_year NOT IN ('2020')

SELECT compilations.compilation_name FROM compilations
INNER JOIN tracklist ON tracklist.compilation_id = compilations.compilation_id 
INNER JOIN tracks ON tracks.track_id = tracklist.track_id
INNER JOIN albums ON albums.album_id = tracks.album_id
INNER JOIN participants ON participants.album_id = albums.album_id
INNER JOIN artists ON artists.artist_id = participants.artist_id
WHERE artists.artist_name = 'Metallica'

SELECT albums.album_name FROM albums
INNER JOIN participants ON participants.album_id = albums.album_id
INNER JOIN artists ON artists.artist_id = participants.artist_id
INNER JOIN genre_artist ON genre_artist.artist_id = artists.artist_id
GROUP BY albums.album_name
HAVING COUNT(genre_artist.artist_id) > 1

SELECT tracks.track_name FROM tracks 
LEFT JOIN tracklist ON tracklist.track_id = tracks.track_id
WHERE tracklist.track_id IS NULL

SELECT artists.artist_id, artists.artist_name, MIN(tracks.track_length) AS track_length FROM artists 
INNER JOIN participants ON participants.artist_id = artists.artist_id
INNER JOIN albums ON albums.album_id = participants.album_id
INNER JOIN tracks ON tracks.album_id = albums.album_id
GROUP BY artists.artist_id

SELECT albums.album_name, COUNT(tracks.track_id) AS track_numbers FROM albums 
LEFT JOIN tracks ON tracks.album_id = albums.album_id
GROUP BY albums.album_name