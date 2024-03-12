from model.user import User
from lib.helper import user_data_path


class Student(User):
    def __init__(self, uid=-1, username="", password="", register_time="yyyy-MM-dd_HH:mm:ss.SSS", role="student",
                 email=""):
        """
        This is the default constructor
        """
        super().__init__(uid, username, password, register_time, role)
        self.email = email

    def __str__(self):
        """
        This method returns the string representation of the object.

        Returns
        -------
        a String of the format “uid;;;username;;;password;;;register_time;;;role;;;email”
        """
        return "{};;;{};;;{};;;{};;;{};;;{}".format(self.uid, self.username, self.password,
                                                    self.register_time, self.role, self.email)

    def get_students_by_page(self, page):
        """
        This method reads the user.txt file to retrieve all the student information.
        With all the student information and the current page number, a list of Student objects
        and the total pages will be generated. Each page has at most 20 students.

        Parameters
        ----------
        page: an int representing the page number

        Returns
        -------
        A tuple contains the list of students, total page number and the total number of students.
        """
        total_students = 0
        total_pages = 0
        student_info_list = []
        student_object_list = []
        try:
            with open(user_data_path, "r") as fuser:
                for each_line in fuser:
                    if each_line.strip().split(";;;")[4].lower() == "student":
                        total_students = total_students + 1
                        student_info_list.append(each_line.strip())
        except FileNotFoundError:
            print("user.txt file not found.")
            print("cwd might be changed or the file doesnt exist")
        except:
            print("Error reading from user.txt file")
        if total_students % 20 == 0:
            total_pages = int(total_students / 20)
        else:
            total_pages = 1 + int(total_students / 20)
        try:
            for i in range((page - 1) * 20, page * 20):
                if i < len(student_info_list):
                    student_info = student_info_list[i].split(";;;")
                    student_object_list.append(Student(int(student_info[0]), student_info[1],
                                                       student_info[2], student_info[3],
                                                       student_info[4], student_info[5]))
                else:
                    break
        except:
            print("Error in creating instructor object")
        return (student_object_list, total_pages, total_students)

    def get_student_by_id(self, id):
        """
        This method returns a student object by retrieving the id from the user.txt file.

        Parameters
        ----------
        id: an int representing the student id

        Returns
        -------
        a Student object
        """
        try:
            with open(user_data_path, "r") as fuser:
                for each_line in fuser:
                    user_info = each_line.split(";;;")
                    if user_info[0] == str(id) and user_info[4].lower() == "student":
                        return Student(int(user_info[0]), user_info[1], user_info[2], user_info[3],
                                       user_info[4], user_info[5])
        except FileNotFoundError:
            print("user.txt file not found.")
            print("cwd might be changed or the file doesnt exist")
        except:
            print("Error reading from user.txt file")

    def delete_student_by_id(self, id):
        """
        This method deletes a student item from the user.txt file based on the given id.

        Parameters
        ----------
        id: an int representing the student id
        """
        try:
            with open(user_data_path, "r") as fuser:
                lines = fuser.readlines()
        except FileNotFoundError:
            print("user.txt file not found.")
            print("cwd might be changed or the file doesnt exist")
        except:
            print("Error reading from user.txt file")
        try:
            with open(user_data_path, "w") as fuser:
                for each_line in lines:
                    if not each_line.strip().split(";;;")[0] == str(id):
                        fuser.write("{}".format(each_line))
        except FileNotFoundError:
            print("user.txt file not found.")
            print("cwd might be changed or the file doesnt exist")
        except:
            print("Error writing to user.txt file")
