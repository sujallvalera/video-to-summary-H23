import openai
import moviepy.editor as mp
from dotenv import dotenv_values
env_vars = dotenv_values(".env")

# initialization for conversion of video to audio using moviepy
print("Converting video into audio...")
clip = mp.VideoFileClip(r"C:\\Users\\HP\\Downloads\\The World Needs More Of You _ 1 Minute Motivational Speech.mp4")
clip.audio.write_audiofile(r"filename.wav")

# using openai's whisper tool to convert the audio file to text
openai.api_key = env_vars["API_KEY"]
audio_file = open("filename.wav", "rb")
print("Converting audio to text...")
trans = openai.Audio.transcribe('whisper-1', audio_file)
text = trans["text"]
print(f"Text - {text}")

# using openai to convert the given text to a summary
completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": f"I want you to summarize the following to a small short actually very short and sweet summary which should cover all the points of the given text. Here's the text - {text}"}
  ]
)
summary = completion.choices[0].message["content"]
print(f"Summary of the video - {summary}")
