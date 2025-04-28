from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 앱 초기화
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guestbook.db'
db = SQLAlchemy(app)

# 데이터베이스 모델
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    content = db.Column(db.String(200))
    password = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# DB 테이블 생성
with app.app_context():
    db.create_all()

# 메인 페이지: 메시지 리스트 보여주기
@app.route("/")
def index():
    messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template("index.html", messages=messages)

# 메시지 추가
@app.route("/add", methods=["POST"])
def add_message():
    name = request.form["name"]
    content = request.form["content"]
    password = request.form["password"]
    new_message = Message(name=name, content=content, password=password)
    db.session.add(new_message)
    db.session.commit()
    return redirect("/")

# 메시지 삭제
@app.route("/delete/<int:message_id>", methods=["POST"])
def delete_message(message_id):
    password = request.form["password"]
    msg = Message.query.get(message_id)
    if msg and msg.password.strip() == password.strip():
        db.session.delete(msg)
        db.session.commit()
        return redirect("/")
    else:
        return "비밀번호가 틀렸습니다.", 403

# 앱 실행
if __name__ == "__main__":
    app.run(debug=True)
