from datetime import date, datetime
from typing import Optional, List, Union

import numpy as np
import pandas as pd
from sqlalchemy import and_, or_, MetaData, Table
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from .models import ExpectedMove


def convert_np(value):
    if isinstance(value, np.generic):
        return value.item()
    return value


def save_expected_move(db: Session, symbol: str, trade_date: datetime, expected_move: dict, move_type: str):
    # Check if a record with the same symbol, trade_date, and type already exists
    existing_record = db.query(ExpectedMove).filter(
        and_(
            ExpectedMove.symbol == symbol,
            ExpectedMove.trade_date == trade_date,
            ExpectedMove.type == move_type
        )
    ).first()

    if existing_record:
        # If the record already exists, we don't save it again
        return existing_record

    # If the record doesn't exist, we create a new one
    db_expected_move = ExpectedMove(
        symbol=symbol,
        trade_date=trade_date,
        underlying_price=convert_np(expected_move['underlying']),
        expected_move=convert_np(expected_move['expected_move']),
        sigma2_up=convert_np(expected_move['sigma2_up']),
        sigma1_up=convert_np(expected_move['sigma1_up']),
        sigma1_down=convert_np(expected_move['sigma1_down']),
        sigma2_down=convert_np(expected_move['sigma2_down']),
        timestamp=datetime.utcnow(),
        type=move_type
    )

    db.add(db_expected_move)
    try:
        db.commit()
        db.refresh(db_expected_move)
    except Exception as e:
        db.rollback()
        raise e
    return db_expected_move


def get_expected_moves(
    db: Session,
    symbol: Optional[Union[str, List[str]]] = None,
    trade_date_start: Optional[date] = None,
    trade_date_end: Optional[date] = None,
    move_type: Optional[Union[str, List[str]]] = None,
    limit: int = 100,
    offset: int = 0
) -> pd.DataFrame:
    query = db.query(ExpectedMove)

    filters = []

    # Handle symbol(s)
    if symbol:
        if isinstance(symbol, str):
            filters.append(ExpectedMove.symbol == symbol)
        elif isinstance(symbol, list):
            filters.append(ExpectedMove.symbol.in_(symbol))

    # Handle date range
    if trade_date_start:
        filters.append(ExpectedMove.trade_date >= trade_date_start)
    if trade_date_end:
        filters.append(ExpectedMove.trade_date <= trade_date_end)

    # Handle move_type(s)
    if move_type:
        if isinstance(move_type, str):
            filters.append(ExpectedMove.type == move_type)
        elif isinstance(move_type, list):
            filters.append(ExpectedMove.type.in_(move_type))

    if filters:
        query = query.filter(and_(*filters))

    # Apply limit and offset
    query = query.limit(limit).offset(offset)

    # Execute query
    results = query.all()

    # Convert to DataFrame
    if results:
        df = pd.DataFrame([
            {
                'id': result.id,
                'symbol': result.symbol,
                'trade_date': result.trade_date,
                'underlying_price': result.underlying_price,
                'expected_move': result.expected_move,
                'sigma2_up': result.sigma2_up,
                'sigma1_up': result.sigma1_up,
                'sigma1_down': result.sigma1_down,
                'sigma2_down': result.sigma2_down,
                'timestamp': result.timestamp,
                'type': result.type
            } for result in results
        ])
        return df
    else:
        # Return an empty DataFrame with the correct columns if no results
        return pd.DataFrame(columns=['id', 'symbol', 'trade_date', 'underlying_price', 'expected_move',
                                     'sigma2_up', 'sigma1_up', 'sigma1_down', 'sigma2_down', 'timestamp', 'type'])


def insert_dataframe_to_postgres(db: Session, df: pd.DataFrame, table_name: str, unique_columns: list):
    # Get the table object
    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=db.bind)

    # Remove the 'id' column from the DataFrame if it exists
    if 'id' in df.columns:
        df = df.drop(columns=['id'])

    # Create the insert statement
    stmt = insert(table)

    # Add the ON CONFLICT clause
    stmt = stmt.on_conflict_do_nothing(index_elements=unique_columns)

    # Convert DataFrame to list of dictionaries
    data = df.to_dict(orient='records')

    try:
        # Execute the bulk insert
        db.execute(stmt, data)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

