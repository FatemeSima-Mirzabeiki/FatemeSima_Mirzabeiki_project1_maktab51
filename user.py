from course import Course
from hashing import hashing_password
import json


class User:
    def __init__(self, user_name, password, major):
        """
        :param user_name: user`s user name
        :param password: user`s password
        :param major: the major of student or the major of education administrator(every major has an administrator)
        """
        self.user_name = user_name
        self.password = hashing_password(password)
        self.major = major

    def show_courses(self):
        """
        :return: a list of "major" courses
        """
        return "Course.list_of_courses(self.major)"

    @staticmethod
    def exist_users(file_of_users):
        """
        this function yield user names and their passwords
        first, it read the jason file contains user names + passwords
        :return:
        """
        with open(file_of_users, 'r') as file:
            data = json.load(file)
            for user, info_ in data.items():
                yield user, info_(0)

    @staticmethod
    def is_user_authorized(username, password, file_of_users):
        """
        :param username: the user name that user entered
        :param password: the password that user entered
        :return: if the user name and password exists, return true
        """
        return any(user_infos == (username, password) for user_infos in User.exist_users(file_of_users))

    @staticmethod
    def is_user_exists(username, file_of_users):
        """
        this function check an username exists or not
        :param username: the user name that user want to have it
        :return: if an username exist, return true or return false if not exist
        """
        return any((usr_name == username) for usr_name, _ in User.exist_users(file_of_users))

    @staticmethod
    def user_info():
        user_name = input("please enter your UserName: ")
        password = hashing_password(input("please enter your Password: "))
        return user_name, password

    @staticmethod
    def sign_in(file_of_users):
        """
        this is sign-in function
        :return: False, if signing in is failed
        """
        counter = 3
        while counter:
            user_name, password = User.user_info()
            if not User.is_user_exists(user_name, file_of_users):
                print(f"\n{user_name} Unavailable. Please Try Again...\n")
                continue
            if User.is_user_authorized(user_name, password, file_of_users):
                print(f"\nWelcome Back {user_name}...\n")
                # log
                return True
            if User.is_user_exists(user_name, file_of_users):
                if counter == 1:
                    # verification email
                    # calling lock_account
                    print(f"\n...YOUR ACCOUNT LOCKED...\n")
                    return False
                print(f"\nentered Password is wrong..."
                      f"\nyou can {counter - 1} more..."
                      f"\nNOTICE!!! if you enter wrong password for 3 times, your account will lock...\n")
            counter -= 1

