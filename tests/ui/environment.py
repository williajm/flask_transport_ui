from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def before_all(context):
    options = Options()
    driver = webdriver.Remote(
        command_executor="http://127.0.0.1:4444/wd/hub",
        options=options,
    )
    context.driver = driver


def after_all(context):
    context.driver.close()
