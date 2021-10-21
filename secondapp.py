from flask import Flask
import requests

app = Flask(__name__)
app.config["SERVER_NAME"] = "127.0.0.1:3000"

@app.route("/num_of_students", methods = ['Get'])
def getAll():
    try:
        student_list = requests.get('http://127.0.0.1:5000//students').content
        return {'num' : len(student_list)}, 200
    except:
        return "Fail", 400

if __name__ == '__main__':
   app.run(debug = True)