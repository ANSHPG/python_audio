import pyaudio
import wave
import os
import speech_recognition as sr
from test_openai import OpenAI
import openai

audio = pyaudio.PyAudio() # Object creation
recognizer = sr.Recognizer()
key = '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'

client = OpenAI()
client = openai.Client(api_key=key)


# client = OpenAI(api_key=key)
# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#   ]
# )

# print(completion.choices[0].message)



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
except KeyboardInterrupt:
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
        print("Transcription:", recognizer.recognize_google(audio_data))
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "you are a kind helpful assistant"},
            {"role": "user", "content": audio_data}
         ]
        )
        print(completion.choices[0].message.content)

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service:", e)
