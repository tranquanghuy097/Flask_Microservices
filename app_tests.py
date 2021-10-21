from flask_testing import TestCase
import unittest
import json
from app import app, db, Student

class TestApp(TestCase):
    SQLALCHEMY_DATBASE_URI =  'sqlite:///test.sqlite3'
    TESTING = True

    student_list = ["Lan", "John", "Jack", "Diana"]

    def create_app(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = self.SQLALCHEMY_DATBASE_URI
        return app

    def setUp(self):
        db.create_all()
        for student in self.student_list:
            db.session.add(Student(student))
        db.session.commit()
    
    def test_get(self):
        response = self.client.get('/students')
        self.assertEqual(response.status_code, 200)
        for index in range(0, len(self.student_list)):
            assert self.student_list[index] == response.json[index]["name"]

    def test_post(self):
        data = {'name' : 'Mark'}
        response = self.client.post('/students', data=json.dumps(data), headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/students')
        name = response.json[len(self.student_list)]["name"]
        assert name == data["name"]

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
