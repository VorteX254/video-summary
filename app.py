import os
from flask import Flask, render_template, request
from moviepy import VideoFileClip
import whisper
from transformers import pipeline
import yt_dlp

app = Flask(__name__)


def download_video(url, output_path="dump/video.mp4"):
    if os.path.exists(output_path):
        os.remove(output_path)
    os.makedirs("dump", exist_ok=True)
    ydl_opts = {'format': 'mp4/best', 'outtmpl': output_path}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_path

def extract_audio(video_path, audio_path="dump/audio.wav"):
    if os.path.exists(audio_path):
        os.remove(audio_path)
    os.makedirs("dump", exist_ok=True)
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    return audio_path

def transcribe_audio(audio_path):
    print("Transcribing audio...")
    try:
        # Explicitly download and load the model
        print("Loading Whisper model (this may take a moment)...")
        model = whisper.load_model("tiny", download_root="./models")
        
        # Check if audio file exists
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
        # Perform transcription
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        print(f"Error during transcription: {str(e)}")
        return "Error: Could not transcribe audio"

def summarize_text(text, chunk_size=500):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # Break transcript into chunks
    words = text.split()
    chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

    summaries = []
    for chunk in chunks:
        try:
            summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)
            summaries.append(summary[0]['summary_text'])
        except Exception as e:
            print("Error summarizing chunk:", e)

    # Combine and format into bullet points
    bullets = "• " + "\n• ".join(summaries)
    return bullets

@app.route("/", methods=["GET", "POST"])
def index():
    
    summary = None
    
    if request.method == "POST":
        url = request.form["video_url"]

        video_file = download_video(url)
        audio_file = extract_audio(video_file)
        transcript = transcribe_audio(audio_file)
        summary = summarize_text(transcript)

    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    app.run(debug=True)
