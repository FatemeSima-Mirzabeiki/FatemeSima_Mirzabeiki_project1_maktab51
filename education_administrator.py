from user import User
from student import Student
import json


class EducationAdministrator(User):
    __users = []
    __passwords = []
    file_of_admins = 'admins.json'

    def __init__(self, user_name, password, major):
        super().__init__(user_name, password, major)

    @staticmethod
    def sign_in():
        return super().sign_in(EducationAdministrator.file_of_admins)

    @staticmethod
    def see_all_students():
        for i in range(Student.num_students()):
            # print(Student.students())
            pass
        return "students"

    @staticmethod
    def see_one_student(user_name):
        # Student.find_a_student(user_name)
        return "student"
