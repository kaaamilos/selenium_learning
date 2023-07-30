import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager


@pytest.fixture(scope="class")
def setup(request):
    print("setup method")
    service = Service(GeckoDriverManager().install())
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(service=service, options=options)
    driver.get('https://www.esky.pl/')
    driver.maximize_window()
    accept_cookies(driver)
    request.cls.driver = driver
    yield
    print('teardown method')
    driver.close()

def accept_cookies(driver):
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '# CybotCookiebotDialog')))
    except:
        pass
    finally:
        wait.until(EC.element_to_be_clickable((
            (By.CSS_SELECTOR, '#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
        ))).click()

