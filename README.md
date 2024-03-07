# sco-recorder-poc

## Fetch
- If [LFS](https://git-lfs.com) is available, just clone the Repository
- Without LFS being installed, you can download the Repository as zip file and manually download `data/bbb_sunflower_1080p_30fps_normal.mp4` as raw file using the GitHub GUI

## Run
### Docker Compose
`docker compose up` should work without any modifications

### Docker
- `docker build -t sco-recorder-poc .`
e.g. `docker run --rm -ti -v $(pwd)/data:/data -p 127.0.0.1:8080:8080 -e SOURCE_PATH=/data/bbb_sunflower_1080p_30fps_normal.mp4 -e SOURCE_FPS=30 -e RECORDS_BASEPATH=/data -e RECORDS_HISTSIZE=10 sco-recorder-poc`

### Python (>= 3.10)
- `pip install -r requirements.txt`
- e.g. `pushd recorder; SOURCE_PATH=../data/bbb_sunflower_1080p_30fps_normal.mp4 SOURCE_FPS=30 RECORDS_BASEPATH=../data RECORDS_HISTSIZE=10 python3 main.py || true; popd`

## Use
### Curl
e.g. `curl -X POST -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"weight": 420}' localhost:8080/api/record | jq`

### Swagger
Open http://localhost:8080/docs and use 'Try it out'

### Jetbrains HTTP client
See `.http/record.http`

## Caveats
Since this is a PoC:
- There are neither unit tests nor integration tests
- There are basically no docs
- Error handling is incomplete
- Timing in `recorder/services/capture.py` is not correctly synced with the provided source
- Dependencies are not pinned to stable versions
- ...

## Attributions
Thanks https://github.com/blender for https://download.blender.org/peach/bigbuckbunny_movies/

## Other important notes
If you ever want to check for valid seat arrangements in a theatre, you could use:
```python
def is_valid_seat_arrangement(seats):
    for col in range(len(seats[0])):
        for row in reversed(range(len(seats))):
            if row != 0 and seats[row][col] < seats[row-1][col]:
                return False
    return True
```

Or a bit more readable:
```python
def is_valid_seat_arrangement(seats):
    for coli, _ in enumerate(seats[0]):
        col = [row[0] for row in seats]
        if col != sorted(col):
            return False
    return True
```
