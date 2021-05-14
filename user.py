import hashlib
from course import Course
import json
import logging


class User:
    my_logger = None

    def __init__(self, user_name, password, major, role):
        """
        :param user_name: user`s user name
        :param password: user`s password
        :param major: the major of student or the major of education administrator(every major has an administrator)
        :param role: role of user(student or admin)
        """
        self.user_name = user_name
        self.password = password
        self.major = major
        self.role = role
        self.is_blocked = False

    @staticmethod
    def check_pass(user_data, user_name, password):
        """
        to check that know password is wrong or not.
        """
        counter = 3
        while counter > 0 and not User.is_user_authorized(user_data, user_name, password):
            if counter == 1:
                for each in user_data:
                    if each['user_name'] == user_name:
                        each['is_blocked'] = True
                dump_user_file(user_data)
                User.my_logger.info(f"{user_name} blocked.")
                return "\n...YOUR ACCOUNT LOCKED...\n"
            print(f"\nentered Password is wrong..."
                  f"\nyou can {counter - 1} more..."
                  f"\nNOTICE!!! if you enter wrong password for 3 times,"
                  f" your account will lock...\n")
            password = input("enter your password again (if you want to back, enter 'back'): ")
            password = hashlib.sha256(password.encode("utf8")).hexdigest()
            if password == 'back':
                return "\nsigning in was canceled...\n"
            counter -= 1
        return True

    @staticmethod
    def confirm_pass(password):
        """
        this method, gets user name again to confirm it
        """
        again_pass = input("please enter password again: ")
        again_pass = hashlib.sha256(again_pass.encode("utf8")).hexdigest()
        while again_pass != password:
            again_pass = input("that`s not sync. please try again...(if you want to back, enter 'back'): ")
            if again_pass == hashlib.sha256("back".encode("utf8")).hexdigest():
                return None
            again_pass = hashlib.sha256(again_pass.encode("utf8")).hexdigest()
        return True

    @staticmethod
    def check_username(user_data, user_name):
        """
        to check that the entered user name is exist or not
        """
        end = False
        while not end and User.is_user_exists(user_data, user_name):
            print(f"\nthis user name already exists...\n")
            user_name = input("enter another username (if you want to back, enter 'back'): ")
            if user_name == 'back':
                return None
        return user_name

    @staticmethod
    def sign_up(user_data, course_data, my_logger):
        """
        sign-up method
        this method use for student registration
        """
        user_name, password, major = get_user_info(user_data, course_data, which='sign-up')

        # to check that user wants to quit or not. User.get_user_info() returns None if user want to quit.
        if user_name:
            # to check the user name exists or not
            user_name = User.check_username(user_data, user_name)
            if user_name:
                if User.confirm_pass(password):
                    user = User(user_name, password, major, role=None)
                    User.my_logger = my_logger
                    return user
        return "\nsigning up was canceled...\n"

    @staticmethod
    def sign_in(user_data, my_logger):
        """
        this is sign-in function
        :return: False, if signing in is failed
        """
        user_name, password, = get_user_info(user_data, course_data=None, which='sign-in')

        # to check that user wants to quit or not. User.get_user_info() returns None if user
        # want to quit.
        if user_name:
            role = User.is_user_exists(user_data, user_name)
            if not role:
                return f"\nthere is no {user_name}.\n"

            if User.not_blocked(user_data, user_name):
                """
                if password is not true, this block gets password again and checks it for 3 times.
                """
                is_authorized = User.check_pass(user_data, user_name, password)
                # if is_authorized is a string, it means that account is locked or signing up was canceled
                if isinstance(is_authorized, str):
                    return is_authorized
                user = User(user_name, password, major=None, role=role)
                User.my_logger = my_logger
                return user

            return "\nyour account was blocked...\n"
        return "\nsigning in was canceled...\n"

    @staticmethod
    def is_user_exists(user_data, username):
        """
        this function checks the username exists or not
        if an user name exist, it return user`s role
        """
        for usr in User.all_users(user_data):
            if usr['user_name'] == username:
                return usr['role']
        return False

    @staticmethod
    def not_blocked(user_data, username):
        """
        this method checks the user is a blocked user or not
        :return: returns false if blocked
        """
        return any((usr['user_name'], usr['is_blocked']) == (username, False)
                   for usr in User.all_users(user_data))

    @staticmethod
    def all_users(user_data):
        """
        this function yield user names and their passwords
        """
        for usr in user_data:
            yield usr

    @staticmethod
    def is_user_authorized(user_data, username, password):
        """
        this method checks that user name and password that user entered, are sync or not...
        :return: if the user name and password exists, returns true
        """
        return any((usr['user_name'], usr['password']) == (username, password) for usr in User.all_users(user_data))

    # @staticmethod
    # def change_password(user_name):
    #     while True:
    #         last_password = input("enter your last pass")
    #         with open("users.json", 'r') as file:
    #             data = json.load(file)
    #             for user, info_ in data.items():
    #                 yield user, info_(0)


def load_user_file():
    with open('user.json', 'r+') as file:
        data = json.load(file)
        return data


def dump_user_file(user_data):
    with open('user.json', 'w') as file:
        file.seek(0)
        json.dump(user_data, file, indent=8)
        file.truncate()


def get_user_info(user_data, course_data, which):
    """
    this function gets the info from user
    """
    user_names = [usr['user_name'] for usr in user_data]

    user_name = input("please enter your UserName: ")

    if which == 'sign-in':
        while user_name not in user_names:
            print(f"{user_name} is not exist.")
            user_name = input("please enter another username(or enter 'back' to back to menu): ")
            if user_name == "back":
                return None, None

        password = input("please enter your Password: ")
        password = hashlib.sha256(password.encode("utf8")).hexdigest()

        return user_name, password

    if which == 'sign-up':
        while user_name in user_names:
            print(f"there is another username.")
            user_name = input("please enter another username(or enter 'back' to back to menu): ")
            if user_name == "back":
                return None, None, None
        password = input("please enter your Password: ")
        password = hashlib.sha256(password.encode("utf8")).hexdigest()
        major = input("please enter your major: ")
        majors = []
        for each in user_data:
            if each['role'] == 'admin':
                majors.append(each['major'])

        while major not in majors:
            print(f"there is no major named {major} in this university.")
            major = input("please enter another major(or enter 'back' to back to menu): ")
            if major == "back":
                return None, None, None
        return user_name, password, major


def print_courses(course_data, major):
    """
    this function prints all major`s courses
    """
    majors = list(course_data.keys())
    if major in majors:
        for course_num, course in Course.each_course(course_data, major):
            print(f"course {course_num}:")
            print(course)
    else:
        print("\nthere is no course for this major...\n")
