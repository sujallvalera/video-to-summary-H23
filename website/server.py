from flask import *
import os
import openai
import moviepy.editor as mp
import time
import random
from dotenv import dotenv_values
env_vars = dotenv_values(".env")

app = Flask(__name__)

# Set the uploads directory path
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def generate_random_string():
    return f"{int(time.time())}-{random.randint(0, int(1E9))}"


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


fileAdd = ""


@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'videoFile' not in request.files:
            return "No file part", 400

        file = request.files['videoFile']

        if file.filename == '':
            return "No selected file", 400

        filename = generate_random_string() + ".mp4"

        global fileAdd
        fileAdd = filename

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        return redirect("/upload_success")
    except Exception as e:
        return str(e), 500


@app.route('/upload_success')
def script():
    clip = mp.VideoFileClip(fr"C:\\Users\HP\\PycharmProjects\\pythonProject1\\uploads\\{fileAdd}")
    audioName = generate_random_string()
    clip.audio.write_audiofile(fr"{audioName}.wav")

    # using openai's whisper tool to convert the audio file to text
    openai.api_key = env_vars["API_KEY"]
    audio_file = open(f"{audioName}.wav", "rb")
    trans = openai.Audio.transcribe('whisper-1', audio_file)
    text = trans["text"]

    # using openai to convert the given text to a summary
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": f"I want you to summarize the following to a small short actually very short and sweet summary which should cover all the points of the given text. If there are any dates mentioned in it, I want you to note it down in the summary and for what purpose it is used. Here's the text - {text}"}
        ]
    )
    summary = completion.choices[0].message["content"]
    return render_template('summary.html', line1=text, line2=summary)


if __name__ == '__main__':
    app.run(port=3000)
