from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Dict, Optional
from collections import defaultdict

@dataclass
class Asset:
    #TODO Add constraints as values cant be negative or zero
    id: str
    weight: float
    price: float
    date: date

    def quantify(self, initial_amount: float) -> QuantifiedAsset:
        quantity = (self.weight * initial_amount) / self.price
        return QuantifiedAsset(
            id=self.id,
            quantity=quantity,
            price=self.price,
            date=self.date,
        )

@dataclass
class QuantifiedAsset:
    id: str
    quantity: float
    price: float
    date: date

    def amount(self) -> float:
        return self.price * self.quantity

@dataclass
class QuantifiedPortfolio:
    assets: List[QuantifiedAsset] = field(default_factory=list)
    _assets_by_date: Dict[date, List[QuantifiedAsset]] = field(default_factory=dict, init=False)

    def __post_init__(self):
        self._assets_by_date = defaultdict(list)
        for asset in self.assets:
            self._assets_by_date[asset.date].append(asset)

    def assets_on(self, day: date) -> List["QuantifiedAsset"]:
        return list(self._assets_by_date.get(day, []))

    def _asset_on(self, asset_id: str, day: date) -> Optional["QuantifiedAsset"]:
        return next(
            (asset for asset in self.assets_on(day) if asset.id == asset_id),
            None,
        )

    def total(self, day: date) -> float:
        return sum(asset.amount() for asset in self.assets_on(day))

    def sell(self, asset_id: str, day: date, amount: float) -> None:
        target_asset = self._asset_on(asset_id, day)

        if target_asset is None:
            raise ValueError(f"No asset with id '{asset_id}' on {day} to sell.")

        if amount < 0:
            raise ValueError("Amount to sell must be non-negative.")

        quantity_to_sell = amount / target_asset.price

        if quantity_to_sell > target_asset.quantity:
            raise ValueError("Cannot sell more than the available quantity.")

        target_asset.quantity -= quantity_to_sell

    def buy(self, asset_id: str, day: date, amount: float) -> None:
        target_asset = self._asset_on(asset_id, day)

        if target_asset is None:
            raise ValueError(f"No asset with id '{asset_id}' on {day} to buy.")

        if amount < 0:
            raise ValueError("Amount to buy must be non-negative.")

        quantity_to_buy = amount / target_asset.price
        target_asset.quantity += quantity_to_buy

    def weight(self, asset_id: str, date: date) -> float:
        target_asset = self._asset_on(asset_id, date)
        return target_asset.amount() / self.total(date)

    def daily_positions(self, start: date, end: date) -> Dict[date, DailyPosition]:
        total_days = (end - start).days
        all_days = [day for i in range(total_days + 1) if self.assets_on(day := start + timedelta(days=i)) != []]

        return {
            current_day: DailyPosition(
                total_amount=self.total(current_day),
                assets=self.assets_on(current_day),
            )
            for current_day in all_days
        }


@dataclass
class DailyPosition:
    total_amount: float
    assets: List[QuantifiedAsset]