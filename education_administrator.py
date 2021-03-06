from user import User, major_courses
from course import dump_course_file, is_course_exist, get_course_info
from student import Student, print_students
import json
import logging


class EducationAdministrator(User):
    def __init__(self, user_name, password, major):
        super().__init__(user_name, password, major, 'admin')

    @staticmethod
    def sign_in(user_data, course_data, user):
        admin = EducationAdministrator(user.user_name, user.password, user.major)
        for each in user_data:
            if each['role'] == 'admin' and each['user_name'] == user.user_name:
                admin.major = each['major']
                course_data[admin.major] = course_data.get(admin.major, [])
                dump_course_file(course_data)
                User.my_logger.info(f"{admin.user_name} signed in.")
                return admin

    @staticmethod
    def create_course(course_data, type_of_course):
        """
        this static method, adds a course
        """
        course = get_course_info(course_data, type_of_course)

        # to check that user wants to quit or not
        # get_course_info(course_data, major) returns None if user want to quit.
        if course:
            info = course.__dict__
            info.pop("major")

            course_data.get(type_of_course, []).append(info)

            dump_course_file(course_data)

            User.my_logger.info(f"{info['name']} created.")
            return course
        return False

    @staticmethod
    def delete_course(user_data, course_data, type_of_course):
        """
        this static method, delete a course
        """
        course_code = is_course_exist(course_data, type_of_course)
        if course_code:
            for course in course_data[type_of_course]:
                if course['code'] == course_code:
                    EducationAdministrator.delete_course_for_students(user_data, course_data, type_of_course, course)
                    course_data[type_of_course].remove(course)
                    dump_course_file(course_data)
                    User.my_logger.info(f"{course['name']} deleted.")
                    return course
        return False

    @staticmethod
    def delete_course_for_students(user_data, course_data, type_of_course, course):
        """
        this method delete a course from students` profiles, if admin want to delete that course
        """
        for _, student in Student.each_student(user_data, type_of_course):
            if course['code'] in student.all_courses.get(type_of_course, []):
                student.remove_course(user_data, course_data, course, type_of_course)


def admin_which_activity(user_data, course_data, admin):
    end = False
    major = admin.major if admin.major != 'general' else 'all'
    while not end:
        activity = input(f"\nENTER 1 ---> see courses"
                         f"\nENTER 2 ---> create a course"
                         f"\nENTER 3 ---> delete a course"
                         f"\nENTER 4 ---> see a list of {major} students"
                         f"\nENTER 5 ---> choose a student and see it`s courses"
                         f"\nENTER 0 ---> quit\n")
        try:
            assert activity in ['0', '1', '2', '3', '4', '5']
            if activity == "0":
                end = True
            elif activity == "1":
                major_courses(course_data, admin.major)
            elif activity == "2":
                course = EducationAdministrator.create_course(course_data, admin.major)
                if course:
                    print("\ncreating course was successful..\n")
            elif activity == "3":
                course = EducationAdministrator.delete_course(user_data, course_data, admin.major)
                if course:
                    print("\ndeleting course was successful...\n")
            elif activity == "4":
                print_students(user_data, admin.major)
            elif activity == "5":
                see_one_student(user_data, admin.major)
        except AssertionError:
            print("\nWRONG INPUT...\n")

    return False


def see_one_student(user_data, major):
    """
    this function finds a student and confirm/not confirm it`s taking courses
    """
    if not Student.any_student(user_data, major):
        print("\nthere is no student in your major...\n")
        return True

    else:
        student_username = input("\nplease enter username of student: ")
        student = Student.find_student(user_data, student_username)

        if student:
            print(student)
            while True:
                choice = input("\nENTER 1 ---> confirm it`s courses"
                               "\nENTER 2 ---> not confirm it`s courses"
                               "\nENTER 0 ---> back\n")
                try:
                    assert choice in ['0', '1', '2']
                    if choice == '0':
                        return True
                    elif choice == '1':
                        student.confirm_courses(user_data, True)
                        return True
                    elif choice == '2':
                        student.confirm_courses(user_data, False)
                        return True
                except AssertionError:
                    print("\nWRONG INPUT...\n")

        print("\nthere is no student with this username...\n")
        return True

