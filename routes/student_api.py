from routes import app
from flask import jsonify 

@app.route('/students/<student_id>', methods=['GET'])
def get_student(student_id):
    student = { 'id': student_id, 'name': 'John Doe', 'gender': 'male' }
    return jsonify(student)