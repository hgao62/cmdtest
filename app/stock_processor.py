from abc import ABC, abstractmethod
from typing import List
from datetime import datetime
from stock_unit import StockUnit
from typing import Dict

class StockProcessor(ABC):

    @abstractmethod
    def vest_stocks(self, data: List[StockUnit], target_date: datetime) -> Dict[str, StockUnit]:
        pass