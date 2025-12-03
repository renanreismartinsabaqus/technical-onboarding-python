import unittest
from datetime import date

from domain import QuantifiedPortfolio, QuantifiedAsset


class TestQuantifiedPortfolioDailyPositions(unittest.TestCase):
    def test_single_date_single_asset(self):
        """Test calculation with a single asset on a single date"""
        asset = QuantifiedAsset(
            id="ASSET1",
            quantity=10.0,
            price=100.0,
            date=date(2025, 1, 1),
        )
        portfolio = QuantifiedPortfolio(assets=[asset])

        start_date = date(2025, 1, 1)
        end_date = date(2025, 1, 1)

        result = portfolio.daily_positions(start_date, end_date)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[date(2025, 1, 1)].total_amount, 1000.0)
        self.assertEqual(result[date(2025, 1, 1)].assets[0].id, "ASSET1")

    def test_single_date_multiple_assets(self):
        """Test calculation with multiple assets on the same date"""
        assets = [
            QuantifiedAsset(
                id="ASSET1",
                quantity=4.0,
                price=100.0,
                date=date(2025, 1, 1),
            ),
            QuantifiedAsset(
                id="ASSET2",
                quantity=6.0,
                price=100.0,
                date=date(2025, 1, 1),
            ),
        ]
        portfolio = QuantifiedPortfolio(assets=assets)

        start_date = date(2025, 1, 1)
        end_date = date(2025, 1, 1)

        result = portfolio.daily_positions(start_date, end_date)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[date(2025, 1, 1)].total_amount, 1000.0)  # 4*100 + 6*100
        self.assertEqual(len(result[date(2025, 1, 1)].assets), 2)

    def test_multiple_dates(self):
        """Test calculation with assets on multiple dates"""
        assets = [
            QuantifiedAsset(
                id="ASSET1",
                quantity=10.0,
                price=100.0,
                date=date(2025, 1, 1),
            ),
            QuantifiedAsset(
                id="ASSET2",
                quantity=5.0,
                price=200.0,
                date=date(2025, 1, 2),
            ),
            QuantifiedAsset(
                id="ASSET3",
                quantity=3.0,
                price=150.0,
                date=date(2025, 1, 3),
            ),
        ]
        portfolio = QuantifiedPortfolio(assets=assets)

        start_date = date(2025, 1, 1)
        end_date = date(2025, 1, 3)

        result = portfolio.daily_positions(start_date, end_date)

        self.assertEqual(len(result), 3)

        self.assertEqual(result[date(2025, 1, 1)].total_amount, 1000.0)
        self.assertEqual(result[date(2025, 1, 2)].total_amount, 1000.0)
        self.assertEqual(result[date(2025, 1, 3)].total_amount, 450.0)

    def test_date_range_filtering(self):
        """Test that only assets within the date range are included"""
        assets = [
            QuantifiedAsset(
                id="ASSET1",
                quantity=10.0,
                price=100.0,
                date=date(2025, 1, 1),
            ),
            QuantifiedAsset(
                id="ASSET2",
                quantity=5.0,
                price=200.0,
                date=date(2025, 1, 2),
            ),
            QuantifiedAsset(
                id="ASSET3",
                quantity=3.0,
                price=150.0,
                date=date(2025, 1, 5),
            ),
        ]
        portfolio = QuantifiedPortfolio(assets=assets)

        start_date = date(2025, 1, 2)
        end_date = date(2025, 1, 2)

        result = portfolio.daily_positions(start_date, end_date)

        # Should only include assets from 2025-1-2
        self.assertEqual(len(result), 1)
        self.assertEqual(result[date(2025, 1, 2)].total_amount, 1000.0)

    def test_multiple_assets_same_date(self):
        """Test grouping multiple assets on the same date"""
        assets = [
            QuantifiedAsset(
                id="ASSET1",
                quantity=2.0,
                price=50.0,
                date=date(2025, 1, 1),
            ),
            QuantifiedAsset(
                id="ASSET2",
                quantity=3.0,
                price=100.0,
                date=date(2025, 1, 1),
            ),
            QuantifiedAsset(
                id="ASSET3",
                quantity=1.0,
                price=200.0,
                date=date(2025, 1, 1),
            ),
        ]
        portfolio = QuantifiedPortfolio(assets=assets)

        start_date = date(2025, 1, 1)
        end_date = date(2025, 1, 1)

        result = portfolio.daily_positions(start_date, end_date)

        self.assertEqual(len(result), 1)
        projection = result[date(2025, 1, 1)]
        self.assertEqual(projection.total_amount, 600.0)  # 2*50 + 3*100 + 1*200
        self.assertEqual(len(projection.assets), 3)

    def test_empty_portfolio(self):
        """Test with an empty portfolio"""
        portfolio = QuantifiedPortfolio(assets=[])

        start_date = date(2025, 1, 1)
        end_date = date(2025, 1, 31)

        result = portfolio.daily_positions(start_date, end_date)

        self.assertEqual(len(result), 0)


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
