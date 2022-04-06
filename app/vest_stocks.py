from datetime import datetime
from stock_processor import StockProcessor
from app_logger import AppLogger
from stock_unit import StockUnit
from typing import List, Dict
from collections import defaultdict


class VestStocks(StockProcessor, AppLogger):

    def __init__(self):
        super().__init__()
        self.data = None
        self.target_date = None
        self.vested_stocks = []  # type: List[StockUnit]
        self.cancelled_stocks = []  # type: List[StockUnit]
        self.award_stocks = defaultdict(int)

    def _preprocess_stocks(self) ->None:
        for stock in self.data:
            if stock.vest == 'CANCEL':
                self.cancelled_stocks.append(stock)
            elif stock.vest == 'VEST':
                self.vested_stocks.append(stock)

    def _process_vest(self) -> Dict[str, StockUnit]:

        vesting_schedule = {}

        for stock in self.vested_stocks:

            key = f'{stock.employee_id}_{stock.award_id}'

            if stock.event_date <= self.target_date:
                self.award_stocks[stock.award_id] += stock.quantity
                if key in vesting_schedule:
                    vesting_schedule[key].quantity += stock.quantity
                else:
                    vesting_schedule[key] = StockUnit(stock.vest, stock.employee_id, stock.employee_name,
                                                      stock.award_id, stock.event_date, stock.quantity)
            else:
                if key not in vesting_schedule:
                    vesting_schedule[key] = StockUnit(stock.vest, stock.employee_id, stock.employee_name,
                                                      stock.award_id, stock.event_date, 0)

        return vesting_schedule

    def _process_cancels(self, vested_stocks: Dict[str, StockUnit]) -> Dict[str, StockUnit]:
        for stock in self.cancelled_stocks:
            if stock.event_date <= self.target_date:
                if stock.quantity > self.award_stocks[stock.award_id]:
                    self.logger.info(f'Invalid cancel event {str(stock)}')
                else:
                    key = f'{stock.employee_id}_{stock.award_id}'
                    if key in vested_stocks:
                        vested_stocks[key].quantity -= stock.quantity

        return vested_stocks

    def vest_stocks(self, data: List[StockUnit], target_date: datetime) -> Dict[str, StockUnit]:
        self.data = data
        self.target_date = target_date
        self._preprocess_stocks()
        vest_schedule = self._process_vest()
        if len(self.cancelled_stocks) > 0:
            vest_schedule = self._process_cancels(vest_schedule)

        return vest_schedule

