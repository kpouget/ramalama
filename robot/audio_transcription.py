#!/usr/bin/env python3

import subprocess
import json
import requests
import os
import sys
import pathlib
import pty
import threading
import time
import re

WHISPER_PORT=8086
MCP_PORT = 8001
RAMALAMA_MCP_PORT = 8002
AUDIO_FILE = "output.wav"

import requests
import pyaudio # sudo dnf install -y python3-pyaudio
import wave

def record_audio(audio_file):
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second

    devnull = os.open(os.devnull, os.O_RDWR)
    old_stderr = os.dup(2)
    os.dup2(devnull, 2)

    try:
        p = pyaudio.PyAudio()
    finally:
        os.dup2(old_stderr, 2)  # restore stderr
        os.close(devnull)

    try:
        input("Press enter to start recording.")
    except KeyboardInterrupt:
        print()
        print("Interrupted")
        sys.exit(0)

    print('Recording')
    stop_flag = False

    def wait_for_enter():
        nonlocal stop_flag
        input("Press ENTER to stop...\n")
        stop_flag = True

    threading.Thread(target=wait_for_enter, daemon=True).start()

    stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

    frames = []  # Initialize array to store frames

    while not stop_flag:
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file

    with wave.open(audio_file, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))


def send_to_ramalama(instructions):
    ramalama_url = f"http://127.0.0.1:{RAMALAMA_MCP_PORT}"

    for instruction in instructions:
        if not instruction: continue
        print("NEXT INSTRUCTION:", instruction)
        #input("Press enter to send it to the model and the robot ...")
        print()
        print("Processing ...")
        response = requests.get(ramalama_url, params=dict(query=instruction))
        response.raise_for_status()
        if response.status_code != 200:
            print(f"Request failed with status code: {response.status_code}")
            return

        # Access the response data (e.g., as JSON)
        data = response.text
        print("Response:")
        print("*"*10)
        print(data)
        print("*"*10)


def transcribe_audio(audio_file):
    whisper_endpoint = f"http://localhost:{WHISPER_PORT}/inference"

    with open(audio_file, "rb") as f:
        audio_data = f.read()

    files = {"file": (audio_file, audio_data, "audio/wav")}
    response = requests.post(whisper_endpoint, files=files)

    response.raise_for_status()
    result = response.json()

    return result.get("text", "")


def split_instructions(transcription):
    instructions = []
    print("-"*10)
    for instruction in re.split(r'[,.\n]', transcription.strip()):
        instruction = instruction.strip()
        print(f"• {instruction}")
        instructions.append(instruction)
    print("-"*10)

    return instructions

def run():
    if "--reuse" not in sys.argv:
        print("🎙️ Recoding the instructions ...")
        record_audio(AUDIO_FILE)

    print("✍🏻 Transcribing the audio file ...")
    transcription = transcribe_audio(AUDIO_FILE)
    instructions = split_instructions(transcription)
    send_to_ramalama(instructions)
    print("### All done ###")
    print("Original nstructions:")
    split_instructions(transcription)

if __name__ == "__main__":
    run()
