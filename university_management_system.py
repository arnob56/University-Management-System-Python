# ==============================
# UNIVERSITY MANAGEMENT SYSTEM
# Using OOP + Design Patterns
# ==============================

# -------- OBSERVER PATTERN --------
class Observer:
    def update(self, message):
        pass


# -------- STRATEGY PATTERN (GPA) --------
class GPAStrategy:
    def calculate(self, grades):
        pass


class RegularGPA(GPAStrategy):
    def calculate(self, grades):
        if not grades:
            return 0.0
        return sum(grades.values()) / len(grades)


# -------- BASE CLASS --------
class Person:
    def __init__(self, name, person_id, email):
        self.name = name
        self.person_id = person_id
        self.email = email

    def display_info(self):
        print(f"Name: {self.name}, ID: {self.person_id}, Email: {self.email}")


# -------- COURSE (SUBJECT) --------
class Course:
    def __init__(self, code, name, credit):
        self.course_code = code
        self.course_name = name
        self.credit = credit
        self.students = []
        self.observers = []

    def attach(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def notify(self, message):
        for obs in self.observers:
            obs.update(message)

    def add_student(self, student):
        if student not in self.students:
            self.students.append(student)
            self.attach(student)
            self.notify(f"Enrolled in {self.course_name}")

    def remove_student(self, student):
        if student in self.students:
            self.students.remove(student)
            self.notify(f"Dropped from {self.course_name}")

    def view_students(self):
        print(f"Students in {self.course_name}:")
        for s in self.students:
            print(f"- {s.name}")


# -------- STUDENT --------
class Student(Person, Observer):
    def __init__(self, name, student_id, email, gpa_strategy):
        super().__init__(name, student_id, email)
        self.courses = {}
        self.grades = {}
        self.gpa_strategy = gpa_strategy

    def add_course(self, course):
        if course.course_code not in self.courses:
            self.courses[course.course_code] = course
            course.add_student(self)
        else:
            print("Already enrolled in this course")

    def drop_course(self, course_code):
        if course_code in self.courses:
            course = self.courses.pop(course_code)
            course.remove_student(self)
        else:
            print("Course not found")

    def update(self, message):
        print(f"[Notification - {self.name}]: {message}")

    def view_courses(self):
        print(f"{self.name}'s Courses:")
        for c in self.courses.values():
            print(f"- {c.course_name}")

    def view_grades(self):
        print("Grades:")
        for code, grade in self.grades.items():
            print(f"{code}: {grade}")

    def calculate_gpa(self):
        return self.gpa_strategy.calculate(self.grades)


# -------- TEACHER --------
class Teacher(Person):
    def __init__(self, name, teacher_id, email):
        super().__init__(name, teacher_id, email)
        self.courses = []

    def assign_course(self, course):
        self.courses.append(course)

    def assign_grade(self, student, course_code, grade):
        if course_code in student.courses:
            student.grades[course_code] = grade
            student.update(f"Grade {grade} assigned for {course_code}")
        else:
            print("Student not enrolled in this course")

    def view_courses(self):
        print(f"{self.name} teaches:")
        for c in self.courses:
            print(f"- {c.course_name}")


# -------- AUTHORITY (ADMIN) --------
class Authority(Person):
    def create_course(self, code, name, credit):
        return Course(code, name, credit)


# -------- FACTORY PATTERN --------
class UserFactory:
    @staticmethod
    def create_user(role, name, id_, email):
        if role == "student":
            return Student(name, id_, email, RegularGPA())
        elif role == "teacher":
            return Teacher(name, id_, email)
        elif role == "authority":
            return Authority(name, id_, email)
        else:
            raise ValueError("Invalid user role")


# -------- SINGLETON PATTERN --------
class UniversitySystem:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.students = {}
            cls._instance.teachers = {}
            cls._instance.courses = {}
        return cls._instance

    def add_student(self, student):
        self.students[student.person_id] = student

    def remove_student(self, student_id):
        self.students.pop(student_id, None)

    def add_teacher(self, teacher):
        self.teachers[teacher.person_id] = teacher

    def remove_teacher(self, teacher_id):
        self.teachers.pop(teacher_id, None)

    def add_course(self, course):
        self.courses[course.course_code] = course

    def remove_course(self, course_code):
        self.courses.pop(course_code, None)

    def list_students(self):
        print("Students:")
        for s in self.students.values():
            print(f"- {s.name} ({s.person_id})")

    def list_teachers(self):
        print("Teachers:")
        for t in self.teachers.values():
            print(f"- {t.name} ({t.person_id})")

    def list_courses(self):
        print("Courses:")
        for c in self.courses.values():
            print(f"- {c.course_name} ({c.course_code})")


# -------- MAIN EXECUTION --------
if __name__ == "__main__":
    uni = UniversitySystem()
    factory = UserFactory()

    admin = factory.create_user("authority", "Registrar", "A01", "admin@uni.edu")
    student1 = factory.create_user("student", "MS Dhoni", "S01", "msdhoni7@uni.edu")
    teacher1 = factory.create_user("teacher", "Goutam Gambhir", "T01", "gg5@uni.edu")

    uni.add_student(student1)
    uni.add_teacher(teacher1)

    cse101 = admin.create_course("CSE110", "Intro to Programming", 3)
    uni.add_course(cse101)

    teacher1.assign_course(cse101)
    student1.add_course(cse101)

    teacher1.assign_grade(student1, "CSE101", 4.0)

    student1.view_courses()
    student1.view_grades()
    print("GPA:", student1.calculate_gpa())

    cse101.view_students()
    uni.list_students()
    uni.list_courses()
    uni.list_teachers()
