import pytest
from unittest.mock import patch
from fastapi import HTTPException
from backend.app.services.items_service import ItemsService
from backend.app.schemas.item import Item, ItemCreate, ItemUpdate

def test_list_items_maps_fields_correctly():
    raw_items = [
        {
            "id": "123",
            "product_name": "Laptop",
            "product_category": "Electronics",
            "discounted_price": "900",
            "actual_price": "1000",
            "discount_percentage": "10%",
            "rating": "4.5",
            "rating_count": "200",
            "about_product": "Good laptop",
            "user_id": "U1",
            "user_name": "John",
            "review_id": "R1",
            "review_title": "Nice",
            "review_content": "Good product",
            "img_link": "img.jpg",
            "product_link": "product.com",
            "quantity": 10
        }
    ]

    with patch("backend.app.services.items_service.ProductsRepo") as mock_repo:
        mock_repo.load_all.return_value = raw_items

        items = ItemsService.list_items()

        assert len(items) == 1
        assert items[0]["id"] == "123"
        assert items[0]["product_name"] == "Laptop"
        mock_repo.load_all.assert_called_once()

def test_create_item_success():
    payload = ItemCreate(
        product_id="temp",
        category="Electronics",
        product_name="Mouse",
        discounted_price="10",
        actual_price="20",
        discount_percentage="50%",
        rating="4",
        rating_count="10",
        about_product="Nice mouse",
        user_id="U1",
        user_name="Bob",
        review_id="R2",
        review_title="Great",
        review_content="Very good",
        img_link="img2.jpg",
        product_link="product.com/mouse",
        quantity= 67
    )

    with patch("backend.app.services.items_service.ProductsRepo") as mock_repo:
        mock_repo.load_all.return_value = []
        mock_repo.save_all.return_value = None

        item = ItemsService.create_item(payload)

        assert item.product_name == "Mouse"
        assert item.product_id is not None
        mock_repo.save_all.assert_called_once()

def test_create_item_id_collision():
    payload = ItemCreate(
        product_id="temp",
        category="X",
        product_name="Test",
        discounted_price="1",
        actual_price="2",
        discount_percentage="10%",
        rating="5",
        rating_count="1",
        about_product="desc",
        user_id="U1",
        user_name="tester",
        review_id="rev1",
        review_title="title",
        review_content="content",
        img_link="img.jpg",
        product_link="link",
        quantity=41
    )

    with patch("backend.app.services.items_service.ProductsRepo") as mock_repo:
        mock_repo.load_all.return_value = [{"product_id": "collision"}]

        with patch("uuid.uuid4", return_value="collision"):
            with pytest.raises(HTTPException) as exc:
                ItemsService.create_item(payload)

            assert exc.value.status_code == 409

def test_get_item_by_id_success():
    with patch("backend.app.services.items_service.ProductsRepo") as mock_repo:
        mock_repo.product_exists.return_value = True
        mock_repo.load_all.return_value = [{
            "product_id": "123",
            "product_name": "Laptop",
            "category": "Electronics",
            "discounted_price": "1",
            "actual_price": "2",
            "discount_percentage": "1%",
            "rating": "5",
            "rating_count": "10",
            "about_product": "desc",
            "user_id": "U",
            "user_name": "N",
            "review_id": "R",
            "review_title": "T",
            "review_content": "C",
            "img_link": "i",
            "product_link": "l",
            "quantity": 8
        }]

        item = ItemsService.get_item_by_id("123")
        assert item.product_id == "123"

def test_get_item_by_id_not_found():
    with patch("backend.app.services.items_service.ProductsRepo") as mock_repo:
        mock_repo.product_exists.return_value = False

        with pytest.raises(HTTPException):
            ItemsService.get_item_by_id("BAD")

