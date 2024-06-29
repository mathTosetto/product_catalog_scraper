import time
import random

import undetected_chromedriver as uc

from fake_useragent import UserAgent

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


class WebScraper:
    """A web scraper for using Selenium and undetected_chromedriver."""

    def __init__(self, url: str) -> None:
        """
        Initialize the scraper with the given URL.

        Args:
            url (str): The URL of the webpage to scrape.
        """
        self.url = url

    def setup_driver(self) -> uc.Chrome:
        """
        Set up the Chrome driver with the necessary options.

        Returns:
            uc.Chrome: An instance of the Chrome driver.
        """
        ua = UserAgent()
        user_agent = ua.random

        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"--user-agent={user_agent}")
        options.add_argument("--disable-blink-features=AutomationControlled")

        return uc.Chrome(options=options)

    def get_max_page(self, driver: uc.Chrome) -> int:
        """
        Get the maximum page number from the pagination elements.

        Args:
            driver (uc.Chrome): The Chrome driver instance.

        Returns:
            int: The maximum page number.
        """
        return self.__find_max_page(driver)

    def open_website(self, driver: uc.Chrome, url: str) -> None:
        """
        Open the website and accept cookies.

        Args:
            driver (uc.Chrome): The Chrome driver instance.
            url (str): The URL to open.
        """
        driver.get(url)

        time.sleep(3.46)
        self.__accept_cookies(driver)

    def scrap_data(self, driver: uc.Chrome, max_page: int) -> list:
        """
        Navigate and scrap the title and the link for each existing product.

        Args:
            driver (uc.Chrome): The Chrome driver instance.
            max_page (int): The maximum page number.

        Returns:
            list: The data scraped.
        """
        scraped_products_list = []

        for page_number in range(1, max_page + 1):
            product_cards = driver.find_elements(
                By.CSS_SELECTOR, ".ColListing--1fk1zey .ProductCardWrapper--6uxd5a"
            )

            print(f"Page number: {page_number}")

            for item in product_cards:
                random_float = random.uniform(2, 3)

                link_element = item.find_element(
                    By.CSS_SELECTOR, "a.ProductCardHiddenLink--v3c62m"
                )
                link = link_element.get_attribute("href")

                title_div = item.find_element(
                    By.CSS_SELECTOR, "div[id^='productCard_title__']"
                )
                item_title = title_div.text

                scraped_products_list.append(
                    {
                        "title": item_title,
                        "link": link,
                    }
                )

                print(f"Item scraped: {item_title}")

                time.sleep(random_float)

            try:
                next_page_button = driver.find_element(
                    By.CSS_SELECTOR,
                    f"button[data-testid='pageOption-link-testId-{page_number + 1}']",
                )
                driver.execute_script(
                    "arguments[0].scrollIntoView();", next_page_button
                )
                next_page_button.click()

                time.sleep(random_float)

            except NoSuchElementException:
                print(f"No more pages found. Stopped at page {page_number}")
                break

        time.sleep(random_float + 2)
        print(f"Longer sleep: {random_float + 2}")

    def __accept_cookies(self, driver: uc.Chrome) -> None:
        """
        Accept the cookies on the website.

        Args:
            driver (uc.Chrome): The Chrome driver instance.
        """
        try:
            accept_cookie_button = driver.find_element(
                By.ID, "onetrust-accept-btn-handler"
            )
            driver.execute_script(
                "arguments[0].scrollIntoView();", accept_cookie_button
            )
            accept_cookie_button.click()
        except Exception as e:
            print(f"Exception while accepting cookies: {e}")

    def __find_max_page(self, driver: uc.Chrome) -> int:
        """
        Find the maximum page number from the pagination elements.

        Args:
            driver (uc.Chrome): The Chrome driver instance.

        Returns:
            int: The maximum page number.
        """
        pagination = driver.find_elements(
            By.XPATH, "//button[starts-with(@data-testid, 'pageOption-link-testId-')]"
        )

        if pagination:
            return int(pagination[-1].text)
        return 1
