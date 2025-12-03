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
