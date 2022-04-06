from abc import ABC, abstractmethod
from typing import List,Union
from stock_unit import StockUnit

class DataLoader(ABC):

    @abstractmethod
    def load_data(self, **kwargs) -> Union[List[StockUnit], List]:
        pass