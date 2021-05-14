from user import User, dump_user_file, print_courses
from course import Course, dump_course_file, is_course_exist
import logging


class Student(User):
    file_of_student = 'students.json'

    def __init__(self, user_name, password, major,
                 all_courses={}, credit=0, is_confirm=True, role=None, is_blocked=None):
        """
        """
        super().__init__(user_name, password, major, role='student')
        self.all_courses = all_courses if all_courses.keys() else {'general': [], major: []}
        self.credit = int(credit)
        self.is_confirm = is_confirm

    @staticmethod
    def sign_up(user_data, course_data, my_logger):
        """
        this is sign up function for students
        :return: if signing up is successful, it returns an instance of Student class
        """
        user = User.sign_up(user_data, course_data, my_logger)
        if isinstance(user, User):
            new_student = Student(user.user_name, user.password, user.major)
            info = new_student.__dict__

            user_data.append(info)
            dump_user_file(user_data)
            User.my_logger.info(f"{new_student.user_name} signed up.")
            return new_student

        message = user
        return message

    @staticmethod
    def sign_in(user_data, user):
        """
        this method is an override of sign in method in user class
        and make a new student object and return it
        """
        student = Student(user.user_name, user.password, user.major)
        for each in user_data:
            if each['role'] == student.role and each['user_name'] == user.user_name:
                student.major = each['major']
                student.all_courses = each['all_courses']
                student.is_confirm = each['is_confirm']
                student.credit = each['credit']
                User.my_logger.info(f"{student.user_name} signed in.")
                return student

    def take_course(self, user_data, course_data, course, type_course):
        """
        this method checks the amount of credit, add a course to student`s courses
        and update the capacity of course
        """
        if (self.credit + course['credit']) <= 20:
            self.credit += course['credit']
            self.all_courses[type_course].append(course['code'])
            course['remaining_capacity'] -= 1

            for each in user_data:
                if each['role'] == 'student' and each['user_name'] == self.user_name:
                    each['credit'] = self.credit
                    each['all_courses'] = self.all_courses
                    break
            dump_user_file(user_data)
            dump_course_file(course_data)
            User.my_logger.info(f"{self.user_name} took {course['name']}.")
            return True

        return False

    def remove_course(self, user_data, course_data, course, type_course):
        """
        this method checks the amount of credit, delete a course from student`s courses
        and update the capacity of course
        """
        self.all_courses[type_course].remove(course['code'])
        self.credit -= course['credit']

        course['remaining_capacity'] += 1

        for each in user_data:
            if each['role'] == 'student' and each['user_name'] == self.user_name:
                each['credit'] = self.credit
                each['all_courses'] = self.all_courses
                each['is_confirm'] = self.is_confirm
                break

        dump_course_file(course_data)
        dump_user_file(user_data)
        User.my_logger.info(f"{self.user_name} removed {course['name']}.")
        return True

    def courses(self, course_data, type_course):
        """
        this method yields all courses that a student have taken
        """
        course_num = 1
        for each in course_data.get(type_course, []):
            if each['code'] in self.all_courses[type_course]:
                course = Course(type_course, **each)
                yield course_num, course
                course_num += 1


    @property
    def get_credit(self):
        """
        this decorator, return amount of a student`s credit
        """
        return self.credit

    @staticmethod
    def each_student(user_data, major):
        """
        this static method, yield each student in major
        """
        student_num = 1
        if major == 'general':
            for each in user_data:
                if each['role'] == 'student':
                    student = Student(**each)
                    yield student_num, student
                    student_num += 1
        else:
            for each in user_data:
                if each['role'] == 'student' and each['major'] == major:
                    student = Student(**each)
                    yield student_num, student
                    student_num += 1

    def __str__(self):
        return f"user name: {self.user_name}" \
               f"\ncourses: {self.all_courses}" \
               f"\namount of credit: {self.get_credit}" \
               f"\nconfirmation student: {self.is_confirm}"

    @staticmethod
    def find_student(user_data, user_name):
        """
        this method, find a student with it`s user name
        and return it
        """
        for each in user_data:
            if each['role'] == 'student' and each['user_name'] == user_name:
                student = Student(**each)
                return student
        return False

    def confirm_courses(self, user_data, status):

        """
        this function, call by administrator to confirm or not confirm a student`s taking courses
        """
        self.is_confirm = status
        for each in user_data:
            if each['role'] == self.role and each['user_name'] == self.user_name:
                each['is_confirm'] = self.is_confirm

        dump_user_file(user_data)
        User.my_logger.info(f"{self.user_name} not confirmed.")
        return True


