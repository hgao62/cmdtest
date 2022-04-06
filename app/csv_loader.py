import os
import csv
from typing import List, Union
from data_loader import DataLoader
from app_logger import AppLogger
from stock_unit import StockUnit

class CSVLoader(DataLoader, AppLogger):

    def __init__(self):
        super().__init__()

    def load_data(self, **kwargs) -> Union[List[StockUnit], List]:
        file_path = kwargs['file_path']
        field_names = kwargs['headers']
        delim = kwargs['delim']
        res = []
        if os.path.exists(file_path):
            try:
                with open(file_path, mode='r') as csv_file:
                    csv_reader = csv.DictReader(csv_file, fieldnames=field_names, delimiter=delim, escapechar='\\')
                    for row in csv_reader:
                        attributes = [row[x] for x in field_names]
                        stock_unit = StockUnit(*attributes)
                        res.append(stock_unit)
                    return res
            except Exception:
                self.logger.exception(f'Load data from csv file {file_path} failed')
        return res
