import os
import sys
import subprocess
from selenium import webdriver
from utilities import ConfigReader
import allure
from allure_commons.types import AttachmentType

# ✅ Fix: Add missing import and cleaner logic
def add_project_paths():
    base_path = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    for folder in ["utilities", "configurations"]:
        full_path = os.path.join(base_path, folder)
        if full_path not in sys.path:
            sys.path.insert(0, full_path)

add_project_paths()

# Update Allure path correctly
ALLURE_PATH = r"C:\Program Files\allure-2.32.0\bin\allure.bat"

def before_scenario(context, scenario):
    try:
        browser_name = ConfigReader.read_configuration("basic info", "browser")

        if browser_name.lower() == "chrome":
            context.driver = webdriver.Chrome()
        elif browser_name.lower() == "firefox":
            context.driver = webdriver.Firefox()
        elif browser_name.lower() == "edge":
            context.driver = webdriver.Edge()
        else:
            raise Exception(f"Browser '{browser_name}' is not supported!")

        context.driver.maximize_window()
        context.driver.get(ConfigReader.read_configuration("basic info", "url"))

    except Exception as e:
        print(f"❌ Error in before_scenario: {e}")
        context.driver = None  # So we don't crash in after_scenario

def after_scenario(context, scenario):
    try:
        if context.driver:
            context.driver.quit()
    except Exception as e:
        print(f"⚠️ Error during driver.quit(): {e}")

def after_step(context, step):
    if context.driver:
        try:
            allure.attach(
                context.driver.get_screenshot_as_png(),
                name=f"Step_{step.name}",
                attachment_type=AttachmentType.PNG
            )
        except Exception as e:
            print(f"⚠️ Screenshot failed: {e}")
