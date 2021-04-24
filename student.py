from user import User
import json


class Student(User):
    __is_exist = False
    _students = []
    file_of_student = 'students.json'

    def __init__(self, user_name, password, major, credit=0, confirm=False):
        """
        :param user_name: user name of student
        :param password: password of student
        :param major: major of student
        """
        super().__init__(user_name, password, major)
        self.courses = []
        self.__credit = credit
        self.confirm = confirm

    def take_course(self):
        """
        this method check the amount of credit and add a course to student`s courses
        and update the capacity of course
        :return: a message
        """
        # use self.credit = ...
        # log
        # save in file
        return "successfully add..."

    def delete_course(self):
        """
        this method check the amount of credit and delete a course from student`s courses
        and update the capacity of course
        :return: a message
        """
        # use self.credit = ...
        # log
        # save in file
        return "successfully delete..."

    @staticmethod
    def num_students():
        return len(Student._students)

    def major(self, user_name):
        """
        this method, return the major of a student
        :param user_name: user name of student
        :return: major
        """
        with open(Student.file_of_student, 'r') as file:
            students = json.load(file)
            for user, info in students.items():
                if user == user_name:
                    return info[2]

    @property
    def credit(self):
        return self.__credit

    @credit.setter
    def credit(self, add_or_minus_credit):
        if self.__credit + add_or_minus_credit >= 0:
            self.__credit += add_or_minus_credit

    def show_student_courses(self):
        """
        this method, shows the student`s courses and sum of credits
        :return: list of chosen courses and sum of their credit
        """
        return self.courses, self.credit

    @staticmethod
    def sign_in():
        if Student.__is_exist:
            return super().sign_in(Student.file_of_student)
        else:
            print(f"\nthere is no student, you have to sign-in....\n")
            return False

    @classmethod
    def sign_up(cls):
        """
        this is sign up function for students
        :return: a string
        """
        user_name, password = User.user_info()
        while True:
            again_pass = input("please enter password again(if you want to back, enter back): ")
            if again_pass != 'back':
                return f"\nsigning up canceled...\n"
            elif again_pass != password:
                print("that is wrong... please try again...")
                continue
            break

        major = input("\nwhat is your major? ")
        # log
        new_student = Student(user_name, password, major)
        Student._students.append(new_student)
        new_student = {new_student.user_name: [new_student.password, new_student.major]}
        with open(Student.file_of_student, 'a') as write_file:
            json.dump(new_student, write_file)

        return "\nsigning up was successful..\n"

    def see_student_courses(self):
        """
        this method, show the student`s courses
        :return: list
        """
        return "self.courses"

    @staticmethod
    def students():
        """
        this method yield a list of students
        :return:
        """
        with open(Student.file_of_student, 'r') as file:
            students = json.load(file)
            for user in students.keys():
                yield user

    @staticmethod
    def find_a_student(user_name):
        """
        this method, find a student with it`s user name
        :param user_name: student user name
        :return: a message or info of student
        """
        with open(Student.file_of_student, 'r') as file:
            students = json.load(file)
            for user, info in students.items():
                if user == user_name:
                    # return the courses of student
                    return info[3]
            return f"there is no {user_name}"

    def confirm_courses(self):
        """
        this function, call by administrator to confirm or edit courses of a student
        :return: a meeage
        """
        return "take courses confirmed"

    def confirm(self):
        self.confirm = True
        # file
        # log
