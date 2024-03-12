import os
import re
import json
import pandas as pd
import matplotlib.pyplot as plt

from model.user import User
from lib.helper import user_data_path


class Instructor(User):
    def __init__(self, uid=-1, username="", password="", register_time="yyyy-MM-dd_HH:mm:ss.SSS", role="instructor",
                 email="", display_name="", job_title="", course_id_list=[]):
        """
        This is the default constructor of the Instructor class
        """
        super().__init__(uid, username, password, register_time, role)
        self.email = email
        self.display_name = display_name
        self.job_title = job_title
        self.course_id_list = course_id_list

    def __str__(self):
        """
        This method returns the string representation of the object.

        Returns
        -------
        a String of the format “uid;;;username;;;password;;;register_time;;;role;;;email;;;display_name;;;
        job_title;;;course_id1--course_id2--course_id3”
        """
        i = 0
        print_course_ids = ""
        for each_course_id in self.course_id_list:
            if i == 0:
                print_course_ids = print_course_ids + each_course_id
                i = i + 1
            else:
                print_course_ids = print_course_ids + "--" + each_course_id
        return "{};;;{};;;{};;;{};;;{};;;{};;;{};;;{};;;{}".format(self.uid, self.username, self.password,
                                                                   self.register_time, self.role, self.email,
                                                                   self.display_name, self.job_title,
                                                                   print_course_ids)

    def get_instructors(self):
        """
        This method will extract instructor information from the given course data files.
        """
        os.chdir("data/source_course_files/")
        category_folders_list = os.listdir(os.getcwd())
        list_of_lines = []
        for each_category_folder in category_folders_list:
            each_category_folder_list = os.listdir(os.getcwd() + "/" + each_category_folder)
            for each_folder in each_category_folder_list:
                each_folder_list = os.listdir(os.getcwd() + "/" + each_category_folder + "/" + each_folder)
                for each_file in each_folder_list:
                    try:
                        with open(os.getcwd() + "/" + each_category_folder + "/" + each_folder + "/" + each_file,
                                  "r") as fjson:
                            data = json.load(fjson)
                            dict_unit = data["unitinfo"]
                            list_of_course = dict_unit["items"]
                            for each_course in list_of_course:
                                course_id = str(each_course['id'])
                                for each_instructor in each_course['visible_instructors']:
                                    flag = False
                                    index = -1
                                    for each_list in list_of_lines:
                                        index = index + 1
                                        if each_instructor['id'] in each_list:
                                            flag = True
                                            break
                                    if flag:
                                        list_of_lines[index][8] = list_of_lines[index][8] + "--" + course_id
                                    else:
                                        new_line = []
                                        new_line.append(each_instructor['id'])
                                        new_line.append(re.sub(" ", "_", each_instructor['display_name'].lower()))
                                        new_line.append(self.encrypt_password(str(each_instructor['id'])))
                                        new_line.append(self.register_time)
                                        new_line.append(self.role)
                                        new_line.append(re.sub(" ", "_", each_instructor['display_name'].lower())
                                                        + "@gmail.com")
                                        new_line.append(each_instructor['display_name'])
                                        new_line.append(each_instructor['job_title'])
                                        new_line.append(course_id)
                                        list_of_lines.append(new_line)
                    except:
                        print("Error reading from json file")
        try:
            os.chdir("../")
            os.chdir("../")
            with open(user_data_path, "a") as fuser:
                for each_line in list_of_lines:
                    fuser.write("{};;;{};;;{};;;{};;;{};;;{};;;{};;;{};;;{}\n".format(each_line[0], each_line[1],
                                                                                      each_line[2], each_line[3],
                                                                                      each_line[4], each_line[5],
                                                                                      each_line[6], each_line[7],
                                                                                      each_line[8]))
        except FileNotFoundError:
            print("user.txt file not found.")
            print("cwd might be changed or the file doesnt exist")
        except:
            print("Error reading from user.txt file")

    def get_instructors_by_page(self, page):
        """
        This method reads the user.txt file to retrieve all the instructor information.
        With all the instructor information and the current page number, a list of Instructor objects
        and the total pages will be generated. Each page has at most 20 instructors.

        Parameters
        ----------
        page: an int representing the page number

        Returns
        -------
        A tuple contains the list of instructors, total page number and the total number of instructors
        """
        total_instructors = 0
        total_pages = 0
        instructor_info_list = []
        instructor_object_list = []
        try:
            with open(user_data_path, "r") as fuser:
                for each_line in fuser:
                    if each_line.strip().split(";;;")[4].lower() == "instructor":
                        total_instructors = total_instructors + 1
                        instructor_info_list.append(each_line.strip())
        except FileNotFoundError:
            print("user.txt file not found.")
            print("cwd might be changed or the file doesnt exist")
        except:
            print("Error reading from user.txt file")
        if total_instructors % 20 == 0:
            total_pages = int(total_instructors / 20)
        else:
            total_pages = 1 + int(total_instructors / 20)
        try:
            for i in range((page - 1) * 20, page * 20):
                if i < len(instructor_info_list):
                    instructor_info = instructor_info_list[i].split(";;;")
                    course_list = instructor_info[8].split("--")
                    instructor_object_list.append(Instructor(int(instructor_info[0]), instructor_info[1],
                                                             instructor_info[2], instructor_info[3],
                                                             instructor_info[4], instructor_info[5],
                                                             instructor_info[6], instructor_info[7],
                                                             course_list))
                else:
                    break
        except:
            print("Error in creating instructor object")
        return (instructor_object_list, total_pages, total_instructors)

    def generate_instructor_figure1(self):
        """
        This method generates a graph that shows the top 10 instructors who teach the most courses

        Returns
        -------
        a string explanation about the understanding of this figure.
        """
        try:
            df = pd.read_csv(user_data_path, engine="python", sep=";;;", header=None,
                             names=["uid", "username", "password",
                                    "register_time", "role",
                                    "email", "display_name",
                                    "job_title",
                                    "course_id_list"])

            # Selecting only insturctor data from the user data
            instructor_df = df.loc[df['role'] == "instructor"]

            # Getting all the instructor names as list
            instructor_names = instructor_df['display_name'].to_list()

            instructor_course_id_list = instructor_df['course_id_list'].to_list()
            instructor_course_id_count_list = []
            for each in instructor_course_id_list:
                instructor_course_id_count_list.append(len(each.split("--")))

            # Calculating the index for the top ten list elements
            index = sorted(range(len(instructor_course_id_count_list)),
                           key=lambda i: instructor_course_id_count_list[i])[-10:]

            # creating list for storing the top ten instructors and a liost for storing the number of courses
            instructor_name_list = []
            number_of_courses = []
            for each in index:
                instructor_name_list.append(instructor_names[each])
                number_of_courses.append((instructor_course_id_count_list[each]))

            for i in range(len(instructor_name_list)):
                if len(instructor_name_list[i].split(" ")) > 3:
                    instructor_name_list[i] = instructor_name_list[i].split(" ")[0] + " " + \
                                              instructor_name_list[i].split(" ")[1] + " " + \
                                              instructor_name_list[i].split(" ")[2]

            # Change the figure size
            plt.figure(figsize=(25, 20))

            # Change the font size of axes, tick label
            plt.rc('axes', labelsize=25, titlesize=35)
            plt.rc('ytick', labelsize=20)
            plt.rc('xtick', labelsize=12)

            # Ploting the graph
            plt.bar(instructor_name_list, number_of_courses, linewidth=1.5)

            # Labeling the x-axis and y-axis and defining he title
            plt.xlabel("Name of the Instructor")
            plt.ylabel("Number of Courses")
            plt.title("Top 10 Instructors Who Teaches The Most Number Of Courses")
            plt.show()

            return "{} teaches {} courses which is the highest number taught by an instructor".format(
                instructor_name_list[9], number_of_courses[9])

        except Exception as e:
            print(e)
