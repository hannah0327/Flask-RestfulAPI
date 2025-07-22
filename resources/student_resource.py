from flask_restful import Resource
from resources import api
from flask import jsonify

# 定義學生資源，這裡僅作為示例，無連接資料庫
class StudentResource(Resource):
    def get(self, student_id: int):
        if student_id == 1:
            return {'id': student_id, 'name': 'John Doe', 'gender': 'male'}
        else:
            return {'error': f'Student not found for id: {student_id}'}, 404
    
    def put(self, student_id: int):
        return {'id': student_id, 'name': 'Mary Doe', 'gender': 'female'}

api.add_resource(StudentResource, '/students/<int:student_id>')