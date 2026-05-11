"""Tests for starter.api.orders."""

from __future__ import annotations

from fastapi.testclient import TestClient

from starter.api.main import app
from starter.api.orders import create_order
from starter.shared import Err, Ok


class TestCreateOrder:
    def test_returns_ok_with_formatted_order_when_input_is_valid(self) -> None:
        result = create_order(amount_cents=12345, customer_id="cust_1")
        assert isinstance(result, Ok)
        assert result.value.amount_cents == 12345
        assert result.value.formatted_amount == "$123.45"
        assert result.value.customer_id == "cust_1"
        assert result.value.id.startswith("ord_")

    def test_rejects_negative_amounts(self) -> None:
        result = create_order(amount_cents=-1, customer_id="cust_1")
        assert isinstance(result, Err)
        assert "non-negative" in result.error

    def test_rejects_empty_customer_id(self) -> None:
        result = create_order(amount_cents=100, customer_id="")
        assert isinstance(result, Err)

    def test_rejects_whitespace_only_customer_id(self) -> None:
        result = create_order(amount_cents=100, customer_id="   ")
        assert isinstance(result, Err)


class TestOrdersHttpEndpoint:
    def test_creates_order_returns_201(self) -> None:
        client = TestClient(app)
        response = client.post("/orders", json={"amount_cents": 100, "customer_id": "c_1"})
        assert response.status_code == 201
        body = response.json()
        assert body["amount_cents"] == 100
        assert body["formatted_amount"] == "$1.00"

    def test_rejects_invalid_amount_returns_422(self) -> None:
        # Pydantic catches negative-int via ge=0 before our handler runs
        client = TestClient(app)
        response = client.post("/orders", json={"amount_cents": -1, "customer_id": "c_1"})
        assert response.status_code == 422

    def test_rejects_blank_customer_id_returns_422(self) -> None:
        client = TestClient(app)
        response = client.post("/orders", json={"amount_cents": 100, "customer_id": ""})
        assert response.status_code == 422


class TestHealthEndpoint:
    def test_health_returns_ok(self) -> None:
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
