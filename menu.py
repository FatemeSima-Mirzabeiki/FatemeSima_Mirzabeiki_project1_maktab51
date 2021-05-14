from student import Student, student_which_activity
from user import User
from education_administrator import EducationAdministrator, admin_which_activity
import json


def load_file():
    with open('user.json', 'r') as file:
        user_data = json.load(file)
    with open('course.json', 'r') as file:
        course_data = json.load(file)
    return user_data, course_data


def menu(choice, my_logger):
    user_data, course_data = load_file()
    try:
        assert choice in ['0', '1', '2']
        if choice == '0':
            return False
        elif choice == '1':
            user = User.sign_in(user_data, my_logger)
            if isinstance(user, User):
                if user.role == 'student':
                    student = Student.sign_in(user_data, user)
                    if not student.is_confirm:
                        print("\nNote...\nyour taking courses is not confirmed...\n")
                    return student_which_activity(user_data, course_data, student)
                else:
                    admin = EducationAdministrator.sign_in(user_data, course_data, user)
                    return admin_which_activity(user_data, course_data, admin)
            message = user
            print(message)
            return True
        elif choice == '2':
            student = Student.sign_up(user_data, course_data, my_logger)
            if isinstance(student, Student):
                print(f"\nWelcome {student.user_name}!\n")
                return student_which_activity(user_data, course_data, student)
            message = student
            print(message)
            return True
    except AssertionError:
        print("\nWRONG INPUT...\n")
        return True

