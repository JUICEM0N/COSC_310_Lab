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
        }
    ]

    with patch("backend.app.services.items_service.ProductsRepo") as mock_repo:
        mock_repo.load_all.return_value = raw_items

        items = ItemsService.list_items()

        assert len(items) == 1
        assert items[0].id == "123"
        assert items[0].product_name == "Laptop"
        mock_repo.load_all.assert_called_once()

def test_create_item_success():
    payload = ItemCreate(
        product_name="Mouse",
        product_category="Electronics",
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
        product_link="product.com/mouse"
    )

    with patch("backend.app.services.items_service.ProductsRepo") as mock_repo:
        mock_repo.load_all.return_value = []
        mock_repo.save_all.return_value = None

        item = ItemsService.create_item(payload)

        assert item.product_name == "Mouse"
        assert item.id is not None  # UUID assigned
        mock_repo.save_all.assert_called_once()

def test_create_item_id_collision():
    payload = ItemCreate(
        product_name="Test",
        product_category="X",
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
        product_link="link"
    )

    with patch("backend.app.services.items_service.ProductsRepo") as mock_repo:
        mock_repo.load_all.return_value = [{"id": "collision"}]

        with patch("uuid.uuid4", return_value="collision"):
            with pytest.raises(HTTPException) as exc:
                ItemsService.create_item(payload)

            assert exc.value.status_code == 409

def test_get_item_by_id_success():
    with patch("backend.app.services.items_service.ProductsRepo") as mock_repo:
        mock_repo.load_all.return_value = [{"id": "123", "product_name": "Laptop"}]

        item = ItemsService.get_item_by_id("123")
        assert item.id == "123"


def test_get_item_by_id_not_found():
    with patch("backend.app.services.items_service.ProductsRepo") as mock_repo:
        mock_repo.load_all.return_value = []

        with pytest.raises(HTTPException) as exc:
            ItemsService.get_item_by_id("BAD")

        assert exc.value.status_code == 404

def test_update_item_success():
    payload = ItemUpdate(
        product_name="Keyboard",
        product_category="Electronics",
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
        product_link="product.com/keyboard"
    )

    old_item = {
        "id": "abc",
        "product_name": "Old",
        "product_category": "OldCat",
        "discounted_price": "99",
        "actual_price": "199",
        "discount_percentage": "80%",
        "rating": "1",
        "rating_count": "5",
        "about_product": "Bad",
        "user_id": "U0",
        "user_name": "Someone",
        "review_id": "RX",
        "review_title": "Old",
        "review_content": "Old review",
        "img_link": "old.jpg",
        "product_link": "oldlink"
    }

    with patch("backend.app.services.items_service.ProductsRepo") as mock_repo:
        mock_repo.load_all.return_value = [old_item]
        mock_repo.save_all.return_value = None

        updated = ItemsService.update_item("abc", payload)

        assert updated.id == "abc"
        assert updated.product_name == "Keyboard"
        assert updated.product_category == "Electronics"
        assert updated.discounted_price == "30"
        mock_repo.save_all.assert_called_once()

def test_update_item_overwrites_all_fields():
    old_item = {
        "id": "aaa",
        "product_name": "OLD",
        "product_category": "OLD",
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
        "product_link": "old"
    }

    new_data = ItemUpdate(
        product_name="NEW",
        product_category="NEWCAT",
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
        product_link="new"
    )

    with patch("backend.app.services.items_service.ProductsRepo") as mock_repo:
        mock_repo.load_all.return_value = [old_item.copy()]
        mock_repo.save_all.return_value = None

        updated = ItemsService.update_item("aaa", new_data)

        assert updated.product_name == "NEW"
        assert updated.review_content == "New review!"
        assert updated.product_link == "new"

def test_update_item_not_found_does_not_save():
    payload = ItemUpdate(
        product_name="X",
        product_category="Y",
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
        product_link="lnk"
    )

    with patch("backend.app.services.items_service.ProductsRepo") as mock_repo:
        mock_repo.load_all.return_value = []

        with pytest.raises(HTTPException):
            ItemsService.update_item("missing", payload)

        mock_repo.save_all.assert_not_called()

def test_delete_item_success():
    with patch("backend.app.services.items_service.ProductsRepo") as mock_repo:
        mock_repo.load_all.return_value = [{"id": "123"}]
        mock_repo.save_all.return_value = None

        ItemsService.delete_item("123")

        mock_repo.save_all.assert_called_once()

def test_delete_item_not_found():
    with patch("backend.app.services.items_service.ProductsRepo") as mock_repo:
        mock_repo.load_all.return_value = [{"id": "1"}]

        with pytest.raises(HTTPException) as exc:
            ItemsService.delete_item("X")

        assert exc.value.status_code == 404