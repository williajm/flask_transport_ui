from selenium import webdriver


def before_all(context):
    driver = webdriver.Remote(
        command_executor="http://127.0.0.1:4444/wd/hub",
        desired_capabilities={"browserName": "chrome", "javascriptEnabled": True},
    )
    context.driver = driver


def after_all(context):
    context.driver.close()
