import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def before_all(context):
    options = Options()

    # Detect if running in CI environment
    if os.getenv("CI"):
        # GitHub Actions: use local Chrome with headless mode
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=options)
    else:
        # Local development: use Selenium Grid (docker)
        driver = webdriver.Remote(
            command_executor="http://127.0.0.1:4444/wd/hub",
            options=options,
        )

    context.driver = driver


def after_all(context):
    context.driver.close()
