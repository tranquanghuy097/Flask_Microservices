from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def to_json(self):
        student_json = {
            'id' : self.id,
            'name' : self.name
        }
        return student_json

@app.route("/students", methods = ['Get'])
def getAll():
    try:
        students = Student.query.all()
        student_list = []
        for student in students:
            student_list.append(student.to_json())
        return jsonify(student_list), 200
    except:
        return "Fail", 400

@app.route("/students", methods = ['Post'])
def add():
    try:
        item = Student(request.json['name'])
        db.session.add(item)
        db.session.commit()
    except:
        return "Fail", 400
    finally:
        return "Success", 201

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)
