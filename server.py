from flask import Flask
import requests
app = Flask(__name__)

scores_url = "http://live-test-scores.herokuapp.com/scores"

@app.route('/')
def hello_world():
    return 'Hello, World!'


# A REST API /students that lists all users that have received at least one test score
@app.route('/students')
def students():
    return 'Hello, World!'


# A REST API /students/{id} that lists the test results for the specified student, and provides the student's average score across all exams
@app.route('/students/{id}')
def student():
    return 'Hello, World!'


# A REST API /exams that lists all the exams that have been recorded
@app.route('/exams')
def exams():
    return 'Hello, World!'


# A REST API /exams/{number} that lists all the results for the specified exam, and provides the average score across all students
@app.route('/exams/{number}')
def exam():
    return 'Hello, World!'


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)