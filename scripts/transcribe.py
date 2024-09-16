import ffmpeg
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch
import librosa

# Load pre-trained Wav2Vec2 ASR model
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

def transcribe_audio(filepath):
    audio, _ = librosa.load(filepath, sr=16000)
    inputs = processor(audio, sampling_rate=16000, return_tensors="pt", padding=True)
    
    with torch.no_grad():
        logits = model(inputs.input_values).logits
    
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)[0]
    
    return transcription

def transcribe_video(filepath):
    audio_filepath = 'temp_audio.wav'
    ffmpeg.input(filepath).output(audio_filepath).run()
    
    return transcribe_audio(audio_filepath)
