from user import User
from student import Student
from course import Course
from education_administrator import EducationAdministrator


def menu(user):
    try:
        assert user not in [0, 1, 2]
        if user == "0":
            return False
        elif user == "1":
            # Student
            return student_menu()
        elif user == "2":
            # Education Administrator
            return admin_menu()
    except:
        print("\nWRONG INPUT...\n")
        return True


def student_menu():
    while 1:
        sign = input("\nENTER 1 ---> sign-in"
                     "\nENTER 2 ---> sign-up"
                     "\nENTER 0 ---> quit\n")
        try:
            assert sign not in [0, 1, 2]
            if sign == "0":
                return False
            elif sign == "1":
                if Student.sign_in():
                    return student_activities()
            elif sign == "2":
                print(Student.sign_up())
                print("\nnow, sign in please....\n")
                if Student.sign_in():
                    return student_activities()
        except:
            print("\nWRONG INPUT...\n")


def student_activities():
    while True:
        activity = input("\nENTER 1 ---> see your major`s courses"
                         "\nENTER 2 ---> take a course"
                         "\nENTER 3 ---> remove a course"
                         "\nENTER 4 ---> see courses you have chosen"
                         "\nENTER 5 ---> see number of your credits"
                         "\nENTER 0 ---> quit\n")
        try:
            assert activity not in [0, 1, 2, 3, 4, 5]
            if activity == "0":
                return False
            elif activity == "1":
                print(Course.list_of_courses())
            elif activity == "2":
                # student.take_course()
                print("course was taken")
            elif activity == "3":
                # student.delete_course()
                print("course was removed")
            elif activity == "4":
                # student.show_student_courses()
                print("students courses")
            elif activity == "5":
                # student.credit
                print("you have no credit")
        except:
            print("\nWRONG INPUT...\n")


def admin_menu():
    while 1:
        sign = input("\nENTER 1 ---> sign-in"
                     "\nENTER 0 ---> quit\n")
        try:
            assert sign not in [0, 1]
            if sign == "0":
                return False
            elif sign == "1":
                if EducationAdministrator.sign_in():
                    return admin_activities()
        except:
            print("\nWRONG INPUT...\n")


def admin_activities():
    while True:
        admin_activity = input("\nENTER 1 ---> create a course"
                               "\nENTER 2 ---> delete a course"
                               "\nENTER 3 ---> see a list of students"
                               "\nENTER 4 ---> choose a student"
                               "\nENTER 0 ---> quit\n")
        try:
            assert admin_activity not in [0, 1, 2, 3, 4]
            if admin_activity == "0":
                return False
            elif admin_activity == "1":
                print(Course.create_course())
            elif admin_activity == "2":
                print(Course.delete_course())
            elif admin_activity == "3":
                print(EducationAdministrator.see_all_students())
            elif admin_activity == "4":
                print(EducationAdministrator.see_one_student())
        except:
            print("\nWRONG INPUT...\n")
