import pytest
from unittest.mock import patch
from backend.app.services.user_dashboard_service import UserDashboardService

def test_get_user_dashboard_success():
    transactions = [
        {"id": 1, "date": "2024-01-10"},
        {"id": 2, "date": "2024-03-05"},
        {"id": 3, "date": "2023-12-01"},
    ]

    penalties = [
        {"id": "p1", "amount": 25.0},
        {"id": "p2", "amount": 10.0},
    ]

    with patch("backend.app.services.user_dashboard_service.TransactionsRepo") as mock_trans, \
        patch("backend.app.services.user_dashboard_service.PenaltiesRepo") as mock_pen:

        mock_trans.get_transactions_by_user.return_value = transactions
        mock_pen.get_penalties_by_user.return_value = penalties

        dashboard = UserDashboardService.get_user_dashboard(5)

        assert dashboard["user_id"] == 5

        expected_sorted = [
            {"id": 2, "date": "2024-03-05"},
            {"id": 1, "date": "2024-01-10"},
            {"id": 3, "date": "2023-12-01"},
        ]
        assert dashboard["transactions"] == expected_sorted


        assert dashboard["penalties"] == penalties

        mock_trans.get_transactions_by_user.assert_called_once_with(5)
        mock_pen.get_penalties_by_user.assert_called_once_with(5)


def test_get_user_dashboard_missing_dates():
    transactions = [
        {"id": 1, "date": ""},
        {"id": 2, "date": "2024-01-05"},
        {"id": 3},
    ]

    penalties = []

    with patch("backend.app.services.user_dashboard_service.TransactionsRepo") as mock_trans, \
        patch("backend.app.services.user_dashboard_service.PenaltiesRepo") as mock_pen:

        mock_trans.get_transactions_by_user.return_value = transactions
        mock_pen.get_penalties_by_user.return_value = penalties

        dashboard = UserDashboardService.get_user_dashboard(9)

        sorted_trans = dashboard["transactions"]
        assert sorted_trans[0]["id"] == 2 
        assert sorted_trans[-1]["id"] in (1, 3)


def test_get_user_dashboard_empty_results():
    with patch("backend.app.services.user_dashboard_service.TransactionsRepo") as mock_trans, \
        patch("backend.app.services.user_dashboard_service.PenaltiesRepo") as mock_pen:

        mock_trans.get_transactions_by_user.return_value = []
        mock_pen.get_penalties_by_user.return_value = []

        dashboard = UserDashboardService.get_user_dashboard(1)

        assert dashboard["transactions"] == []
        assert dashboard["penalties"] == []
        assert dashboard["user_id"] == 1
