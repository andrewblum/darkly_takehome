from flask import Flask, jsonify
import json
from sseclient import SSEClient
import threading
from flask_redis import FlaskRedis

app = Flask(__name__)
redis = FlaskRedis(app)

scores_url = "http://live-test-scores.herokuapp.com/scores"


def connect():
    # This endpoint provides a SSE stream of JSON that looks like the following:
    # {"studentId":"Emely10", "exam":10634, "score":0.729252306067532}
    # Data shape in our Redis store
    #   ID: 
    #         { type:
    #               'exam'
    #           scores: 
    #               [{id: 'mary8', score: 1}], 
    #           average: 
    #               1
    #           total:
    #               1
    #         } 
    #     
    #  exams: [id, id]
    #  students: [id, id] 

    messages = SSEClient(scores_url)
    if not redis.get('students'):
        redis.set('students', json.dumps([]))
    if not redis.get('exams'):
        redis.set('exams', json.dumps([]))

    for msg in messages:
        if msg.data:
            result = json.loads(msg.data)
            student_id = result['studentId']
            score = result['score']
            exam_id = result['exam']
            if not redis.get(student_id):
                data = {'type': 'student', 
                        'scores': [{'id': exam_id, 'score': score}], 
                        'average': score,
                        'total': score}
                redis.set(student_id, json.dumps(data))
                all_students = json.loads(redis.get('students'))
                all_students.append(student_id)
                redis.set('students', json.dumps(all_students))
            if not redis.get(exam_id):
                data = {'type': 'exam',
                        'scores': [{'id': student_id, 'score': score}], 
                        'average': score,
                        'total': score}
                redis.set(exam_id, json.dumps(data))
                all_exams = json.loads(redis.get('exams'))
                all_exams.append(exam_id)
                redis.set('exams', json.dumps(all_exams))

            # Update exam obj 
            exam = json.loads(redis.get(exam_id))
            exam['total'] += score
            exam['average'] = exam['total'] / len(exam['scores'])
            exam['scores'].append({'id': student_id, 'score': score})
            redis.set(exam_id, json.dumps(exam))

            # Update student obj
            student = json.loads(redis.get(student_id))
            student['total'] += score
            student['average'] = student['total'] / len(student['scores'])
            student['scores'].append({'id': exam_id, 'score': score})
            redis.set(student_id, json.dumps(student))
    

@app.before_first_request
def startup():
    thread = threading.Thread(target=connect)
    thread.start()


# /students that lists all users that have received at least one test score
@app.route('/students')
def students():
    # print(redis.keys())
    if redis.get('students'):
        return jsonify(json.loads(redis.get('students')))
    return 'No students, please try again later', 404


# /students/{id} that lists the test results for the specified student, and provides the student's average score across all exams
@app.route('/students/<id>')
def student(id):
    if redis.get(id):
        return jsonify(json.loads(redis.get(id)))
    return 'Student not found', 404


# /exams that lists all the exams that have been recorded
@app.route('/exams')
def exams():
    if redis.get('exams'):
        return jsonify(json.loads(redis.get('exams')))
    return 'No exams, please try again later', 404


# /exams/{number} that lists all the results for the specified exam, and provides the average score across all students
@app.route('/exams/<number>')
def exam(number):
    if redis.get(number):
        return jsonify(json.loads(redis.get(number)))
    return 'Exam not found', 404


if __name__ == "__main__":
    app.debug = True
    app.config['REDIS_URL'] = "redis://:password@localhost:6379/0"
    app.run(host="0.0.0.0", port=5000)