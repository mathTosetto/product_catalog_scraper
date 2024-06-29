import os
import re

import pandas as pd

from datetime import datetime


class ScrapProcessor:
    """A class to process and save scraped data."""

    def __init__(self, scraped_products_list: list) -> None:
        """
        Initialize the processor with the scraped products list.

        Args:
            scraped_products_list (list): List of scraped product dictionaries.
        """
        self.scraped_products_list = scraped_products_list

    def process_data(self) -> list:
        """
        Process the scraped data to extract product details.

        Returns:
            list: Treated data
        """
        for item in self.scraped_products_list:
            item["product_id"] = self._extract_product_id(item["link"])
            item["product_name"], item["price"] = self._split_title(item["title"])
            item["execution_time"] = datetime.now().strftime(r"%Y-%m-%d")

        return self.scraped_products_list

    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert the processed data to a Pandas DataFrame.

        Returns:
            pd.DataFrame: Return a dataframe.
        """
        df = pd.DataFrame(self.scraped_products_list)
        return df[["product_id", "product_name", "price", "link", "execution_time"]]

    def save_to_csv(
        self,
        file_name: str,
        output_path: str = "data/02_output/",
        **kwargs,
    ) -> None:
        """
        Save the processed data to a CSV file.

        Args:
            csv_path (str): The directory path to save the CSV file.
            file_name (str): The name of the CSV file.
            **kwargs: Additional arguments to pass to `pandas.DataFrame.to_csv`.
        """
        df = self.to_dataframe()

        os.makedirs(output_path, exist_ok=True)

        full_path = os.path.join(output_path, file_name)

        df.to_csv(full_path, index=False, **kwargs)
        print(f"Data saved to {full_path}")

    def _extract_product_id(self, link: str) -> str:
        """
        Extract the product ID from the link.

        Args:
            link (str): Product URL.

        Returns:
            str: The product ID.
        """
        match = re.search(r"id-(\d+)", link)
        return match.group(1) if match else None

    def _split_title(self, title: str) -> tuple:
        """
        Split the title into product name and price.

        Args:
            title (str): The product title and price.

        Returns:
            tuple: The product title, price.
        """
        return title.split(", ", 1)
