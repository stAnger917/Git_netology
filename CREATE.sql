create table if not exists artists (artist_id serial primary key, artist_name character varying(30) not null);

create table if not exists albums (album_id serial primary key, album_name character varying(40) not null, album_year integer not null);

create table if not exists participants (id serial primary key, artist_id integer not null references artists(artist_id), album_id integer not null references albums(album_id));

create table if not exists tracks (track_id serial primary key, track_name character varying(50) not null, track_length time not null, album_id integer not null references albums(album_id));

create table if not exists compilations (compilation_id serial primary key, compilation_name character varying(30) not null, compilation_year integer not null);

create table if not exists tracklist (id serial primary key, compilation_id integer not null references compilations(compilation_id), track_id integer not null references tracks(track_id));

create table if not exists genres (genre_id serial primary key, gener_name character varying(30) not null);

create table if not exists genre_artist (id serial primary key, genre_id integer not null references genres(genre_id), artist_id integer not null references artists(artist_id));