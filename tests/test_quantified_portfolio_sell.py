import unittest
from datetime import date

from domain import QuantifiedPortfolio, QuantifiedAsset


class TestQuantifiedPortfolioSell(unittest.TestCase):
    def setUp(self):
        self.day = date(2025, 1, 1)
        self.asset = QuantifiedAsset(
            id="ASSET1",
            quantity=10.0,
            price=100.0,
            date=self.day,
        )
        self.portfolio = QuantifiedPortfolio(assets=[self.asset])

    def test_sell_reduces_quantity_and_total_amount(self):
        # Sell 300 monetary units -> quantity reduced by 3
        self.portfolio.sell(asset_id="ASSET1", day=self.day, amount=300.0)

        self.assertAlmostEqual(self.asset.quantity, 7.0)
        self.assertAlmostEqual(self.portfolio.total(self.day), 700.0)

    def test_sell_more_than_available_raises_error(self):
        # Attempt to sell more than the total amount (1000)
        with self.assertRaises(ValueError):
            self.portfolio.sell(asset_id="ASSET1", day=self.day, amount=1500.0)

    def test_sell_nonexistent_asset_raises_error(self):
        with self.assertRaises(ValueError):
            self.portfolio.sell(asset_id="UNKNOWN", day=self.day, amount=100.0)

    def test_sell_negative_amount_raises_error(self):
        with self.assertRaises(ValueError):
            self.portfolio.sell(asset_id="ASSET1", day=self.day, amount=-100.0)

    def test_no_assets_in_date_range(self):
        """Test when no assets fall within the specified date range"""
        assets = [
            QuantifiedAsset(
                id="ASSET1",
                quantity=10.0,
                price=100.0,
                date=date(2025, 2, 1),
            ),
        ]
        portfolio = QuantifiedPortfolio(assets=assets)

        start_date = date(2025, 1, 1)
        end_date = date(2025, 1, 31)

        result = portfolio.daily_positions(start_date, end_date)

        self.assertEqual(len(result), 0)


