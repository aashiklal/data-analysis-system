import json
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from lib.helper import course_data_path, user_data_path


class Course:
    # To check the functionality of any method separately, uncomment the line below if the cwd is /model
    # os.chdir("../")

    def __init__(self, category_title="", subcategory_id=-1, subcategory_title="", subcategory_description="",
                 subcategory_url="", course_id=-1, course_title="", course_url="", num_of_subscribers=0,
                 avg_rating=0.0, num_of_reviews=0):
        """
        This is the default constructor for Course class
        """
        self.category_title = category_title
        self.subcategory_id = subcategory_id
        self.subcategory_title = subcategory_title
        self.subcategory_description = subcategory_description
        self.subcategory_url = subcategory_url
        self.course_id = course_id
        self.course_title = course_title
        self.course_url = course_url
        self.num_of_subscribers = num_of_subscribers
        self.avg_rating = avg_rating
        self.num_of_reviews = num_of_reviews

    def __str__(self):
        """
        This method returns the string representation of the object.

        Returns
        -------
        a String of the format “{category_title};;;{subcategory_id};;;{subcategory_title};;;
        {subcategory_description};;;{subcategory_url};;;{course_id};;;{course_title};;;{course_url};;;
        {num_of_subscribers};;;{avg_rating};;;{num_of_reviews}”
        """
        return "{};;;{};;;{};;;{};;;{};;;{};;;{};;;{};;;{};;;{};;;{}".format(self.category_title, self.subcategory_id,
                                                                             self.subcategory_title,
                                                                             self.subcategory_description,
                                                                             self.subcategory_url, self.course_id,
                                                                             self.course_title,
                                                                             self.course_url, self.num_of_subscribers,
                                                                             self.avg_rating, self.num_of_reviews)

    def get_courses(self):
        """
        This method will extract course information from the given course data files.
        """
        os.chdir("data/source_course_files/")
        category_folders_list = os.listdir(os.getcwd())
        list_of_lines = []
        for each_category_folder in category_folders_list:
            category = each_category_folder.split("_")[2]
            each_category_folder_list = os.listdir(os.getcwd() + "/" + each_category_folder)
            for each_folder in each_category_folder_list:
                each_folder_list = os.listdir(os.getcwd() + "/" + each_category_folder + "/" + each_folder)
                for each_file in each_folder_list:
                    try:
                        with open(os.getcwd() + "/" + each_category_folder + "/" + each_folder + "/" + each_file,
                                  "r") as fjson:
                            data = json.load(fjson)
                            dict_unit = data["unitinfo"]
                            source_objects = dict_unit["source_objects"][0]
                            list_of_course = dict_unit["items"]
                            for each_course in list_of_course:
                                new_line = []
                                new_line.append(category)
                                new_line.append(source_objects["id"])
                                new_line.append(source_objects["title"])
                                new_line.append(source_objects["description"])
                                new_line.append(source_objects["url"])
                                new_line.append(each_course["id"])
                                new_line.append(each_course["title"])
                                new_line.append(each_course["url"])
                                new_line.append(each_course["num_subscribers"])
                                new_line.append(each_course["avg_rating"])
                                new_line.append(each_course["num_reviews"])
                                list_of_lines.append(new_line)
                    except:
                        print("Error reading from json file")
        try:
            os.chdir("../")
            os.chdir("../")
            with open(course_data_path, "w") as fcourse:
                for each_line in list_of_lines:
                    fcourse.write(
                        "{};;;{};;;{};;;{};;;{};;;{};;;{};;;{};;;{};;;{};;;{}\n".format(each_line[0], each_line[1],
                                                                                        each_line[2], each_line[3],
                                                                                        each_line[4], each_line[5],
                                                                                        each_line[6], each_line[7],
                                                                                        each_line[8], each_line[9],
                                                                                        each_line[10]))
        except FileNotFoundError:
            print("course.txt file not found.")
            print("cwd might be changed or the file doesnt exist")
        except:
            print("Error reading from course.txt file")

    def clear_course_data(self):
        """
        This method will remove all the content in the course.txt file.
        After calling this method, the course.txt file will become an empty file.
        """
        try:
            fcourse = open(course_data_path, "w")
            fcourse.close()
        except FileNotFoundError:
            print("course.txt file not found")
            print("cwd might be changed or the file doesnt exist")
        except:
            print("Error opening course.txt file")

    def generate_page_num_list(self, page, total_pages):
        """
        This method uses the current page number and total pages to generate a list of integers as viewable
        page numbers.

        Parameters
        ----------
        page: an int representing the page number
        total_pages: an int representing the total page number

        Returns
        -------
        a list of int
        """
        if page <= 5:
            return [i for i in range(1, 10)]
        elif page > 5 and page < total_pages - 4:
            return [i for i in range(page - 4, page + 5)]
        else:
            return [i for i in range(total_pages - 8, total_pages + 1)]

    def get_courses_by_page(self, page):
        """
        This method reads the course.txt file to retrieve all the course information. With all
        the course information and the current page number, a list of Course objects will be generated and
        the total pages and the total number of courses will be returned. Each page has at most 20 courses.

        Parameters
        ----------
        page: an int representing the page number

        Returns
        -------
        a tuple that contains a list of Course objects, total pages of courses and the total number of courses.
        """
        total_courses = 0
        course_info_list = []
        course_object_list = []
        try:
            with open(course_data_path, "r") as fcourse:
                for each_line in fcourse:
                    total_courses = total_courses + 1
                    course_info_list.append(each_line.strip())
        except FileNotFoundError:
            print("course.txt file not found")
            print("cwd might be changed or the file doesnt exist")
        except:
            print("Error reading from course.txt file")
        if total_courses % 20 == 0:
            total_pages = int(total_courses / 20)
        else:
            total_pages = 1 + int(total_courses / 20)
        try:
            for i in range((page - 1) * 20, page * 20):
                if i < len(course_info_list):
                    course_info = course_info_list[i].split(";;;")
                    course_object_list.append(Course(course_info[0], int(course_info[1]),
                                                     course_info[2], course_info[3],
                                                     course_info[4], int(course_info[5]),
                                                     course_info[6], course_info[7],
                                                     int(course_info[8]), float(course_info[9]),
                                                     int(course_info[10])))
                else:
                    break
        except:
            print("Error in creating instructor object")
        return (course_object_list, total_pages, total_courses)

    def delete_course_by_id(self, temp_course_id):
        """
        The method reads course info from the course.txt file and deletes the course information belongs to
        that course_id. If an instructor in the user.txt file teaches this course, the course id will
        be removed from the instructor’s course_id_list.


        Parameters
        ----------
        temp_course_id: an int representing the course id

        Returns
        -------
        True if course id is found and it is removed successfully.
        Else returns False
        """
        i = 0
        try:
            with open(course_data_path, "r") as fcourse:
                lines = fcourse.readlines()
        except FileNotFoundError:
            print("course.txt file not found")
            print("cwd might be changed or the file doesnt exist")
        except:
            print("Error reading from course.txt file")
        try:
            with open(course_data_path, "w") as fcourse:
                for each_line in lines:
                    if not each_line.strip().split(";;;")[5] == str(temp_course_id):
                        fcourse.write("{}".format(each_line))
                    else:
                        i = i + 1
        except FileNotFoundError:
            print("course.txt file not found")
            print("cwd might be changed or the file doesnt exist")
        except:
            print("Error writing to course.txt file")
        try:
            with open(user_data_path, "r") as fuser:
                user_lines = fuser.readlines()
        except FileNotFoundError:
            print("user.txt file not found")
            print("cwd might be changed or the file doesnt exist")
        except:
            print("Error reading from user.txt file")
        try:
            with open(user_data_path, "w") as fuser:
                for each_line in user_lines:
                    if each_line.strip().split(";;;")[4].lower() == "instructor":
                        if str(temp_course_id) in each_line.strip().split(";;;")[8].split("--"):
                            temp_list = each_line.strip().split(";;;")
                            course_id_list = []
                            for each_course_id in temp_list[8].split("--"):
                                if each_course_id != str(temp_course_id):
                                    course_id_list.append(each_course_id)
                            course_ids = ""
                            j = -1
                            for each_course_id in course_id_list:
                                j = j + 1
                                if j == len(course_id_list) - 1:
                                    course_ids = course_ids + each_course_id
                                else:
                                    course_ids = course_ids + each_course_id + "--"
                            fuser.write("{};;;{};;;{};;;{};;;{};;;{};;;{};;;{};;;{}\n".format(temp_list[0],
                                                                                              temp_list[1],
                                                                                              temp_list[2],
                                                                                              temp_list[3],
                                                                                              temp_list[4],
                                                                                              temp_list[5],
                                                                                              temp_list[6],
                                                                                              temp_list[7],
                                                                                              course_ids))
                            i = i + 1
                        else:
                            fuser.write("{}".format(each_line))
        except FileNotFoundError:
            print("user.txt file not found")
            print("cwd might be changed or the file doesnt exist")
        except:
            print("Error writing to user.txt file")
        if i > 0:
            if i == 1:
                print("Course id removed from course.txt")
            if i == 2:
                print("Course id removed from course.txt and user.txt")
            return True
        else:
            return False

    def get_course_by_course_id(self, temp_course_id):
        """
        This method will find the course by given course_id and convert the info to a Course object.

        Parameters
        ----------
        temp_course_id: an int value representing the course id

        Returns
        -------
        a tuple containing the Course object and comment if found
        Else it returns none
        """
        try:
            with open(course_data_path, "r") as fcourse:
                for each_line in fcourse:
                    if each_line.strip().split(";;;")[5] == str(temp_course_id):
                        course_info = each_line.strip().split(";;;")
                        course_object = Course(course_info[0], int(course_info[1]), course_info[2], course_info[3],
                                               course_info[4], int(course_info[5]), course_info[6], course_info[7],
                                               int(course_info[8]), float(course_info[9]), int(course_info[10]))
                        try:
                            num_of_sub = int(course_info[8])
                            avg_rating = float(course_info[9])
                            num_of_reviews = int(course_info[10])
                        except:
                            print("Error in converting str to int")
                        if num_of_sub > 100000 and avg_rating > 4.5 and num_of_reviews > 10000:
                            comment = "Top Courses"
                        elif num_of_sub > 50000 and avg_rating > 4.0 and num_of_reviews > 5000:
                            comment = "Popular Courses"
                        elif num_of_sub > 10000 and avg_rating > 3.5 and num_of_reviews > 1000:
                            comment = "Good Courses"
                        else:
                            comment = "General Courses"
                        return (course_object, comment)
        except FileNotFoundError:
            print("course.txt file not found")
            print("cwd might be changed or the file doesnt exist")
        except Exception as e:
            print(e)

    def get_course_by_instructor_id(self, instructor_id):
        """
        This method reads the user.txt file and course.txt file to find all the course information
        the specified instructor teaches. If this instructor teaches more than 20 courses, only 20 courses
        will be returned with the total number of courses this instructor teaches. Otherwise, all the
        courses and the total number will be returned.

        Parameters
        ----------
        instructor_id: an int representing the instructor id

        Returns
        -------
        a tuple that contains a list of course objects and the total number of courses if the instructor id is
        found, otherwise returns None
        """
        course_id_list = []
        course_object_list = []
        try:
            with open(user_data_path, "r") as fuser:
                for each_line in fuser:
                    if each_line.strip().split(";;;")[0] == str(instructor_id):
                        course_id_list = each_line.strip().split(";;;")[8].split("--")
        except FileNotFoundError:
            print("user.txt file not found")
            print("cwd might be changed or the file doesnt exist")
        except:
            print("Error reading from user.txt file")
        total_courses = len(course_id_list)
        if len(course_id_list) > 20:
            course_id_list = course_id_list[:20]
        try:
            with open(course_data_path, "r") as fcourse:
                for each_line in fcourse:
                    if each_line.strip().split(";;;")[5] in course_id_list:
                        course_info = each_line.strip().split(";;;")
                        course_object = Course(course_info[0], int(course_info[1]), course_info[2], course_info[3],
                                               course_info[4], int(course_info[5]), course_info[6], course_info[7],
                                               int(course_info[8]), float(course_info[9]), int(course_info[10]))
                        course_object_list.append(course_object)
        except FileNotFoundError:
            print("course.txt file not found")
            print("cwd might be changed or the file doesnt exist")
        except Exception as e:
            print(e)
        return (course_object_list, total_courses)

    def generate_course_figure1(self):
        """
        This method generates a graph to show the top 10 subcategories with the most subscribers.

        Returns
        -------
        a string explanation about this figure
        """
        try:
            # Reading the file as pandas dataframe
            df = pd.read_csv(course_data_path, engine="python", sep=";;;", header=None,
                             names=["category_title", "subcategory_id", "subcategory_title",
                                    "subcategory_description", "subcategory_url", "course_id",
                                    "course_title", "course_url", "num_of_subscribers", "avg_rating",
                                    "num_of_reviews"])

            num_of_subscribers = df['subcategory_title'].value_counts(ascending=True).to_numpy()
            subcategory_title = df['subcategory_title'].value_counts(ascending=True).keys().to_numpy()

            # Extracting only the first three words of the subcategory name if it is too long
            for i in range(len(subcategory_title)):
                if len(subcategory_title[i].split(" ")) > 3:
                    subcategory_title[i] = subcategory_title[i].split(" ")[0] + " " + \
                                           subcategory_title[i].split(" ")[1] + " " + \
                                           subcategory_title[i].split(" ")[2]

            # Change the figure size
            plt.figure(figsize=(25, 20))

            # Change the font size of axes, tick label
            plt.rc('axes', labelsize=25, titlesize=35)
            plt.rc('ytick', labelsize=20)
            plt.rc('xtick', labelsize=10)

            # Plotting the graph by passing only the top 10 values from both the list
            plt.bar(subcategory_title[-10:], num_of_subscribers[-10:], linewidth=1.5)

            # Labeling the x-axis and y-axis and defining he title
            plt.xlabel("Subcategory Title")
            plt.ylabel("Total Number Of Subscribers")
            plt.title("Top 10 Subcategories With Most Subscribers")
            plt.show()

            return "The subcategory {} has {} subscribers which is the highest out of all subcategories".format(
                subcategory_title[-1], num_of_subscribers[-1])

        except Exception as e:
            print(e)

    def generate_course_figure2(self):
        """
        This method generates a graph to show the top 10 courses that have lowest avg rating and
        over 50000 reviews.

        Returns
        -------
        a string explanation about this figure
        """
        try:
            # Reading the file as pandas dataframe
            df = pd.read_csv(course_data_path, engine="python", sep=";;;", header=None,
                             names=["category_title", "subcategory_id", "subcategory_title",
                                    "subcategory_description", "subcategory_url", "course_id",
                                    "course_title", "course_url", "num_of_subscribers", "avg_rating",
                                    "num_of_reviews"])

            # Selecting only courses with over 50000 reviews
            df = df.loc[df['num_of_reviews'] > 50000]

            # Creating a list of course_title and avg_rating
            course_title = df['course_title'].tolist()
            avg_rating = df['avg_rating'].tolist()

            # Creating a dictionary of course_title and avg_rating
            dict_of_data = {course_title[i]: avg_rating[i] for i in range(len(course_title))}

            # Sorting the dictionary based on values
            sorted_dict_of_data = {}
            sorted_values = sorted(dict_of_data.values())
            for each in sorted_values:
                for keys in dict_of_data.keys():
                    if dict_of_data[keys] == each:
                        sorted_dict_of_data[keys] = dict_of_data[keys]
                        break

            # Gathering the sorted course title and avg rating in two different list
            sorted_course_title = list(sorted_dict_of_data.keys())
            sorted_avg_rating = list(sorted_dict_of_data.values())

            # Extracting only the first three words of the course title if it is too long
            for i in range(len(sorted_course_title)):
                if len(sorted_course_title[i].split(" ")) > 3:
                    sorted_course_title[i] = sorted_course_title[i].split(" ")[0] + " " + \
                                             sorted_course_title[i].split(" ")[1] + " " + \
                                             sorted_course_title[i].split(" ")[2]

            # Change the figure size
            plt.figure(figsize=(25, 20))

            # Change the font size of axes, tick label
            plt.rc('axes', labelsize=25, titlesize=35)
            plt.rc('ytick', labelsize=20)
            plt.rc('xtick', labelsize=10)

            # Plotting the graph by passing only the top 10 values from both the list
            plt.bar(sorted_course_title[:10], sorted_avg_rating[:10], linewidth=1.5)

            # Labeling the x-axis and y-axis and defining he title
            plt.xlabel("Course Title")
            plt.ylabel("Average Rating")
            plt.title("Top 10 Courses That Have Lowest Avg Rating And Over 50000 Reviews")
            plt.show()

            return "{} have an avg rating of {} which is the lowest for courses over " \
                   "50000 reviews".format(sorted_course_title[0], sorted_avg_rating[0])

        except Exception as e:
            print(e)

    def generate_course_figure3(self):
        """
        This method generate a graph to show the all the courses avg rating distribution that has
        subscribers between 100000 and 10000

        Returns
        -------
        a string explanation about this figure
        """
        try:
            # Reading the file as pandas dataframe
            df = pd.read_csv(course_data_path, engine="python", sep=";;;", header=None,
                             names=["category_title", "subcategory_id", "subcategory_title",
                                    "subcategory_description", "subcategory_url", "course_id",
                                    "course_title", "course_url", "num_of_subscribers", "avg_rating",
                                    "num_of_reviews"])

            # Selecting only courses with subscribers between 10000 and 100000
            df = df.loc[(df['num_of_subscribers'] >= 10000) & (df['num_of_subscribers'] <= 100000)]

            # Creating numpy array of required values
            num_of_subscribers = df.iloc[:, 8].values
            avg_rating = df.iloc[:, 9].values

            # Change the figure size
            plt.figure(figsize=(25, 20))

            # Change the font size of axes, tick label
            plt.rc('axes', labelsize=25, titlesize=35)
            plt.rc('ytick', labelsize=20)
            plt.rc('xtick', labelsize=20)

            # Creating scatter plot
            plt.scatter(num_of_subscribers, avg_rating)

            # Labeling the x-axis and y-axis and defining he title
            plt.xlabel("Number Of Subscribers")
            plt.ylabel("Average Rating")
            plt.title("Graph Showing All Course Avg Rating Distribution That Has Subscribers between 10000 and 100000")

            # Displaying the graph
            plt.show()

            return "Majority of the courses have an avg rating above 3.5"

        except Exception as e:
            print(e)

    def generate_course_figure4(self):
        """
        This method generate a graph to show the number of courses for all categories and sort in
        ascending order

        Returns
        -------
        a string explanation about this figure
        """
        try:
            # Reading the file as pandas dataframe
            df = pd.read_csv(course_data_path, engine="python", sep=";;;", header=None,
                             names=["category_title", "subcategory_id", "subcategory_title",
                                    "subcategory_description", "subcategory_url", "course_id",
                                    "course_title", "course_url", "num_of_subscribers", "avg_rating",
                                    "num_of_reviews"])

            # Gathering the required values
            category_titles = df['category_title'].value_counts(ascending=True).keys().to_numpy()
            number_of_courses = df['category_title'].value_counts(ascending=True).to_numpy()

            # Change the figure size
            plt.figure(figsize=(25, 20))

            # Plotting the pie chart
            explode_list = [0.0 for i in range(len(category_titles))]
            explode_list[-2] = 0.1
            plt.pie(number_of_courses, labels=category_titles, explode=explode_list,
                    textprops={"fontsize": 25})

            # Title of chart
            plt.title("Number Of Courses Based On Category", fontsize=35)

            # Displaying the pie chart
            plt.show()

            return "{} category has the most number of courses : {}".format(category_titles[-1],
                                                                            number_of_courses[-1])

        except Exception as e:
            print(e)

    def generate_course_figure5(self):
        """
        This method generate a graph to show how many courses have reviews and how many
        courses do not have reviews.

        Returns
        -------
        a string explanation about this figure
        """
        try:
            # Reading the file as pandas dataframe
            df = pd.read_csv(course_data_path, engine="python", sep=";;;", header=None,
                             names=["category_title", "subcategory_id", "subcategory_title",
                                    "subcategory_description", "subcategory_url", "course_id",
                                    "course_title", "course_url", "num_of_subscribers", "avg_rating",
                                    "num_of_reviews"])

            # Courses having review
            df_have_review = df.loc[df['num_of_reviews'] != 0]

            # Courses not having review
            df_not_have_review = df.loc[df['num_of_reviews'] == 0]

            number_of_courses_having_review = len(df_have_review.index)
            number_of_courses_not_having_review = len(df_not_have_review.index)

            course_number_list = [number_of_courses_having_review, number_of_courses_not_having_review]
            labels = ["Courses With Review", "Courses Without Review"]

            # Change the figure size
            plt.figure(figsize=(25, 20))

            # Change the font size of axes, tick label
            plt.rc('axes', labelsize=25, titlesize=35)
            plt.rc('ytick', labelsize=20)
            plt.rc('xtick', labelsize=20)

            # Plotting the graph
            plt.bar(labels, course_number_list)
            plt.title("Courses With And Without Review")
            plt.show()

            return "There are {} number of courses with review and {} " \
                   "number of courses without review".format(number_of_courses_having_review,
                                                             number_of_courses_not_having_review)


        except Exception as e:
            print(e)

    def generate_course_figure6(self):
        """
        This method generate a graph to show the top 10 subcategories with the least courses

        Returns
        -------
        a string explanation about this figure
        """
        try:
            # Reading the file as pandas dataframe
            df = pd.read_csv(course_data_path, engine="python", sep=";;;", header=None,
                             names=["category_title", "subcategory_id", "subcategory_title",
                                    "subcategory_description", "subcategory_url", "course_id",
                                    "course_title", "course_url", "num_of_subscribers", "avg_rating",
                                    "num_of_reviews"])

            total_courses = df['subcategory_title'].value_counts(ascending=True).to_numpy()
            subcategory_title = df['subcategory_title'].value_counts(ascending=True).keys().to_numpy()

            # Extracting only the first three words of the subcategory name if it is too long
            for i in range(len(subcategory_title)):
                if len(subcategory_title[i].split(" ")) > 3:
                    subcategory_title[i] = subcategory_title[i].split(" ")[0] + " " + \
                                           subcategory_title[i].split(" ")[1] + " " + \
                                           subcategory_title[i].split(" ")[2]

            # Change the figure size
            plt.figure(figsize=(25, 20))

            # Change the font size of axes, tick label
            plt.rc('axes', labelsize=25, titlesize=35)
            plt.rc('ytick', labelsize=20)
            plt.rc('xtick', labelsize=10)

            # Plotting the graph by passing only the top 10 values from both the list
            plt.bar(subcategory_title[:10], total_courses[:10], linewidth=1.5)

            # Labeling the x-axis and y-axis and defining he title
            plt.xlabel("Subcategory Title")
            plt.ylabel("Number Of Courses")
            plt.title("Top 10 Subcategories With Least Number Of Courses")

            # Displaying the graph
            plt.show()

            return "{} has {} number of courses which is the least".format(subcategory_title[0], total_courses[0])

        except Exception as e:
            print(e)
