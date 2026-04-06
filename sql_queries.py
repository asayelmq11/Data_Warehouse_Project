import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events (
    artist VARCHAR,
    auth VARCHAR,
    firstName VARCHAR,
    gender VARCHAR,
    itemInSession INT,
    lastName VARCHAR,
    length FLOAT,
    level VARCHAR,
    location VARCHAR,
    method VARCHAR,
    page VARCHAR,
    registration FLOAT,
    sessionId INT,
    song VARCHAR,
    status INT,
    ts BIGINT,
    userAgent VARCHAR,
    userId INT
);
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs (
    num_songs INT,
    artist_id VARCHAR,
    artist_latitude FLOAT,
    artist_longitude FLOAT,
    artist_location VARCHAR,
    artist_name VARCHAR,
    song_id VARCHAR,
    title VARCHAR,
    duration FLOAT,
    year INT
);
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id BIGINT IDENTITY(0,1),
    start_time TIMESTAMP,
    user_id INT,
    level VARCHAR,
    song_id VARCHAR,
    artist_id VARCHAR,
    session_id INT,
    location VARCHAR,
    user_agent VARCHAR
);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY,
    first_name VARCHAR,
    last_name VARCHAR,
    gender VARCHAR,
    level VARCHAR
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
    song_id VARCHAR PRIMARY KEY,
    title VARCHAR,
    artist_id VARCHAR,
    year INT,
    duration FLOAT
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    artist_id VARCHAR PRIMARY KEY,
    name VARCHAR,
    location VARCHAR,
    latitude FLOAT,
    longitude FLOAT
);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
    start_time TIMESTAMP PRIMARY KEY,
    hour INT,
    day INT,
    week INT,
    month INT,
    year INT,
    weekday INT
);
""")

# STAGING TABLES

staging_events_copy = ("""
COPY staging_events
FROM {0}
IAM_ROLE {1}
JSON {2}
REGION 'us-west-2';
""").format(
    config.get('S3','LOG_DATA'),
    config.get('IAM_ROLE','ARN'),
    config.get('S3','LOG_JSONPATH')
)

staging_songs_copy = ("""
COPY staging_songs
FROM {0}
IAM_ROLE {1}
JSON 'auto'
REGION 'us-west-2';
""").format(
    config.get('S3','SONG_DATA'),
    config.get('IAM_ROLE','ARN')
)

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays (
    start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
)
SELECT 
    TIMESTAMP 'epoch' + e.ts/1000 * INTERVAL '1 second',
    e.userId,
    e.level,
    s.song_id,
    s.artist_id,
    e.sessionId,
    e.location,
    e.userAgent
FROM staging_events e
JOIN staging_songs s
ON e.song = s.title
AND e.artist = s.artist_name
WHERE e.page = 'NextSong';
""")

user_table_insert = ("""
INSERT INTO users
SELECT DISTINCT userId, firstName, lastName, gender, level
FROM staging_events
WHERE userId IS NOT NULL;
""")

song_table_insert = ("""
INSERT INTO songs
SELECT DISTINCT song_id, title, artist_id, year, duration
FROM staging_songs;
""")

artist_table_insert = ("""
INSERT INTO artists
SELECT DISTINCT artist_id, artist_name, artist_location, artist_latitude, artist_longitude
FROM staging_songs;
""")

time_table_insert = ("""
INSERT INTO time
SELECT DISTINCT
    TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 second',
    EXTRACT(hour FROM TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 second'),
    EXTRACT(day FROM TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 second'),
    EXTRACT(week FROM TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 second'),
    EXTRACT(month FROM TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 second'),
    EXTRACT(year FROM TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 second'),
    EXTRACT(weekday FROM TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 second')
FROM staging_events
WHERE ts IS NOT NULL;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]