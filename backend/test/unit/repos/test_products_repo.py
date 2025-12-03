import json
import pytest
from pathlib import Path
from backend.app.repositories.products_repo import ProductsRepo

@pytest.fixture
def temp_products_file(tmp_path, monkeypatch):
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

@pytest.fixture
def mock_products(monkeypatch):
    data = [
        {
            "product_name": "Apple iPhone 13",
            "discounted_price": "$799.00",
            "category": "Electronics|Mobile",
            "rating": "4.5"
        },
        {
            "product_name": "Samsung TV 55 Inch",
            "discounted_price": "$699.00",
            "category": "Electronics|TV",
            "rating": "4.0"
        },
        {
            "product_name": "Juicer Mixer Grinder",
            "discounted_price": "$59.00",
            "category": "Home|Kitchen",
            "rating": "|"
        }
    ]

    def fake_load_products():
        return data

    monkeypatch.setattr(ProductsRepo, "load_products", fake_load_products)
    return data

def test_search_products_found(mock_products):
    results = ProductsRepo.search_products("iphone")
    assert len(results) == 1
    assert results[0]["product_name"] == "Apple iPhone 13"

def test_search_products_not_found(mock_products):
    with pytest.raises(Exception) as e:
        ProductsRepo.search_products("nonexistent")
    assert "don't have nonexistent" in str(e.value)

def test_filter_by_keyword(mock_products):
    results = ProductsRepo.filter_products(keyword="tv")
    assert len(results) == 1
    assert "Samsung TV" in results[0]["product_name"]

def test_filter_by_min_price(mock_products):
    results = ProductsRepo.filter_products(min_price=700)
    assert len(results) == 1
    assert "iPhone" in results[0]["product_name"]

def test_filter_by_max_price(mock_products):
    results = ProductsRepo.filter_products(max_price=100)
    assert len(results) == 1
    assert "Juicer" in results[0]["product_name"]

def test_filter_by_category(mock_products):
    results = ProductsRepo.filter_products(category="mobile")
    assert len(results) == 1
    assert "iPhone" in results[0]["product_name"]

def test_filter_by_rating_valid(mock_products):
    results = ProductsRepo.filter_products(rating=4.2)
    assert len(results) == 1
    assert "iPhone" in results[0]["product_name"]

def test_filter_by_rating_ignores_invalid(mock_products):
    results = ProductsRepo.filter_products(rating=0)
    assert len(results) == 2

def test_filter_products_no_match(mock_products):
    with pytest.raises(Exception) as e:
        ProductsRepo.filter_products(keyword="xyz")
    assert "No products found matching the filter criteria." in str(e.value)
