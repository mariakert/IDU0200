from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import json
import gridfs
import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
TIME = 5
BIT_RATE = 44100
CHANNELS = 2

app = Flask(__name__)


client = MongoClient('localhost', 27017)
db = client.Words
fs = gridfs.GridFS(db)


@app.route('/addWord', methods=['POST'])
def add_word():
    try:
        json_data = request.json
        word = json_data['word']

        file = str(fs.put(open(r'recording.wav', 'rb'), content_type='audio/wav'))

        db.words.insert_one({
            'word': word, 'file': file
        })
        return jsonify(status='OK', message='inserted successfully')

    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


@app.route('/getWord', methods=['POST'])
def get_word():
    try:
        json_data = request.json
        word = json_data['word']

        print(word)

        database_word = db.words.find_one({'word': word})
        """print(str(database_word['_id']))
        print(database_word['word'])
        print(database_word['file'])"""

        if database_word is None:
            return jsonify(status='ERROR', message='entry not found')
        else:
            word_item = {
                'id': str(database_word['_id']),
                'word': database_word['word'],
                'audioFile': database_word['file']
            }
            return json.dumps(word_item)

    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


@app.route('/getAllWords', methods=['GET'])
def get_all_words():
    try:
        words = db.words.find({})

        word_list = []
        for word in words:
            word_item = {
                'id': str(word['_id']),
                'word': word['word'],
                'audioFile': word['file']
            }
            word_list.append(word_item)

        print("word list: " + json.dumps(word_list))

        return json.dumps(word_list)
    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


@app.route('/updateWord', methods=['POST'])
def update_word():
    try:
        json_data = request.json
        word = json_data['word']

        database_word = db.words.find_one({'word': word})
        file = str(fs.put(open(r'recording.wav', 'rb')))
        print(file)
        db.words.update_one({'_id': database_word['_id']}, {'$set': {'file': file}}, upsert=False)
        return jsonify(status='OK', message='inserted successfully')

    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


@app.route('/record', methods=['POST'])
def record():
    try:
        json_data = request.json
        word = json_data['word']
        file_name = "recording.wav"

        audio = pyaudio.PyAudio()

        # start Recording
        stream = audio.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=BIT_RATE,
                            input=True,
                            frames_per_buffer=CHUNK)
        print("recording...")
        frames = []

        for i in range(0, int(BIT_RATE / CHUNK * TIME)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("finished recording")

        # stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()

        wave_file = wave.open(file_name, 'wb')
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(audio.get_sample_size(FORMAT))
        wave_file.setframerate(BIT_RATE)
        wave_file.writeframes(b''.join(frames))
        wave_file.close()
        return jsonify(status='OK', message='inserted successfully')
    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


@app.route('/play', methods=['POST'])
def play_word():
    try:
        json_data = request.json
        file = json_data['audioFile']
        with open('result.wav', 'wb+') as f:
            f.write(fs.get(ObjectId(file)).read())
            f.close()

        wf = wave.open('result.wav', 'rb')

        audio = pyaudio.PyAudio()

        stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)

        data = wf.readframes(CHUNK)

        while data != '':
            stream.write(data)
            data = wf.readframes(CHUNK)

        stream.close()
        audio.terminate()
        return jsonify(status='OK', message='played successfully')

    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
