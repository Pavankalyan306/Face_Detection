# app.py

from flask import Flask, render_template, request, jsonify
import face_recognition
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# Change this list to the names of your known face image files
KNOWN_FACE_FILENAMES = ['Pavan Kalyan Kumar.jpg', 'Murali.jpg', 'Sapth.jpg','Screenshot_32.jpg']
# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'face_recognition_db'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Save the uploaded file
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    # Face recognition logic
    unknown_image = face_recognition.load_image_file(file_path)
    unknown_encoding = face_recognition.face_encodings(unknown_image)

    if len(unknown_encoding) > 0:
        for known_face_filename in KNOWN_FACE_FILENAMES:
            known_image_path = os.path.join('known_faces', known_face_filename)
            known_image = face_recognition.load_image_file(known_image_path)
            known_encoding = face_recognition.face_encodings(known_image)[0]

            result = face_recognition.compare_faces([known_encoding], unknown_encoding[0])
            if result[0]:
                # Fetch matched person's information from the database
                cur = mysql.connection.cursor()
                cur.execute("SELECT matched_person_name, matched_person_id FROM matched_images WHERE image_name = %s", (file.filename,))
                matched_person_info = cur.fetchone()
                cur.close()

                if matched_person_info:
                    matched_person_name, matched_person_id = matched_person_info
                    return jsonify(result="Face recognized as {}.".format(matched_person_name), name=matched_person_name,
                                   id=matched_person_id)

        return jsonify({'result': 'Face not recognized_Unknown Person'})
    else:
        return jsonify({'error': 'No face found in the uploaded image'})

@app.route('/matched_images')
def display_matched_images():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM matched_images")
    matched_images = cur.fetchall()
    cur.close()

    # Extract image names from the database entries
    image_names = [entry[1] for entry in matched_images]

    return render_template('matched_images.html', image_names=image_names)

if __name__ == '__main__':
    app.run(debug=True)
