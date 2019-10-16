# CPSC 449 - Fall 2019 - Project 1

## Dependencies
This project depends on Foreman and all of the Python modules listed in `requirements.txt`. To install foreman and the modules and run:

```
sudo apt install ruby-foreman
pip3 install -r requirements.txt
```

If you run into dependency errors, ensure all of the modules in `requirements.txt` are install properly. You may have to use `apt install` to install some.

## Running the Application
To run the application, you have to initialize the database and run each service on their own port. To do so, run the following:

```
./init
foreman start
```

## Testing the Application
To test the application you can use the provided `curlfile` executable.
```
./curlfile
```
The executable creates, retrieves, updates, and deletes from the database using the endpoints of the application

## Endpoints
### Tracks
- `/tracks/<int:id>`
    - `GET` Retrieves a track given its ID
    - `DELETE` Deletes a track given its ID
    - `PATCH` Updates a track given its ID and the JSON data of the fields to be modified
- `/tracks`
    - `POST` Inserts a track given the JSON data of a new track

### Playlists
- `/playlists/<int:id>`
    - `GET` Retrieves a playlist given its ID
    - `DELETE` Deletes a playlist given its ID
- `/playlists`
    - `GET` Retrieves a playlist of a user given the argument `creator=`
    - `POST` Inserts a playlist given the JSON data of a new playlist
- `/playlists/all`
    - `GET` Retrieves all playlists

## Data Structure
Below are sample JSONs of the entities.
### Tracks
```
{
    "id" : 1
    "track_title": "Track Title",
    "album_title": "Album Title",
    "artist": "Artist's Name",
    "track_length": 2.6,
    "media_file_url": "file:///home/student/Music/mediafile1",
    "album_art_url": "file:///home/student/Music/albumart1"
}

```
### Playlists
```
{
    "title": "Playlist Title",
    "creator": "Username",
    "tracks" : [
        "file:///home/student/Music/media_file1",
        "file:///home/student/Music/media_file2"
    ],
    "description": "Description of playlist"
}
```
