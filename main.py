import os

from dotenv import load_dotenv

from src.scraper_app.utils.data_loader import WebScraper
from src.scraper_app.utils.data_processor import ScrapProcessor

load_dotenv()

if __name__ == "__main__":
    url = os.environ["URL"]

    scraper = WebScraper(url)
    driver = scraper.setup_driver()
    scraper.open_website(driver, scraper.url)
    max_page = scraper.get_max_page(driver)
    scraped_data_list = scraper.scrap_data(driver, max_page)

    processor = ScrapProcessor(scraped_data_list)
    processed_data = processor.process_data()
    df = processor.to_dataframe()
    processor.save_to_csv(file_name="item_catalog_products.csv")
