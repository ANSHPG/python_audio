import pyaudio
import wave
import os
import speech_recognition as sr
import openai
import sys

audio = pyaudio.PyAudio() # Object creation
recognizer = sr.Recognizer()
key = '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'

client = openai.Client(api_key=key)

stream = audio.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024)

frames = []
try:
    while True:
        data = stream.read(1024)
        frames.append(data)
        slash_chars = ['-', '\\', '|', '/']
        for char in slash_chars:
            sys.stdout.write('\r')
            sys.stdout.write(f'recording: {char}')
            sys.stdout.flush()
except KeyboardInterrupt:
    print("\nrecording stopped!\n")
    pass
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()

    wave_file_path = 'E:\codes\ml\AUDIO\output.wav'
    with wave.open(wave_file_path, "wb") as sound_file:
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b"".join(frames))

    # Recognizing speech
    with sr.AudioFile(wave_file_path) as source:
        audio_data = recognizer.record(source)

    try:
        # Get the text from the audio input
        text_input = recognizer.recognize_google(audio_data)
        print("Transcription:", text_input)

        # Generate completions using GPT-3 based on the text input
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "you are a kind helpful assistant"},
                {"role": "user", "content": text_input}
            ]
        )

        # Print the generated response from GPT-3
        print("GPT-3 Response:", completion.choices[0].message.content)

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service:", e)
