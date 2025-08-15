from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

app = Flask(__name__)
CORS(app)

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

@app.route('/klasifikasi', methods=['POST'])
def klasifikasi():
    data = request.json
    komentar = data.get('komentar', '')

    vektor = vectorizer.transform([komentar])
    prediksi = model.predict(vektor)[0]

    return jsonify({'label': prediksi})

if __name__ == '__main__':
    app.run(port=5000)
