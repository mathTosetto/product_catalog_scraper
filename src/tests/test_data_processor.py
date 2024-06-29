import os
import pytest

import pandas as pd

from scraper_app.utils.data_processor import ScrapProcessor


@pytest.fixture
def sample_data():
    return [
        {"title": "Product A, €1.99", "link": "https://example.com/product-a-id-12345"},
        {"title": "Product B, €2.99", "link": "https://example.com/product-b-id-67890"},
    ]


@pytest.fixture
def processor(sample_data):
    return ScrapProcessor(sample_data)


def test_process_data(processor):
    processor.process_data()
    for item in processor.scraped_products_list:
        assert "product_id" in item
        assert "product_name" in item
        assert "price" in item
        assert "execution_time" in item


def test_to_dataframe(processor):
    processor.process_data()
    df = processor.to_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == [
        "product_id",
        "product_name",
        "price",
        "link",
        "execution_time",
    ]
    assert len(df) == 2


def test_save_to_csv(processor):
    processor.process_data()

    test_output_path = "data/02_output"
    test_file_name = "test_products.csv"
    full_path = os.path.join(test_output_path, test_file_name)

    processor.save_to_csv(test_file_name)
    assert os.path.isfile(full_path)

    df = pd.read_csv(full_path)
    assert len(df) == 2
    assert list(df.columns) == [
        "product_id",
        "product_name",
        "price",
        "link",
        "execution_time",
    ]

    if os.path.isfile(full_path):
        os.remove(full_path)
