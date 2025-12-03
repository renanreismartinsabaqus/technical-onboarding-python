import unittest
from datetime import date

from domain import QuantifiedPortfolio, QuantifiedAsset


class TestQuantifiedPortfolioBuy(unittest.TestCase):
    def setUp(self):
        self.day = date(2025, 1, 1)
        self.asset = QuantifiedAsset(
            id="ASSET1",
            quantity=10.0,
            price=100.0,
            date=self.day,
        )
        self.portfolio = QuantifiedPortfolio(assets=[self.asset])

    def test_buy_increases_quantity_and_total_amount(self):
        # Buy 300 monetary units -> quantity increased by 3
        self.portfolio.buy(asset_id="ASSET1", day=self.day, amount=300.0)

        self.assertAlmostEqual(self.asset.quantity, 13.0)
        self.assertAlmostEqual(self.portfolio.total(self.day), 1300.0)

    def test_buy_nonexistent_asset_raises_error(self):
        with self.assertRaises(ValueError):
            self.portfolio.buy(asset_id="UNKNOWN", day=self.day, amount=100.0)

    def test_buy_negative_amount_raises_error(self):
        with self.assertRaises(ValueError):
            self.portfolio.buy(asset_id="ASSET1", day=self.day, amount=-100.0)

    def test_buy_zero_amount(self):
        # Buy 0 amount should not change quantity
        initial_quantity = self.asset.quantity
        self.portfolio.buy(asset_id="ASSET1", day=self.day, amount=0.0)

        self.assertAlmostEqual(self.asset.quantity, initial_quantity)
        self.assertAlmostEqual(self.portfolio.total(self.day), 1000.0)

    def test_buy_on_different_date_raises_error(self):
        # Try to buy on a date where the asset doesn't exist
        different_day = date(2025, 1, 2)
        with self.assertRaises(ValueError):
            self.portfolio.buy(asset_id="ASSET1", day=different_day, amount=100.0)

    def test_buy_multiple_times(self):
        # Buy multiple times should accumulate
        self.portfolio.buy(asset_id="ASSET1", day=self.day, amount=200.0)
        self.portfolio.buy(asset_id="ASSET1", day=self.day, amount=300.0)

        self.assertAlmostEqual(self.asset.quantity, 15.0)
        self.assertAlmostEqual(self.portfolio.total(self.day), 1500.0)

    def test_buy_with_multiple_assets_same_date(self):
        # Test buying when multiple assets exist on the same date
        assets = [
            QuantifiedAsset(
                id="ASSET1",
                quantity=10.0,
                price=100.0,
                date=self.day,
            ),
            QuantifiedAsset(
                id="ASSET2",
                quantity=5.0,
                price=200.0,
                date=self.day,
            ),
        ]
        portfolio = QuantifiedPortfolio(assets=assets)

        # Buy only ASSET1
        portfolio.buy(asset_id="ASSET1", day=self.day, amount=500.0)

        # Verify ASSET1 increased, ASSET2 unchanged
        asset1 = next(asset for asset in portfolio.assets_on(self.day) if asset.id == "ASSET1")
        asset2 = next(asset for asset in portfolio.assets_on(self.day) if asset.id == "ASSET2")

        self.assertAlmostEqual(asset1.quantity, 15.0)
        self.assertAlmostEqual(asset2.quantity, 5.0)
        self.assertAlmostEqual(portfolio.total(self.day), 2500.0)  # 15*100 + 5*200


