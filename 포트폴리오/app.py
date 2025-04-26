from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guestbook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 모델 정의
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    content = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# DB 테이블 생성
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post', methods=['POST'])
def post():
    name = request.form['name']
    content = request.form['content']
    new_msg = Message(name=name, content=content)
    db.session.add(new_msg)
    db.session.commit()
    return redirect('/messages')

@app.route('/messages')
def messages():
    all_messages = Message.query.all()
    return render_template('messages.html', messages=all_messages)


@app.route('/delete/<int:msg_id>', methods=['POST'])
def delete(msg_id):
    msg = Message.query.get_or_404(msg_id)
    db.session.delete(msg)
    db.session.commit()
    return redirect('/messages')


if __name__ == '__main__':
    app.run(debug=True)
