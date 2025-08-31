# Video Summarizer

## General Info
This project summarizes videos by downloading them from Youtube, transcripting and summarizing them using some ai models.

## Setup
To run this project, you can use docker:
```
$ docker build -t image-name .
$ docker run -p 5000:5000 image-name
```

OR install it locally using a python environment:

```
$ pip install requirements.txt
$ winget install FFmpeg 
$ python app.py
```