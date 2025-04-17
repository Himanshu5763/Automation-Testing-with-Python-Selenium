from datetime import datetime
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource (compatible with PyInstaller .exe) """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

def get_new_email_with_timestamp():
    time_stamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    return "amotoori" + time_stamp + "@gmail.com"
