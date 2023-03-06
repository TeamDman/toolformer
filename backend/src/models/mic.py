import io
from pydub import AudioSegment
import speech_recognition as sr
import whisper
import queue
import tempfile
import os
import threading
import torch
import numpy as np

def record_audio(audio_queue, energy, pause, dynamic_energy):
    r = sr.Recognizer()
    r.energy_threshold = energy
    r.pause_threshold = pause
    r.dynamic_energy_threshold = dynamic_energy

    with sr.Microphone(sample_rate=16000) as source:
        i = 0
        while True:
            #get and save audio to wav file
            audio = r.listen(source)
            torch_audio = torch.from_numpy(np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
            audio_data = torch_audio
            audio_queue.put_nowait(audio_data)
            i += 1


def transcribe_forever(audio_queue, result_queue, audio_model, english, verbose):
    while True:
        audio_data = audio_queue.get()
        if english:
            result = audio_model.transcribe(audio_data,language='english')
        else:
            result = audio_model.transcribe(audio_data)

        if not verbose:
            predicted_text = result["text"]
            result_queue.put_nowait(predicted_text)
        else:
            result_queue.put_nowait(result)

def start_background():
    model="base"
    audio_model = whisper.load_model(model).to("cuda")

    english=True
    verbose=False
    energy=100
    pause=0.8
    dynamic_energy=False

    audio_queue = queue.Queue()
    result_queue = queue.Queue()

    record_thread = threading.Thread(
        target=record_audio,
        args=(
            audio_queue,
            energy,
            pause,
            dynamic_energy,
        )
    )
    record_thread.start()

    transcribe_thread = threading.Thread(
        target=transcribe_forever,
        args=(
            audio_queue,
            result_queue,
            audio_model,
            english,
            verbose,
        )
    )
    transcribe_thread.start()
    
    return result_queue, (record_thread, transcribe_thread)