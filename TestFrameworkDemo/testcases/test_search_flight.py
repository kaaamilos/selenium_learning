import time
import pytest
from selenium.webdriver.common.by import By

from pages.esky__launch_page import LaunchPage
from pages.search_flight_results_page import SearchFlightResults
from utilities.utils import Utils


@pytest.mark.usefixtures("setup")
class TestSearchAndVerify:
    def test_search_flight(self):
        lp = LaunchPage(self.driver)

        lp.enter_depart_from_location('Warszawa')
        lp.going_to('Kraków')
        lp.trip_one_way()
        lp.departure_date("24/07/2023")
        lp.click_search()
        time.sleep(5)
        lp.page_scroll()

        sf = SearchFlightResults(self.driver)
        sf.filter_flights()
        time.sleep(5)
        bez_przesiadki_locator = "//span[contains(text(), 'bez przesiadki')]"

        without_stops = sf.wait_for_presence_of_all_elements(By.XPATH, bez_przesiadki_locator)
        ut = Utils()
        ut.assert_list_item_text(without_stops, 'bez przesiadki')


