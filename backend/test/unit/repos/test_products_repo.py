import json
import pytest
from pathlib import Path
from backend.app.repositories.products_repo import ProductsRepo

@pytest.fixture
def temp_products_file(tmp_path, monkeypatch):
    """Creates a temporary amazon_cad.json for isolation."""
    temp_json = tmp_path / "amazon_cad.json"
    temp_json.write_text("[]") 

    monkeypatch.setattr(
        "backend.app.repositories.products_repo.DATA_PATH",
        temp_json
    )
    return temp_json

def read_json(path: Path):
    return json.loads(path.read_text())

def test_load_products_reads_file(temp_products_file):
    temp_products_file.write_text(json.dumps([
        {"product_id": "A1", "name": "Laptop"}
    ]))

    products = ProductsRepo.load_products()
    assert len(products) == 1
    assert products[0]["product_id"] == "A1"

def test_get_product_returns_correct_item(temp_products_file):
    temp_products_file.write_text(json.dumps([
        {"product_id": "X9", "name": "Keyboard"}
    ]))

    prod = ProductsRepo.get_products("X9")
    assert prod["name"] == "Keyboard"

def test_get_product_returns_none_if_missing(temp_products_file):
    temp_products_file.write_text(json.dumps([]))
    prod = ProductsRepo.get_products("NOT_REAL")
    assert prod is None

def test_load_all_returns_empty_when_file_missing(tmp_path, monkeypatch):
    fake_path = tmp_path / "amazon_cad.json" 
    monkeypatch.setattr(
        "backend.app.repositories.products_repo.DATA_PATH",
        fake_path
    )

    with pytest.raises(FileNotFoundError):
        ProductsRepo.load_all()

def test_load_all_reads_data(temp_products_file):
    temp_products_file.write_text(json.dumps([
        {"product_id": "B2", "price": 12.99}
    ]))

    items = ProductsRepo.load_all()
    assert items == [{"product_id": "B2", "price": 12.99}]

def test_save_all_overwrites_file_safely(temp_products_file):
    ProductsRepo.save_all([
        {"product_id": "T3", "rating": 5.0}
    ])

    data = read_json(temp_products_file)
    assert data == [{"product_id": "T3", "rating": 5.0}]