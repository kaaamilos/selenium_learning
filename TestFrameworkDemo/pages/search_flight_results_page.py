import selenium.common.exceptions

from base.base_driver import BaseDriver

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class SearchFlightResults(BaseDriver):
    def __init__(self, driver):
        super().__init__(driver)

    def filter_flights(self):
        try:
            self.wait_until_presence_of_element_located(
                By.XPATH,
                "//filters-wrapper[@class='filters-wrapper ng-tns-c142-3 ng-trigger ng-trigger-routeAnimation ng-star-inserted']"
            )
        except selenium.common.exceptions.TimeoutException:
            filter_xpath = "//button[@class='toggle-filters']"
            self.wait_until_element_is_clickable(By.XPATH, filter_xpath).click()
            self._choose_without_stops()
            show_results_button_css_selector = "button[class='btn normal function view-results-count ng-tns-c142-3']"
            self.wait_until_element_is_clickable(By.CSS_SELECTOR, show_results_button_css_selector).click()
        else:
            self._choose_without_stops()


    def _choose_without_stops(self):
        self.wait.until(
            (EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Bez przesiadek')]")))).click()

    def wait_for_presence_of_all_elements(self, locator_type, locator):
        list_of_elements = self.wait_until_presence_of_all_elements_located(locator_type, locator)
        return list_of_elements
