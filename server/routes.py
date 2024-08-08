import os

from flask import Flask, render_template, request, jsonify, url_for
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from flask_mail import Mail, Message

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from ultralytics import YOLO
import cv2

from models import User, db
from itsdangerous import URLSafeTimedSerializer


app = Flask(__name__)
app.config.from_pyfile('config.py') 


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY']) 

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

jwt = JWTManager(app)
model = YOLO("model/final.pt")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']


    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"msg": "Username or email already exists"}), 400 


    hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    else:
        return jsonify({"msg": "Invalid credentials"}), 401

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token), 200

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data['email']
    user = User.query.filter_by(email=email).first()

    if user:
        token = s.dumps(email, salt='password-reset')
        msg = Message(
            'Reset Your Password',
            sender='your_email@gmail.com',
            recipients=[email]
        )
        link = url_for('reset_password', token=token, _external=True)  
        msg.body = f'Click the following link to reset your password: {link}'
        mail.send(msg)
        return jsonify(message='Password reset email sent'), 200
    else:
        return jsonify(message='User not found'), 404

@app.route('/reset_password/<token>', methods=['POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='password-reset', max_age=3600)
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return jsonify(message='Invalid or expired token'), 400
        
        data = request.get_json()
        new_password = data['new_password']
        hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=8)
        user.password = hashed_password
        db.session.commit()

        return jsonify(message='Password reset successful'), 200

    except:
        return jsonify(message='Invalid or expired token'), 400

@app.route('/classify', methods=['POST'])
@jwt_required()
def classify():
    if 'image' not in request.files:
        return jsonify(error='No file part')

    file = request.files['image']

    if file.filename == '':
        return jsonify(error='No selected file')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        image = cv2.imread(file_path)
        results = model(image, conf=0.6)
        highest_confidence = 0
        best_class_name = ""
        for r in results:
            for idx, class_idx in enumerate(r.probs.top5):
                class_name = r.names[class_idx]
                confidence = float(r.probs.top5conf[idx])
                if confidence > highest_confidence:
                    highest_confidence = confidence
                    best_class_name = class_name

        # Store the classification results in the database
        # Implement database storage logic here

        return jsonify(best_class_name=best_class_name, highest_confidence=highest_confidence)

    else:
        return jsonify(error='Invalid file type')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)