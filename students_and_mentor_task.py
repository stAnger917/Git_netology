
class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def average_student_rating(self, grades):
        all_grades = (list(grades.values()))
        counter = 0
        pre_result = 0
        for j in all_grades:
            counter += len(j)
        for i in range(len(all_grades)):
            pre_result += sum(all_grades[i])
        if counter !=0 and pre_result !=0:
            average_rating_result = round((pre_result / counter), 2)
        else:
            average_rating_result = 0           
        return average_rating_result

    def rate_lecturer(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if grade in range(1, 11):
                if course in lecturer.grade:
                    lecturer.grade[course] += [grade]
                    
                else:
                    lecturer.grade[course] = [grade]
            else:
                print("Grade must be in range 1 - 11")
    
    def __lt__(self, other):
        return self.average_student_rating(self.grades) > other.average_student_rating(other.grades)
    
    def __str__(self):
        present_courses = ', '.join(self.courses_in_progress)
        return f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за домашние задания: {self.average_student_rating(self.grades)}\nКурсы в процессе изучения: {present_courses}\nЗавершенные курсы: Введение в программирование'


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        Mentor.__init__(self, name, surname)
        self.courses_attached = []
        self.grade = {}

    def average_lector_rating(self, grade):
        all_grades = (list(grade.values()))
        counter = 0
        pre_result = 0
        for j in all_grades:
            counter += len(j)
        for i in range(len(all_grades)):
            pre_result += sum(all_grades[i])
        if counter != 0 and pre_result != 0:
            average_rating_result = round((pre_result / counter), 2)         
            return average_rating_result
        else:
            return 0

    def __lt__(self, other):
        return self.average_lector_rating(self.grade) > other.average_lector_rating(other.grade)      

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self.average_lector_rating(self.grade)}'


class Reviewer(Mentor):
    def __init__(self, name, surname):
        Mentor.__init__(self, name, surname)
        self.courses_attached = []

    def rate_by_reviewer(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'
    
    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'


test_student_1 = Student('Ruoy', 'Eman', 'male')
test_student_1.courses_in_progress += ['Python']
test_student_1.courses_in_progress += ['Go']

test_student_2 = Student('Harry', 'Potter', 'male')
test_student_2.courses_in_progress += ['Go']

test_lector_1 = Lecturer('John', 'Sheppard')
test_lector_1.courses_attached += ['Python']
test_lector_1.courses_attached += ['Go']

test_lector_2 = Lecturer('Hannibal', 'Lector')
test_lector_2.courses_attached += ['Python']

test_rewiever_1 = Reviewer('Jack', 'Daniels')
test_rewiever_1.courses_attached += ['Python']
test_rewiever_1.courses_attached += ['Go']

test_rewiever_2 = Reviewer('William', 'Lawson')
test_rewiever_2.courses_attached += ['Python']

test_student_1.rate_lecturer(test_lector_1, 'Python', 9)
test_student_1.rate_lecturer(test_lector_1, 'Go', 10)
test_student_2.rate_lecturer(test_lector_1, 'Go', 7)
test_student_1.rate_lecturer(test_lector_2, 'Python', 10)
test_student_1.rate_lecturer(test_lector_2, 'Python', 2)

test_rewiever_1.rate_by_reviewer(test_student_1, 'Python', 10)
test_rewiever_1.rate_by_reviewer(test_student_2, 'Go', 10)
test_rewiever_1.rate_by_reviewer(test_student_1, 'Go', 7)
test_rewiever_1.rate_by_reviewer(test_student_2, 'Go', 2)

print(test_lector_1)
print(test_student_1)
print(test_rewiever_1)

print(f'Is lecturer {test_lector_1.name} has greater average grade rating than {test_lector_2.name}:', test_lector_1 > test_lector_2)
print(f'Is student {test_student_1.name} has greater average grade rating than {test_student_2.name}:', test_student_1 < test_student_2)

def average_homework_grades_by_course(student_lits, course_name):
    grades_list = []
    counter = 0
    pre_result = 0
    for stud in student_lits:
        if course_name in stud.grades:
            tmp_lst = stud.grades.get(f'{course_name}')
            grades_list.append(tmp_lst)
    for j in grades_list:
        counter += len(j)
    for i in range(len(grades_list)):
        pre_result += sum(grades_list[i])
    if counter !=0 and pre_result !=0:
        result = round((pre_result / counter), 2)           
        return result
    else:
        return 0

std_lst = [test_student_1, test_student_2]

print(average_homework_grades_by_course(std_lst, 'Go'))

def average_lections_grades_by_cousre(lectors_list, course_name):
    grades_list = []
    counter = 0
    pre_result = 0
    for lect in lectors_list:
        if course_name in lect.grade:
            tmp_lst = lect.grade.get(f'{course_name}')
            grades_list.append(tmp_lst)
    for j in grades_list:
        counter += len(j)
    for i in range(len(grades_list)):
        pre_result += sum(grades_list[i])
    if counter !=0 and pre_result !=0:
        result = round((pre_result / counter), 2)           
        return result
    else:
        return 0

lectors_list = [test_lector_1, test_lector_2]

print(average_lections_grades_by_cousre(lectors_list, 'Python'))
