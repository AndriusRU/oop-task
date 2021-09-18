class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_course(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer):
            if course in lecturer.courses_attached:
                if 0 <= grade <= 10:
                    if course in lecturer.grades:
                        lecturer.grades[course] += [grade]
                    else:
                        lecturer.grades[course] = [grade]
                else:
                    print('Ошибка - оценка должна быть от 0 до 10')
                    return
            else:
                print('Ошибка - нет курса у лектора')
                return
        else:
            print('Ошибка - это не лектор!!!')
            return

    def avg_grade(self):
        count = 0
        summary = 0
        for key, items in self.grades.items():
            count += len(items)
            for item in items:
                summary += item
        return (summary / count) if count else 0

    def __str__(self):
        return f'Имя: {self.name}\n' \
               f'Фамилия: {self.surname}\n' \
               f'Средняя оценка за домашние задания: {self.avg_grade()}\n' \
               f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n' \
               f'Завершенные курсы: {", ".join(self.finished_courses)}\n' \


    def __lt__(self, other):
        if not isinstance(other, Student):
            print('Вы сравниваете не со студентом !!!')
            return
        return self.avg_grade() < other.avg_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    # def avg_grade(self):
    #     count = 0
    #     summary = 0
    #     for key, items in self.grades.items():
    #         count += len(items)
    #         for item in items:
    #             summary += item
    #     return summary / count

    # Используем тот же метод для подсчета средней оценки, что и у Student
    # в данной задаче нет на то ограничений. Нет нужды писать точно такую же функцию.
    # f'Средняя оценка за домашние задания: {Student.avg_grade(self)}\n' \

    def __str__(self):
        return f'Имя: {self.name}\n' \
               f'Фамилия: {self.surname}\n' \
               f'Средняя оценка за лекции: {Student.avg_grade(self)}\n'

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            print('вы сравниваете не с лектором !!!')
            return
        return Student.avg_grade(self) < Student.avg_grade(other)


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            print(f'{self.surname} {self.name} не являешься проверяющим по курсу {course}!!!')
            return 'Ошибка'

    def __str__(self):
        return f'Имя: {self.name}\n' \
               f'Фамилия: {self.surname}\n'


def avg_grade_hw_course(list_students: list, course: str) -> float:
    summary = 0
    count = 0
    for student in list_students:
        if isinstance(student, Student) and course in student.courses_in_progress:
            if student.grades.get(course) is not None:
                count += len(student.grades[course])
                for grade in student.grades[course]:
                    summary += grade
            else:
                continue
        else:
            print(f'{student.surname} {student.name} - не является студентом или не изучает(ал) курс {course}')
    return (summary / count) if count else 0


def avg_grade_lecture(list_lecturers: list, course: str) -> float:
    summary = 0
    count = 0
    for lecturer in list_lecturers:
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached:
            if lecturer.grades.get(course) is not None:
                count += len(lecturer.grades[course])
                for grade in lecturer.grades[course]:
                    summary += grade
            else:
                continue
        else:
            print(f'{lecturer.surname} {lecturer.name} - не читает(ал) курс по {course}')
    return (summary / count) if count else 0


student_1 = Student('Roy', 'Eman', 'your_gender')
student_1.courses_in_progress += ['Python']
student_1.courses_in_progress += ['Git']

student_2 = Student('Ivan', 'Ivanov', 'male')
student_2.courses_in_progress += ['Python']
student_2.courses_in_progress += ['JAVA']
student_2.courses_in_progress += ['Git']

reviewer_1 = Reviewer('Some', 'Buddy')
reviewer_1.courses_attached += ['Python']
reviewer_1.courses_attached += ['Git']

reviewer_2 = Reviewer('Sam', 'Washington')
reviewer_2.courses_attached += ['JAVA']

lecturer_1 = Lecturer('Ivan', 'Ivanov')
lecturer_1.courses_attached += ['JAVA']
lecturer_1.courses_attached += ['Python']

lecturer_2 = Lecturer('Ivan', 'Ivanov')
lecturer_2.courses_attached += ['Git']

reviewer_1.rate_hw(student_1, 'Python', 10)
reviewer_1.rate_hw(student_1, 'Python', 9)
reviewer_1.rate_hw(student_1, 'Python', 8)

reviewer_1.rate_hw(student_2, 'Python', 7)
reviewer_1.rate_hw(student_2, 'Python', 9)
reviewer_1.rate_hw(student_2, 'Python', 8)

reviewer_1.rate_hw(student_1, 'Git', 10)
reviewer_1.rate_hw(student_1, 'Git', 7)
reviewer_1.rate_hw(student_1, 'Git', 8)

reviewer_2.rate_hw(student_2, 'JAVA', 10)
reviewer_2.rate_hw(student_2, 'JAVA', 10)
reviewer_2.rate_hw(student_2, 'JAVA', 8)

student_1.rate_course(lecturer_1, 'JAVA', 1)
student_2.rate_course(lecturer_1, 'JAVA', 10)
student_1.rate_course(lecturer_1, 'Python', 9)
student_2.rate_course(lecturer_1, 'Python', 10)
student_1.rate_course(lecturer_2, 'Git', 8)

print(student_1)
print(reviewer_1)
print(lecturer_1)

print(student_2 > student_1)
print(lecturer_1 > lecturer_2)

list_students = [student_1, student_2]
list_lecturer = [lecturer_1, lecturer_2]
course = 'Python'
print(f'Средняя оценка по ДЗ  курс {course} - {avg_grade_hw_course(list_students, course)}')
print(f'Средняя оценка за курс {course } - {avg_grade_lecture(list_lecturer, course)}')
course = 'Git'
print(f'Средняя оценка по ДЗ  курс {course} - {avg_grade_hw_course(list_students, course)}')
print(f'Средняя оценка за курс {course } - {avg_grade_lecture(list_lecturer, course)}')
course = 'JAVA'
print(f'Средняя оценка по ДЗ  курс {course} - {avg_grade_hw_course(list_students, course)}')
print(f'Средняя оценка за курс {course } - {avg_grade_lecture(list_lecturer, course)}')


# Показ ошибочных данных
reviewer_1.rate_hw(student_1, 'JAVA', 8)
