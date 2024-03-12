from flask import Blueprint, render_template, request, redirect, url_for
from lib.helper import render_result, render_err_result, course_data_path, user_data_path
from model.course import Course
from model.user import User
from model.user_admin import Admin
from model.user_instructor import Instructor
from model.user_student import Student

user_page = Blueprint("user_page", __name__)

model_user = User()
model_course = Course()
model_student = Student()


def generate_user(login_user_str):
    login_user = None  # a User object
    if login_user_str.split(";;;")[4] == "admin":
        login_user = Admin(int(login_user_str.split(";;;")[0]), login_user_str.split(";;;")[1],
                           login_user_str.split(";;;")[2], login_user_str.split(";;;")[3],
                           login_user_str.split(";;;")[4])
    elif login_user_str.split(";;;")[4] == "instructor":
        login_user = Instructor(int(login_user_str.split(";;;")[0]), login_user_str.split(";;;")[1],
                                login_user_str.split(";;;")[2], login_user_str.split(";;;")[3],
                                login_user_str.split(";;;")[4], login_user_str.split(";;;")[5],
                                login_user_str.split(";;;")[6], login_user_str.split(";;;")[7],
                                login_user_str.split(";;;")[8].split("--"))
    elif login_user_str.split(";;;")[4] == "student":
        login_user = Student(int(login_user_str.split(";;;")[0]), login_user_str.split(";;;")[1],
                             login_user_str.split(";;;")[2], login_user_str.split(";;;")[3],
                             login_user_str.split(";;;")[4], login_user_str.split(";;;")[5])

    return login_user


@user_page.route("/login")
def login():
    return render_template("00login.html")


@user_page.route("/login", methods=['POST'])
def login_post():
    req = request.values
    username = req["username"] if "username" in req else "null"
    password = req["password"] if "password" in req else "null"
    if User.validate_username(User(), username) and User.validate_password(User(), password):
        (flag, string_ifo) = User.authenticate_user(User(), username, password)
    else:
        (flag, string_ifo) = User.authenticate_user(User(), username, password)
    if flag:
        User.current_login_user = generate_user(string_ifo)


@user_page.route("/logout")
def logout():
    User.current_login_user = None
    return render_template("01index.html")


@user_page.route("/register")
def register():
    return render_template("00register.html")


@user_page.route("/register", methods=['POST'])
def register_post():
    req = request.values
    username = req["username"] if "username" in req else "null"
    password = req["password"] if "password" in req else "null"
    email = req["email"] if "email" in req else "null"
    register_time = req["register_time"] if "register_time" in req else "null"
    role = req["role"] if "role" in req else "null"

    if User.validate_username(User(), username) and User.validate_password(User(), password) \
            and User.validate_email(User(), email):
        flag = User.register_user(User(), username, password, email, register_time, role)
        if not flag:
            return render_err_result(msg="error registering user")


@user_page.route("/student-list")
def student_list():
    if User.current_login_user:  # check login user
        req = request.values
        page = req['page'] if "page" in req else 1
        context = {}
        # get values for one_page_instructor_list, total_pages, total_num
        (one_page_user_list, total_pages, total_num) = User.current_login_user.get_students_by_page(1)

        # get values for page_num_list
        page_num_list = Course.generate_page_num_list(Course(), 1, total_pages)

        # check one_page_instructor_list, make sure this variable not be None, if None, assign it to []
        if one_page_user_list is None:
            one_page_user_list = []

        context['one_page_user_list'] = one_page_user_list
        context['total_pages'] = total_pages
        context['page_num_list'] = page_num_list
        context['current_page'] = int(page)
        context['total_num'] = total_num
        # add "current_user_role" to context
        context['current_user_role'] = User.current_login_user.role

    else:
        return redirect(url_for("index_page.index"))

    return render_template("10student_list.html", **context)


@user_page.route("/student-info")
def student_info():
    req = request.values
    id = req['id'] if "id" in req else 1
    context = {}
    if id == 1:
        context["current_user_role"] = "student"
        return Student()
    else:
        context["current_user_role"] = "student"
        return Student.get_student_by_id(Student(), id)


@user_page.route("/student-delete")
def student_delete():
    req = request.values
    id = req['id'] if "id" in req else 1
    if id != 1:
        Student.delete_student_by_id(Student(), id)
        return redirect(url_for("user_page.student_list"))
    else:
        return redirect(url_for("index_page.index"))
