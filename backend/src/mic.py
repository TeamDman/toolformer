import speech_recognition as sr
import whisper
import asyncio
import torch
import numpy as np
from typing import *


async def record_audio(
    audio_queue: asyncio.Queue[torch.Tensor],
    energy: int,
    pause: float,
    dynamic_energy: bool,
    stop_event: asyncio.Event
):
    r = sr.Recognizer()
    r.energy_threshold = energy
    r.pause_threshold = pause
    r.dynamic_energy_threshold = dynamic_energy

    loop = asyncio.get_running_loop()

    print("[MIC] Starting listener")
    with sr.Microphone(sample_rate=16000) as source:
        print("[MIC] found microphone")
        while not stop_event.is_set():
            #get and save audio to wav file
            audio = await loop.run_in_executor(None, r.listen, source)
            torch_audio = torch.from_numpy(np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
            audio_data = torch_audio
            await audio_queue.put(audio_data)
    print("[MIC] Listener finished")

async def transcribe_forever(
    audio_queue: asyncio.Queue[torch.Tensor],
    result_queue: asyncio.Queue[str],
    audio_model: whisper.Whisper,
    english: bool,
    stop_event: asyncio.Event
):
    print("[MIC] Starting transcriber")
    while not stop_event.is_set():
        audio_data = await audio_queue.get()
        if english:
            result = audio_model.transcribe(audio_data, language='english')
        else:
            result = audio_model.transcribe(audio_data)

        predicted_text = str(result["text"]).strip()
        await result_queue.put(predicted_text)
    print("[MIC] Transcriber finished")
    

async def start_background():
    model = "base"
    audio_model = whisper.load_model(model).to("cuda")

    english = True
    energy = 100
    pause = 0.8
    dynamic_energy = False

    audio_queue: asyncio.Queue[torch.Tensor] = asyncio.Queue()
    result_queue: asyncio.Queue[str] = asyncio.Queue()
    stop_event = asyncio.Event()

    record_task = asyncio.create_task(
        record_audio(
            audio_queue,
            energy,
            pause,
            dynamic_energy,
            stop_event,
        )
    )

    transcribe_task = asyncio.create_task(
        transcribe_forever(
            audio_queue,
            result_queue,
            audio_model,
            english,
            stop_event,
        )
    )

    return result_queue, stop_event, record_task, transcribe_task

async def prompt_recognizer(voice_queue: asyncio.Queue[str], activation_keywords: List[str] | None = None):
    if activation_keywords is None:
        activation_keywords = ["computer", "pewter", "pewder", "cuter"]
    while True:
        prompt = await voice_queue.get()
        print(f"[MIC] heard '{prompt}'")
        activated = False
        for keyword in activation_keywords:
            if prompt.lower().startswith(keyword):
                activated = True
                prompt = prompt[len(keyword):].strip().strip(",").strip()
                break
        if activated:
            print(f"[MIC] activated with '{prompt}'")
            yield prompt
