class Course:
    _courses = []
    _major_courses = dict()
    _teacher_courses = dict()

    def __init__(self, major, name, teacher, credit, capacity):
        """
        :param major: major of course
        :param name: name of course
        :param teacher: the teacher who will teach the course
        :param credit: credit of course
        :param capacity: the number of students who can choose the course
        """
        self.major = major
        self.name = name
        self.teacher = teacher
        self.credit = credit
        self.capacity = capacity

    @classmethod
    def create_course(cls):
        """
        this class method, add a course
        :return: message
        """
        # log
        # save in file
        return "successfully add..."

    @classmethod
    def delete_course(cls):
        """
        this class method, delete a course
        :return: message
        """
        # log
        # save in file
        return "successfully delete..."

    @staticmethod
    def list_of_courses(base=None):
        """
        :param base: it can be major, teacher or none(if base=none, this method return a list of all courses)
        :return: a list of courses based on "base"
        """
        return "Course._courses"
