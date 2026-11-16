# Video Summarizer

## General Info
This project summarizes videos by downloading them from Youtube, transcripting and summarizing them using some ai models.

## Setup
To run this project, you can use docker:
```
$ docker build -t image-name .
$ docker run -p 5000:5000 image-name
```

OR install it locally using a python environment (Python 3.13):

```
$ pip install -r requirements.txt
$ winget install FFmpeg
$ winget install DenoLand.Deno
$ python app.py
```

Deno is required because yt-dlp needs a JavaScript runtime to download from YouTube.

If YouTube downloads stop working, update yt-dlp first:

```
$ pip install -U "yt-dlp[default]"
```