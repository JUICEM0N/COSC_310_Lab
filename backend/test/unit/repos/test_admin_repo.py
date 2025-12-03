import pytest
from backend.app.repositories.admin_repo import AdminRepository

@pytest.fixture
def repo(tmp_path):

    admin_repo = AdminRepository()
    admin_repo.users_path = tmp_path / "users.json"
    admin_repo.penalties_path = tmp_path / "penalties.json"
    admin_repo.admins_path = tmp_path / "admins.json"
    admin_repo.products_of_week_path = tmp_path / "products_of_week.json"
    admin_repo.discounts_path = tmp_path / "discounts.json"

    for path in [
        admin_repo.users_path,
        admin_repo.penalties_path,
        admin_repo.admins_path,
        admin_repo.products_of_week_path,
        admin_repo.discounts_path
    ]:
        path.write_text("[]")

    return admin_repo


def test_users(repo):
    repo.save_users([{"user_id": 1, "name": "Alice"}])
    users = repo.load_users()
    assert users == [{"user_id": 1, "name": "Alice"}]


def test_penalties(repo):
    repo.save_penalties([{"id": 1, "reason": "Late return"}])
    penalties = repo.load_penalties()
    assert penalties == [{"id": 1, "reason": "Late return"}]


def test_admins(repo):
    repo.save_admins([{"user_id": 99, "name": "Admin"}])
    admins = repo.load_admins()
    assert admins == [{"user_id": 99, "name": "Admin"}]


def test_products_of_week(repo):
    repo.save_products_of_week([101, 102])
    products = repo.load_products_of_week()
    assert products == [101, 102]


def test_discounts(repo):
    repo.save_discounts([{"product_id": 101, "discount_percent": 20.0}])
    discounts = repo.load_discounts()
    assert discounts == [{"product_id": 101, "discount_percent": 20.0}]
