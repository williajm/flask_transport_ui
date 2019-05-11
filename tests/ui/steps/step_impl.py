from behave import step
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException

WAIT_MAX = 5

@step('the train times page')
def step_impl(context):
    context.driver.get("http://test_server:5000")


@step('I enter {keys} into the search box')
def step_impl(context, keys):
    search = WebDriverWait(context.driver, WAIT_MAX).until(EC.presence_of_element_located((By.ID, "search_data")))
    search.send_keys(keys)


@step('{suggestions} stations are suggested')
def step_impl(context, suggestions):
    results = WebDriverWait(context.driver, WAIT_MAX).until(EC.presence_of_all_elements_located(
        (By.XPATH, "//html/body/ul/li[@class='ui-menu-item']/div[@class='ui-menu-item-wrapper']")))
    expected = suggestions.split(',')
    actual = [result.text for result in results]
    assert expected == actual, f'expected={expected} actual={actual}'


@step('I click the search button')
def step_impl(context):
    button = WebDriverWait(context.driver, WAIT_MAX).until(EC.presence_of_element_located((By.ID, "search_button")))
    button.click()


@step('the {station} departures page is displayed')
def step_impl(context, station):
    verify_station_name(context.driver, station)
    verify_departure_table()


def verify_station_name(driver: WebDriver, station: str) -> None:
    text_present_in_element_id(driver=driver, html_id='station_name', text=station)


def verify_departure_table():
    verify_times()
    verify_destination()
    verify_platform()
    verify_operator()
    verify_origin()
    verify_status()


def verify_times():
    pass


def verify_destination():
    pass


def verify_platform():
    pass


def verify_operator():
    pass


def verify_origin():
    pass


def verify_status():
    pass


def text_present_in_element_id(driver: WebDriver, html_id: str, text: str):
    try:
        WebDriverWait(driver, WAIT_MAX).until(EC.text_to_be_present_in_element((By.ID, html_id), text))
    except TimeoutException as te:
        # The default TimeoutException message is not that useful
        raise AssertionError(f'{text} not found in html id {html_id} within {WAIT_MAX} seconds') from te
