from model.user import User
from lib.helper import user_data_path
from time import time


class Admin(User):
    def __init__(self, uid=-1, username="", password="", register_time="yyyy-MM-dd_HH:mm:ss.SSS", role="admin"):
        """
        This is the default constructor of Admin class
        """
        super().__init__(uid, username, password, register_time, role)

    def register_admin(self):
        """
        This method will create a new admin account and write this account into the user.txt file.
        """
        try:
            with open(user_data_path, "a") as fuser:
                fuser.write("{};;;{};;;{};;;{};;;{}\n".format(self.generate_unique_user_id(),
                                                              "admin", self.encrypt_password("admin1234"),
                                                              self.date_conversion(int(time() * 1000)),
                                                              "admin"))
        except FileNotFoundError:
            print("user.txt file not found. change current working directory")
        except:
            print("Error reading from user.txt file")

    def __str__(self):
        """
        This method returns the string representation of the object.

        Returns
        -------
        a String of the format “uid;;;username;;;password;;;register_time;;;role”
        """
        return User.__str__(self)
