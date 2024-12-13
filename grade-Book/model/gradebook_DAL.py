import json
from werkzeug.security import generate_password_hash

#jane.doe password123

def setup_db():
    data = {
        "Courses": {
            "Computer Science": {
                "Assignments": {
                    "Formative": {
                        "Homework 1": 75,
                        "Quiz 1": 85,
                        "Homework 2": 95
                    },
                    "Summative": {
                        "Test 1": 90,
                        "Project 1": 100
                    },
                    "Final Exam": 99
                },
                "isAP": True,
                "Average": 95
            }
        },
        "Numeric GPA": 93.25,
        "Unweighted GPA": 3.75,
        "Weighted GPA": 3.8
    }
    f = open('database/gradebook_database.json', 'w')
    json.dump(data, f)
    f.close()


def write_to_db(data):
    f = open('database/gradebook_database.json', 'w')
    json.dump(data, f)
    f.close()


def get_db_as_dict():
    f = open('database/gradebook_database.json', 'r')
    data = json.load(f)
    f.close()
    return data


def get_all_courses(user):
    data = get_db_as_dict()
    return list(data[user]['Courses'])


def get_course(course, user):
    data = get_db_as_dict()
    return data[user]['Courses'][course]


def add_assignment(user, course, category, name, grade):
    data = get_db_as_dict()
    data[user]['Courses'][course]['Assignments'][category][name] = grade
    write_to_db(data)

    adjust_grades(user, course)


def remove_assignment(user, course, category, name):
    try:
        data = get_db_as_dict()
        del data[user]['Courses'][course]['Assignments'][category][name]
        write_to_db(data)

        adjust_grades(user, course)
    except KeyError:
        return False


def set_final_exam(user, course, grade):
    data = get_db_as_dict()
    data[user]['Courses'][course]['Assignments']['Final Exam'] = grade
    write_to_db(data)

    adjust_grades(user, course)


def get_final_exam(user, course):
    data = get_db_as_dict()
    return data[user]['Courses'][course]['Assignments']['Final Exam']


def set_course_average(user, course):
    avg_form = get_category_average(user, course, 'Formative')
    avg_sum = get_category_average(user, course, 'Summative')
    final_exam = get_final_exam(user, course)
    avg = round(avg_form * .3 + avg_sum * .5 + final_exam * .2, 2)

    data = get_db_as_dict()
    data[user]['Courses'][course]['Average'] = avg
    write_to_db(data)


def get_category_average(user, course, category):
    data = get_db_as_dict()
    course_data = data[user]['Courses'][course]['Assignments'][category]
    average = 0
    for key in course_data:
        average += int(course_data[key])
    average /= len(course_data)
    return average


def get_course_average(user, course):
    data = get_db_as_dict()
    return data[user]['Courses'][course]['Average']


def get_letter_grade(user, course):
    avg = get_course_average(user, course)
    if avg >= 90:
        return 'A'
    elif avg >= 80:
        return 'B'
    elif avg > 70:
        return 'C'
    elif avg == 70:
        return 'D'
    else:
        return 'F'


def get_course_qp(user, course, isAP=False):
    qp = 0
    avg = round(get_course_average(user, course))
    if avg >= 90:
        qp = 4
    elif avg >= 80:
        qp = 3
    elif avg > 70:
        qp = 2
    elif avg == 70:
        qp = 1

    if isAP and qp > 0:
        qp += 1
    return qp


def set_numeric_gpa(user):
    data = get_db_as_dict()
    total = 0
    for course in data[user]['Courses']:
        total += data[user]['Courses'][course]['Average']
    data['Numeric GPA'] = round(total / len(data[user]['Courses']), 2)
    write_to_db(data)


def get_numeric_gpa(user):
    data = get_db_as_dict()
    return data[user]['Numeric GPA']


def set_unweighted_gpa(user):
    data = get_db_as_dict()
    total_gp = 0
    for course in data[user]['Courses']:
        total_gp += get_course_qp(user, course)
    unweighted_gpa = round(total_gp / len(data[user]['Courses']), 2)
    data[user]['Unweighted GPA'] = unweighted_gpa
    write_to_db(data)


def get_unweighted_gpa(user):
    data = get_db_as_dict()
    return data[user]['Unweighted GPA']


def set_weighted_gpa(user):
    data = get_db_as_dict()
    total_gp = 0
    for course in data[user]['Courses']:
        isAP = data[user]['Courses'][course]["isAP"]
        total_gp += get_course_qp(user, course, isAP)
    weighted_gpa = round(total_gp / len(data[user]['Courses']), 2)
    data[user]['Weighted GPA'] = weighted_gpa
    write_to_db(data)


def get_weighted_gpa(user):
    data = get_db_as_dict()
    return data[user]['Weighted GPA']


def adjust_grades(user, course):
    set_course_average(user, course)
    set_numeric_gpa(user)
    set_unweighted_gpa(user)
    set_weighted_gpa(user)


def get_all_users_as_list():
    data = get_db_as_dict()
    return data.keys()


def get_user_hashed_password(user):
    data = get_db_as_dict()
    return data[user]["Hashed Password"]


def get_user_full_name(user):
    data = get_db_as_dict()
    return data[user]["First Name"] + " " + data[user]["Last Name"]


def add_hashed_password(user, password):
    data = get_db_as_dict()
    hashed_password = generate_password_hash(password)
    data[user]["Hashed Password"] = hashed_password
    write_to_db(data)


add_hashed_password('doe.jane', 'password123')
