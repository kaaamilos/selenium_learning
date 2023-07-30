import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver

from base.base_driver import BaseDriver
from utilities.months import Months


def _reformat_date(date):
    day, month, year = date.split('/')
    return day, month, year


class LaunchPage(BaseDriver):
    #Locators

    DEPART_FROM_FIELD = 'departureRoundtrip0'

    def __init__(self, driver: webdriver):
        super().__init__(driver)

    def get_depart_from_location(self):
        return self.wait_until_element_is_clickable(By.ID, self.DEPART_FROM_FIELD)

    def enter_depart_from_location(self, depart_location):
        self.get_depart_from_location().click()
        self.get_depart_from_location().send_keys(depart_location)
        self.get_depart_from_location().send_keys(Keys.ENTER)

    def going_to(self, going_to_location):
        going_to = self.wait_until_element_is_clickable(By.ID, 'arrivalRoundtrip0')
        going_to.click()
        going_to.send_keys(going_to_location)

    def trip_one_way(self):
        trip_one_way_button = self.wait_until_element_is_clickable(
            By.XPATH,
            "//label[contains(text(),'W jedną stronę')]"
        )
        trip_one_way_button.click()

    def departure_date(self, departuredate):
        date_picker = self.wait_until_element_is_clickable(By.XPATH, "//input[@id='departureDateOneway']")
        self.set_date(date_picker, departuredate)

    def return_date(self, returndate):
        date_picker = self.wait_until_element_is_clickable(By.XPATH, "//input[@id='departureDateOneway']")

        date_picker.click()

        all_dates = self.wait_until_element_is_clickable(By.XPATH, "//span[@class='ui-datepicker-month']")
        all_dates = all_dates.find_elements((By.XPATH, "//span[@class='ui-datepicker-month']"))

        for date in all_dates:
            if date.get_attribute("data-date") == returndate:
                date.click()
                break

    def set_date(self, date_picker, date):
        date_picker.click()
        day, month, year = _reformat_date(date)
        self._set_year(year)
        self._set_month(month)
        self._set_day(day)

    def click_search(self):
        self.wait_until_element_is_clickable(By.CSS_SELECTOR, "button[class='btn transaction qsf-search']").click()

    def _set_year(self, year):
        if isinstance(year, str):
            year = int(year)
        current_year = self._get_current_year()
        print('current year', current_year)

        if current_year == year:
            return
        elif current_year < year:
            css_selector = '.ui-icon.ui-icon-circle-triangle-e'
        elif current_year > year:
            css_selector = '.ui-icon.ui-icon-circle-triangle-w'

        while not current_year == year:
            self.wait_until_element_is_clickable(By.CSS_SELECTOR, css_selector).click()

            current_year = self._get_current_year()

    def _set_month(self, month):
        if isinstance(month, str):
            month = int(month)
        current_month = self._get_current_month()
        print('current month', current_month)
        if current_month == month:
            return
        elif current_month < month:
            css_selector = '.ui-icon.ui-icon-circle-triangle-e'
        elif current_month > month:
            css_selector = '.ui-icon.ui-icon-circle-triangle-w'

        while not current_month == month:
            print(f'current month: {current_month}\ndesired month: {month}\n')
            self.wait_until_element_is_clickable(By.CSS_SELECTOR, css_selector).click()
            time.sleep(2)
            current_month = self._get_current_month()

    def _set_day(self, day):
        if isinstance(day, str):
            day = int(day)
        self.wait_until_element_is_clickable(By.XPATH, f"//a[normalize-space()='{day}']").click()

    def _get_current_month(self):
        current_month = self.driver.find_element(By.CSS_SELECTOR, '.ui-datepicker-month').text
        return Months[current_month].value

    def _get_current_year(self):
        return int(self.driver.find_element(By.CSS_SELECTOR, '.ui-datepicker-year').text)
