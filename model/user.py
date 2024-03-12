import random
import os
import re
from lib.helper import user_data_path


class User:
    # To check the functionality of any method separately,
    # uncomment the line below if the cwd is /model for admin, instructor and student class

    # os.chdir("../")
    current_login_user = None

    def __init__(self, uid=-1, username="", password="", register_time="yyyy-MM-dd_HH:mm:ss.SSS",
                 role=""):
        """
        This is the default constructor of User class
        """
        self.uid = uid
        self.username = username
        self.password = password
        self.register_time = register_time
        self.role = role

    def __str__(self):
        """
        This method returns the string representation of the object.

        Returns
        -------
        a String of the format “uid;;;username;;;password;;;register_time;;;role”
        """
        return "{};;;{};;;{};;;{};;;{}".format(self.uid, self.username, self.password,
                                               self.register_time, self.role)

    def validate_username(self, username):
        """
        This method validates the username

        Parameters
        ----------
        username: a String representing the username

        Returns
        -------
        True if The username contains only letters or underscore.
        If not, return False.
        """
        if re.fullmatch("^[a-zA-Z_]*$", username):
            return True
        else:
            return False

    def validate_password(self, password):
        """
        This method validates the password

        Parameters
        ----------
        password: a String representing the password

        Returns
        -------
        True if The length of password is greater than or equal to 8.
        If not, return False.
        """
        if len(password) >= 8:
            return True
        else:
            return False

    def validate_email(self, email):
        """
        This method uses regex expressions to check whether the email address is valid or not.

        Parameters
        ----------
        email: a String representing the email of the user

        Returns
        -------
        True if the email ends with “.com”, contain “@”, and have length greater than 8.
        If not, return False.
        """
        if len(email) >= 8:
            if re.fullmatch("^[a-zA-Z0-9]+[.]*[a-zA-Z0-9]*@[a-z]+.com", email):
                return True
            else:
                return False
        else:
            return False

    def clear_user_data(self):
        """
        This method will remove all the data in the user.txt file.
        """
        try:
            fuser = open(user_data_path, "w")
            fuser.close()
        except FileNotFoundError:
            print("user.txt file not found")
            print("cwd might be changed or the file doesnt exist")
        except:
            print("Error opening user.txt file")

    def authenticate_user(self, username, password):
        """
        This method is used to check whether username and password can be matched with users saved in
        user.txt data file.

        Parameters
        ----------
        username: a String representing the username
        password: a String representing the password

        Returns
        -------
        If matched, this method will retrieve the user information from user.txt file and return a tuple
        (True, user_info_string), otherwise return (False, “”).
        """
        try:
            with open(user_data_path, "r") as fuser:
                for each_line in fuser:
                    each_user_data = each_line.strip().split(";;;")
                    if each_user_data[1] == username and each_user_data[2] == self.encrypt_password(password):
                        return (True, each_line.strip())
                return (False, "")
        except FileNotFoundError:
            print("user.txt file not found")
            print("cwd might be changed or the file doesnt exist")
        except:
            print("Error reading from user.txt file")

    def check_username_exist(self, username):
        """
        This method is to check whether the given username exists in the user.txt data file.

        Parameters
        ----------
        username: a string representing the username

        Returns
        -------
        If username exists, return True, otherwise return False.
        """
        try:
            with open(user_data_path, "r") as fuser:
                for each_line in fuser:
                    each_user_data = each_line.strip().split(";;;")
                    if each_user_data[1] == username:
                        return True
                return False
        except FileNotFoundError:
            print("user.txt file not found")
            print("cwd might be changed or the file doesnt exist")
        except:
            print("Error reading from user.txt file")

    def generate_unique_user_id(self, number_of_digits=6):
        """
        This method is used to generate and return a 6 digit unique user id which is not in the user.txt file.

        Parameters
        ----------
        number_of_digits: int An integer representing the number of digits

        Return
        ------
        string A random id generated
        """
        flag = False

        # Generating a random number
        random_number = str(random.randint(10 ** (number_of_digits - 1), 10 ** number_of_digits - 1))

        # Checking whether the generated random number is already present
        try:
            with open(user_data_path, "r") as fuser:
                for each_line in fuser:
                    each_user_data = each_line.strip().split(";;;")
                    if each_user_data[0] == random_number:
                        flag = True
                        break
        except FileNotFoundError:
            print("user.txt file not found")
            print("cwd might be changed or the file doesnt exist")
        except:
            print("Error reading from user.txt file")
        if flag:
            self.generate_unique_user_id()
        else:
            return random_number

    def encrypt_password(self, password):
        """
        This function encrypts the password entered by the user

        Parameters
        ----------
        password : str
            String containing the password to be encrypted

        Returns
        -------
        str
            String containing the encrypted password

        Example
        -------
        >>> encrypt_password("password")
        returns “^^^)p)$$a$$)))s))))s)$$w$$)))o))))r)$$d$$$$$”
        """
        # Characters for encrypting the password
        all_punctuation = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
        # List to store the index of the three characters for encryption
        index_of_char_for_encryption = []
        index_of_char_for_encryption.append(len(password) % len(all_punctuation))  # first character
        index_of_char_for_encryption.append(len(password) % 5)  # second character
        index_of_char_for_encryption.append(len(password) % 10)  # third character
        # initialising the encrypted password variable
        encrypt_password = "^^^"
        # Loop to concatenate the all_punctuation characters and password characters
        for i in range(0, len(password)):
            # adds the first character for encryption one time before and after the [i]th character of password
            if i % 3 == 0:
                encrypt_password += all_punctuation[index_of_char_for_encryption[i % 3]]
                encrypt_password += password[i]
                encrypt_password += all_punctuation[index_of_char_for_encryption[i % 3]]
            # adds the second character for encryption two time before and after the [i]th character of password
            elif i % 3 == 1:
                encrypt_password += all_punctuation[index_of_char_for_encryption[i % 3]] * 2
                encrypt_password += password[i]
                encrypt_password += all_punctuation[index_of_char_for_encryption[i % 3]] * 2
            # adds the third character for encryption three time before and after the [i]th character of password
            elif i % 3 == 2:
                encrypt_password += all_punctuation[index_of_char_for_encryption[i % 3]] * 3
                encrypt_password += password[i]
                encrypt_password += all_punctuation[index_of_char_for_encryption[i % 3]] * 3
        encrypt_password += "$$$"
        return encrypt_password

    def register_user(self, username, password, email, register_time, role):
        """
        This method registers a new user to the system

        Parameters
        ----------
        username: a string representing the username
        password: a string representing the password
        email: a string representing the email
        register_time: an int representing the unix epoch timestamp in milliseconds
        role: a string representing the role of the user

        Returns
        -------
        If the username exists in the user.txt file, return False.
        If the user registers successfully, return True.
        """
        flag = False
        try:
            with open(user_data_path, "r") as fuser:
                for each_line in fuser:
                    each_user_data = each_line.strip().split(";;;")
                    if each_user_data[1] == username:
                        flag = True
                        break
        except FileNotFoundError:
            print("user.txt file not found")
            print("cwd might be changed or the file doesnt exist")
        except:
            print("Error reading from user.txt file")
        if flag:
            return False
        else:
            try:
                with open(user_data_path, "a") as fuser:
                    if role.lower() == "student":
                        fuser.write("{};;;{};;;{};;;{};;;{};;;{}\n".format(self.generate_unique_user_id(),
                                                                           username, self.encrypt_password(password),
                                                                           self.date_conversion(register_time),
                                                                           role, email))
                    elif role.lower() == "instructor":
                        fuser.write("{};;;{};;;{};;;{};;;{};;;{};;;;;;;;;\n".format(self.generate_unique_user_id(),
                                                                                    username,
                                                                                    self.encrypt_password(password),
                                                                                    self.date_conversion(register_time),
                                                                                    role, email))
            except FileNotFoundError:
                print("user.txt file not found")
                print("cwd might be changed or the file doesnt exist")
            except:
                print("Error reading from user.txt file")
            return True

    def date_conversion(self, register_time):
        """
        This method converts the given register_time which will be a unix epoch timestamp (milli seconds)
        into the format “year-month-day_hour:minute:second.milliseconds”.
        Parameters
        ----------
        register_time: an int representing the register time

        Returns
        -------
        a string representing the converted register time in format
        "year-month-day_hour:minute:second.milliseconds"
        """
        register_time = int(register_time)
        register_time = register_time + 11 * 3600 * 1000  # Converting to AEST
        yyyy = 1970 + int(register_time / 31556926000)
        register_time = register_time % 31556926000
        MM = 1 + int(register_time / 2629743000)
        if MM < 10:
            MM = '0' + str(MM)
        register_time = register_time % 2629743000
        dd = 1 + int(register_time / 86400000)
        if dd < 10:
            dd = '0' + str(dd)
        register_time = register_time % 86400000
        HH = int(register_time / 3600000)
        if HH < 10:
            HH = '0' + str(HH)
        register_time = register_time % 3600000
        mm = int(register_time / 60000)
        if mm < 10:
            mm = '0' + str(mm)
        register_time = register_time % 60000
        ss = int(register_time / 1000)
        if ss < 10:
            ss = '0' + str(ss)
        register_time = register_time % 1000
        if register_time < 10:
            SSS = '00' + str(register_time)
        elif register_time >= 10 and register_time < 100:
            SSS = '0' + str(register_time)
        else:
            SSS = str(register_time)
        return "{}-{}-{}_{}:{}:{}.{}".format(yyyy, MM, dd, HH, mm, ss, SSS)
