import unittest
from datetime import date

from domain import Asset, QuantifiedPortfolio
from service import to_quantified_portfolio

#TODO what happens if the weights dont sum to one?
#TODO what happens if the prices are non positive?
#TODO what happens if the initial amount is non positive?
#TODO what happens if the date is not the same for all assets?
#TODO what happens if assets are empty?
#TODO what happens if there are repeats in the assets?

class TestToQuantifiedPortfolio(unittest.TestCase):
    def test_to_quantified_portfolio_calculates_quantities_of_assets(self):
        assets = [
            Asset(
                id="ASSET1",
                weight=0.4,
                price=100.0,
                date=date(2025, 1, 1),
            ),
            Asset(
                id="ASSET2",
                weight=0.6,
                price=100.0,
                date=date(2025, 1, 1),
            ),
        ]

        initial_amount = 1000.0
        portfolio = to_quantified_portfolio(
            assets=assets,
            initial_amount=initial_amount,
        )

        assert len(portfolio.assets) == 2

        asset1 = next(a for a in portfolio.assets if a.id == "ASSET1")
        asset2 = next(a for a in portfolio.assets if a.id == "ASSET2")

        assert asset1.quantity == 4.0
        assert asset2.quantity == 6.0


