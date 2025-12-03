from datetime import date
from domain import QuantifiedPortfolio, QuantifiedAsset, Asset
from typing import List


def to_quantified_portfolio(
    assets: List[Asset],
    initial_amount: float,
) -> QuantifiedPortfolio:
    quantified_assets: List[QuantifiedAsset] = []
    # TODO make sure all assets have the same date
    for asset in assets:
        quantified_assets.append(asset.quantify(initial_amount))

    return QuantifiedPortfolio(assets=quantified_assets)
