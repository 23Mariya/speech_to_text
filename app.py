import streamlit as st
import whisper
import numpy as np
import sounddevice as sd
import torch
import os
import wave
import pyaudio
import json
import vosk  # ✅ Corrected import

# Set up device for Whisper (CUDA if available, otherwise CPU)
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load Whisper Model
whisper_model = whisper.load_model("base", device=device)

# Load Vosk Model
vosk_model = vosk.Model("vosk-model-small-en-us-0.15")  # Ensure correct model path

# Initialize speech history if not present in session state
if 'whisper_history' not in st.session_state:
    st.session_state['whisper_history'] = []
if 'vosk_history' not in st.session_state:
    st.session_state['vosk_history'] = []

st.title("🎤 Real-Time Speech-to-Text (Offline)")

# **Layout with columns for side-by-side models**
col1, col2 = st.columns(2)

# **Whisper Model Section**
with col1:
    st.header("🔊 Whisper Speech-to-Text")

    # Function to record audio for Whisper
    def record_audio_whisper(filename="temp_whisper.wav", duration=5, samplerate=16000):
        audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
        sd.wait()
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(samplerate)
            wf.writeframes(audio.tobytes())

    # Button for Whisper Speech-to-Text
    if st.button("🎤 Speak Now (Whisper)"):
        record_audio_whisper()
        result = whisper_model.transcribe("temp_whisper.wav")
        recognized_text = result["text"]
        st.text_area("📝 Recognized Text (Whisper):", recognized_text, height=100)
        
        # Save to history
        st.session_state['whisper_history'].append(recognized_text)

    # Display Whisper History
    if st.session_state['whisper_history']:
        st.subheader("📝 Whisper History:")
        for idx, history in enumerate(st.session_state['whisper_history']):
            st.text(f"{idx + 1}. {history}")

# **Vosk Model Section**
with col2:
    st.header("🔊 Vosk Speech-to-Text")

    # Function to record audio for Vosk
    def record_audio_vosk(filename="temp_vosk.wav", duration=5):
        chunk = 1024
        format = pyaudio.paInt16
        channels = 1
        rate = 16000

        p = pyaudio.PyAudio()
        stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
        
        frames = []
        for _ in range(0, int(rate / chunk * duration)):
            data = stream.read(chunk)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        p.terminate()

        with wave.open(filename, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(format))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))

    # Function for Vosk speech recognition
    def recognize_speech_vosk(filename="temp_vosk.wav"):
        wf = wave.open(filename, "rb")
        rec = vosk.KaldiRecognizer(vosk_model, wf.getframerate())
        
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result["text"]
        
        final_result = json.loads(rec.FinalResult())
        return final_result["text"]

    # Button for Vosk Speech-to-Text
    if st.button("🎤 Speak Now (Vosk)"):
        record_audio_vosk()
        recognized_text_vosk = recognize_speech_vosk()
        st.text_area("📝 Recognized Text (Vosk):", recognized_text_vosk, height=100)
        
        # Save to history
        st.session_state['vosk_history'].append(recognized_text_vosk)

    # Display Vosk History
    if st.session_state['vosk_history']:
        st.subheader("📝 Vosk History:")
        for idx, history in enumerate(st.session_state['vosk_history']):
            st.text(f"{idx + 1}. {history}")

# Button to download the speech history as a text file
if st.button("Download History"):
    with open("speech_history.txt", "w") as file:
        file.write("Whisper Speech-to-Text History:\n")
        for history in st.session_state['whisper_history']:
            file.write(history + "\n")
        file.write("\nVosk Speech-to-Text History:\n")
        for history in st.session_state['vosk_history']:
            file.write(history + "\n")
    
    with open("speech_history.txt", "rb") as file:
        st.download_button("Download History File", file, file_name="speech_history.txt")
