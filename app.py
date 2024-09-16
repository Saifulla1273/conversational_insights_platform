from flask import Flask, render_template, request, redirect, url_for
import os
from scripts.transcribe import transcribe_audio, transcribe_video
from scripts.analyze import extract_topics, analyze_sentiment, generate_insights
from models import save_insights, init_db

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize the database
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Transcribe based on file type (video/audio)
    if file.filename.endswith('.mp4'):
        transcription = transcribe_video(filepath)
    else:
        transcription = transcribe_audio(filepath)

    # Process the transcription to extract insights
    topics = extract_topics(transcription)
    sentiment = analyze_sentiment(transcription)
    insights = generate_insights(transcription, topics, sentiment)

    # Save results in the database
    save_insights(file.filename, transcription, topics, sentiment, insights)

    return render_template('result.html', transcription=transcription, topics=topics, sentiment=sentiment, insights=insights)

if __name__ == '__main__':
    app.run(debug=True)
