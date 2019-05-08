from behave import step
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@step('the train times page')
def step_impl(context):
    context.driver.get("http://test_server:5000")


@step('I enter {keys} into the search box')
def step_impl(context, keys):
    search = WebDriverWait(context.driver, 10).until(EC.presence_of_element_located((By.ID, "search_data")))
    search.send_keys(keys)


@step('{suggestions} stations are suggested')
def step_impl(context, suggestions):
    results = WebDriverWait(context.driver, 10).until(EC.presence_of_all_elements_located(
        (By.XPATH, "//html/body/ul/li[@class='ui-menu-item']/div[@class='ui-menu-item-wrapper']")))
    expected = suggestions.split(',')
    actual = [result.text for result in results]
    assert expected == actual, f'expected={expected} actual={actual}'
