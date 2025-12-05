from datetime import datetime, date
from typing import List

import pandas as pd

from domain import Holding


def read_weights_sheet(
    file_path: str = "datos.xlsx",
    sheet_name: str = "weights",
) -> pd.DataFrame:
    return pd.read_excel(file_path, sheet_name=sheet_name, header=0)

def _to_date(value) -> date:
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    # Fallback: try to parse ISO-like strings (e.g. "2025-01-01")
    return datetime.fromisoformat(str(value)).date()


def assets_from_weights_sheet(
    file_path: str = "datos.xlsx",
    sheet_name: str = "weights",
    weight_column: str = "portafolio 1",
) -> List[Holding]:
    df = read_weights_sheet(file_path=file_path, sheet_name=sheet_name)
    prices = pd.read_excel('datos.xlsx', sheet_name='Precios',  index_col=0, parse_dates=True)

    # Use positional indexing for date (first column) and asset_id (second column)
    date_column_index = 0
    id_column_index = 1

    assets: List[Holding] = []
    for _, row in df.iterrows():
        asset = Holding(
            id=str(row.iloc[id_column_index]),
            weight=float(row[weight_column]),
            #price=float(df.loc[asset_date.strftime("%d-%m-%Y"), str(row.iloc[id_column_index])]),
            price=float(prices.loc[row.iloc[date_column_index], str(row.iloc[id_column_index])]),
            date=_to_date(row.iloc[date_column_index]),
        )
        assets.append(asset)

    return assets



def main() -> None:
    assets = assets_from_weights_sheet()
    for asset in assets:
        print(asset)

if __name__ == "__main__":
    main()
