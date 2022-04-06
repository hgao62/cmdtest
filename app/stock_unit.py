from functools import total_ordering
from datetime import date
from typing import Optional
from dateutil.parser import parse
from app_logger import AppLogger


@total_ordering
class StockUnit(AppLogger):

    def __init__(self, event: str, employee_id: str, employee_name: str,
                 award_id: str, event_date: Optional[date] = None,
                 quantity: Optional[int] = 0):

        super().__init__()
        self.vest = event
        self.employee_id = employee_id
        self.employee_name = employee_name
        self.award_id = award_id
        self._event_date = event_date
        self._quantity = quantity
        self._try_convert_date()
        self._try_convert_qty()

    def _try_convert_date(self):
        if isinstance(self.event_date, str):
            try:
                self._event_date = parse(self.event_date)
            except ValueError:
                self.event_date = date(1900,0,0)
                self.logger.Exception(f'cannot convert {self.event_date} to datetime')

    def _try_convert_qty(self):
        if isinstance(self.quantity, str):
            try:
                self.quantity = int(self._quantity)
            except ValueError:
                self.quantity = 0
                self.logger.exception(f'cannot convert {self.quantity} to integer')

    @property
    def event_date(self):
        return self._event_date

    @event_date.setter
    def event_date(self, value):
        if isinstance(value, str):
            try:
                self._event_date = parse(value)
            except ValueError:
                self._event_date = date(1900,0,0)
                self.logger.Exception(f'cannot convert {value} to datetime')

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        try:
            self._quantity = int(value)
        except ValueError:
            self._quantity = 0
            self.logger.Exception(f'could not convert {value} to int. default to 0')

    def __eq__(self, other):
        return (self.employee_id, self.award_id) == (other.employee_id, other.award_id)

    def __lt__(self, other):
        return (self.employee_id, self.award_id ) < (other.employee_id, other.award_id)

    def __str__(self):
        try:
            display_cols = [self.employee_id, self.employee_name, self.award_id, str(self.quantity)]
            str_display = ','.join(display_cols)
        except Exception:
            str_display = ''
            self.logger.exception(f'Convert StockUnit class to string failed for employee:{self.employee_id } award_id:{self.employee_id}')
        return str_display