def test_update_item_success():
    payload = ItemUpdate(
        product_id="abc",
        category="Electronics",
        product_name="Keyboard",
        discounted_price="30",
        actual_price="50",
        discount_percentage="20%",
        rating="4",
        rating_count="50",
        about_product="Mechanical keys",
        user_id="U1",
        user_name="Bob",
        review_id="R2",
        review_title="Great!",
        review_content="Solid keyboard",
        img_link="keyboard.jpg",
        product_link="product.com/keyboard",
        quantity=6
    )

    old_item = {
        "product_id": "abc",
        "product_name": "Old",
        "category": "OldCat",
        "discounted_price": "1",
        "actual_price": "2",
        "discount_percentage": "1%",
        "rating": "1",
        "rating_count": "1",
        "about_product": "O",
        "user_id": "U",
        "user_name": "N",
        "review_id": "R",
        "review_title": "T",
        "review_content": "C",
        "img_link": "i",
        "product_link": "l",
        "quantity": "H"
    }

    with patch("backend.app.services.items_service.ProductsRepo") as mock_repo:
        mock_repo.product_exists.return_value = True
        mock_repo.load_all.return_value = [old_item]
        mock_repo.save_all.return_value = None

        updated = ItemsService.update_item("abc", payload)

        assert updated.product_name == "Keyboard"

def test_update_item_overwrites_all_fields():
    old_item = {
        "product_id": "aaa",
        "product_name": "OLD",
        "category": "OLD",
        "discounted_price": "9",
        "actual_price": "19",
        "discount_percentage": "90%",
        "rating": "1",
        "rating_count": "1",
        "about_product": "OLD",
        "user_id": "OLD",
        "user_name": "OLD",
        "review_id": "OLD",
        "review_title": "OLD",
        "review_content": "OLD",
        "img_link": "old.jpg",
        "product_link": "old",
        "quantity": 5
    }

    new_data = ItemUpdate(
        product_id="aaa",
        category="NEWCAT",
        product_name="NEW",
        discounted_price="10",
        actual_price="20",
        discount_percentage="5%",
        rating="5",
        rating_count="999",
        about_product="NEW DESC",
        user_id="U2",
        user_name="NewUser",
        review_id="RNEW",
        review_title="Great",
        review_content="New review!",
        img_link="new.jpg",
        product_link="new",
        quantity=7
    )

    with patch("backend.app.services.items_service.ProductsRepo") as mock_repo:
        mock_repo.product_exists.return_value = True
        mock_repo.load_all.return_value = [old_item.copy()]
        mock_repo.save_all.return_value = None

        updated = ItemsService.update_item("aaa", new_data)

        assert updated.product_name == "NEW"

def test_update_item_not_found_does_not_save():
    payload = ItemUpdate(
        product_id="missing",
        category="Y",
        product_name="X",
        discounted_price="1",
        actual_price="2",
        discount_percentage="10%",
        rating="5",
        rating_count="10",
        about_product="ok",
        user_id="U1",
        user_name="Bob",
        review_id="R1",
        review_title="T",
        review_content="C",
        img_link="img.jpg",
        product_link="lnk",
        quantity=7
    )

    with patch("backend.app.services.items_service.ProductsRepo") as mock_repo:
        mock_repo.product_exists.return_value = False

        with pytest.raises(HTTPException):
            ItemsService.update_item("missing", payload)

        mock_repo.save_all.assert_not_called()


def test_delete_item_success():
    with patch("backend.app.services.items_service.ProductsRepo") as mock_repo:
        mock_repo.product_exists.return_value = True
        mock_repo.load_all.return_value = [{"product_id": "123"}]
        mock_repo.save_all.return_value = None

        ItemsService.delete_item("123")

        mock_repo.save_all.assert_called_once()


def test_delete_item_not_found():
    with patch("backend.app.services.items_service.ProductsRepo") as mock_repo:
        mock_repo.load_all.return_value = [{"id": "1"}]

        with pytest.raises(HTTPException) as exc:
            ItemsService.delete_item("X")

        assert exc.value.status_code == 404