def student_which_activity(user_data, course_data, student):
    end = False
    while not end:
        activity = input(f"\nENTER 1 ---> see courses"
                         f"\nENTER 2 ---> take a course"
                         f"\nENTER 3 ---> remove a course"
                         f"\nENTER 4 ---> see your courses"
                         f"\nENTER 5 ---> see number of your credits"
                         f"\nENTER 0 ---> quit\n")
        try:
            assert activity in ['0', '1', '2', '3', '4', '5']
            if activity == "0":
                end = True
            elif activity == "1":
                if not see_all_courses(course_data, student):
                    return False
            elif activity == "2":
                return take_course(user_data, course_data, student)
            elif activity == "3":
                return remove_course(user_data, course_data, student)
            elif activity == "4":
                if not student_courses(course_data, student):
                    return False
            elif activity == "5":
                print(f"the amount of your credit = {student.get_credit}")
        except AssertionError:
            print("\nWRONG INPUT...\n")

    return False


def which_type_of_course(student):
    type = input(f"\nENTER 1 ---> general course"
                 f"\nENTER 2 ---> {student.major} course"
                 f"\nENTER 0 ---> quit\n")
    try:
        assert type in ['0', '1', '2']
        if type == '0':
            return False
        elif type == '1':
            return 'general'
        elif type == '2':
            return student.major
    except AssertionError:
        print("\nWRONG INPUT...\n")


def take_course(user_data, course_data, student):
    """
    this function gets inputs that take course method need.
    """
    type_of_course = which_type_of_course(student)
    if not type_of_course:
        return False

    if course_data.get(type_of_course, []):
        course_code = is_course_exist(course_data, type_of_course)
        if not course_code:
            print("\ntaking course was canceled...\n")
            return

        course_codes = student.all_courses.get(type_of_course, [])
        if course_code not in course_codes:
            for course in course_data[type_of_course]:
                if course_code == course['code']:
                    if not course['remaining_capacity']:
                        print("\nthere is no capacity for this course...\n")
                        return
                    break
            # call a instance method of student class(self.take_course)
            # to add the course in the courses list of a student
            if student.take_course(user_data, course_data, course, type_of_course):
                print("\ntaking course was successful...\n")
                return

            print(f"you can`t get this course... you can have just 20 credits...")
            return

        print("\nyou already have this course...\n")
        return

    print("\nthere is no course to be taken...\n")
    return


def remove_course(user_data, course_data, student):
    type_of_course = which_type_of_course(student)
    if not type_of_course:
        return False

    course_codes = student.all_courses[type_of_course]

    if course_codes:
        course_code = is_course_exist(course_data, type_of_course)
        if not course_code:
            print("\nremoving course was canceled...\n")
            return

        if course_code not in course_codes:
            print("\nyou already don`t have this course...\n")
            return

        for course in course_data[type_of_course]:
            if course['code'] == course_code:
                break

        if student.credit < 11:
            print(f"\nNote: you have just {student.credit} credits..."
                  f"if you remove this course, you will have {student.credit - course['credit']} left...\n")
            end = False
            while not end:
                choice = input(f"are you sure?"
                               f"\nENTER 1 ---> remove"
                               f"\nENTER 0 ---> cancel\n")
                try:
                    assert choice in ['0', '1']
                    if choice == '0':
                        print("\nremoving was canceled...\n")
                        return
                    elif choice == '1':
                        end = True
                except AssertionError:
                    print("\nWRONG INPUT...\n")

        student.remove_course(user_data, course_data, course, type_of_course)
        print("\nremoving was successful...\n")
        return

    print("\nyou have no courses...\n")
    return


def student_courses(course_data, student):
    """
    this method declares the type of courses that student wants to see
    call an instance method: courses; it yield each course that student have taken
    then print each course
    """
    type_of_course = which_type_of_course(student)
    if not type_of_course:
        return False
    if student.all_courses[type_of_course]:
        for course_num, course in student.courses(course_data, type_of_course):
            print(f"course {course_num}:")
            print(course)
    else:
        print(f"\nyou don`t have any {type_of_course} course...\n")
        return True


def see_all_courses(course_data, student):
    type_of_course = which_type_of_course(student)
    if not type_of_course:
        return False
    print_courses(course_data, type_of_course)
    return True


def print_students(user_data, major):
    """
    this function prints all major`s students
    """
    for student_num, student in Student.each_student(user_data, major):
        if not student:
            # it means there is no student for this major...
            print("\nthere is no student in your major...\n")
            return
        print(f"student {student_num}:")
        print(student)


# if __name__ == "__main__":
#     course_data = load_course_file()
#     print_courses(course_data, 'computer')
#     # student = Student.sign_in()
#     # Course.show_courses(student.major)
#     # student.take_course()
#     # student.remove_course()
#     # student.all_courses()
#     student = Student.sign_up()
