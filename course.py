import json
import logging


class Course:
    def __init__(self, major, name, professor, credit, total_capacity, remaining_capacity, code):
        """
        :param major: major of course
        :param name: name of course
        :param professor: the professor who will teach the course
        :param credit: credit of course
        :param total_capacity: total capacity of course(the number of students who can choose the course)
        :param remaining_capacity: remaining capacity
        """
        self.major = major
        self.name = name
        self.professor = professor
        self.credit = int(credit)
        self.total_capacity = int(total_capacity)
        self.remaining_capacity = int(remaining_capacity)
        self.code = code

    def __str__(self):
        return f"name: {self.name}" \
               f"\ncode: {self.code}" \
               f"\ncredit: {self.credit}" \
               f"\ntotal capacity: {self.total_capacity}" \
               f"\nremaining capacity: {self.remaining_capacity}" \
               f"\nthe professor who teaches this course: {self.professor}"

    @staticmethod
    def each_course(course_data, major):
        """
        this method,yields each course of a major
        """
        course_num = 1
        for each in course_data[major]:
            course = Course(major, **each)
            yield course_num, course
            course_num += 1


def load_course_file():
    with open('course.json', 'r+') as file:
        data = json.load(file)
        return data


def dump_course_file(course_data):
    with open('course.json', 'w') as file:
        file.seek(0)
        json.dump(course_data, file, indent=8)
        file.truncate()


def is_course_exist(course_data, type_of_course):
    """
    this method gets a course code and find it in the list of courses
    """
    course_codes = [course['code'] for course in course_data.get(type_of_course, [])]

    course_code = input('please enter the code of course: ')
    while course_code not in course_codes:
        print(f"there is no course with this code.")
        course_code = input("please enter another code(or enter 'back' to back to menu): ")
        if course_code == "back":
            return False
    return course_code


def get_course_info(course_data, type_of_course):
    """
    this method gets the info of course from admin
    """
    course_names = [course['name'] for course in course_data.get(type_of_course, [])]
    course_codes = [course['code'] for course in course_data.get(type_of_course, [])]

    course_name = input('please enter the name of course: ')
    while course_name in course_names:
        print(f"there is another course with this name.")
        course_name = input("please enter another name(or enter 'back' to back to menu): ")
        if course_name == "back":
            return None

    course_code = input('please enter the code of course: ')
    while course_code in course_codes:
        print(f"there is another course with this code.")
        course_code = input("please enter another code(or enter 'back' to back to menu): ")
        if course_code == "back":
            return None

    professor = input("please enter the name of the professor who is teaching this course: ")
    credit = input("how many credits is this course? ")
    capacity = input("how many people does this course have capacity for? ")

    course = Course(type_of_course, course_name, professor, credit, capacity, capacity, course_code)
    return course

