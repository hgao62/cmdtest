import os
from datetime import datetime
import argparse
from os.path import dirname, abspath
import configparser
from typing import List, Dict

from csv_loader import CSVLoader
from vest_stocks import VestStocks
from display_result_sort import DisplayResultSort
from stock_processor import StockProcessor
from data_loader import DataLoader
from stock_unit import StockUnit
from display_result import DisplayResult

ROOT_DIR = dirname(dirname(abspath(__file__)))


class App:

    def __init__(self, stock_processor: StockProcessor, data_loader: DataLoader, display_format: DisplayResult):
        self.data_loader = data_loader
        self.stock_processor = stock_processor
        self.display_format = display_format
        
    def load_data(self, **kwargs) -> List[StockUnit]:
        return self.data_loader.load_data(**kwargs)

    def process_data(self, stocks: List[StockUnit], target_date: datetime) -> Dict[str, StockUnit]:
        return self.stock_processor.vest_stocks(stocks, target_date)

    def display(self, data: Dict[str, StockUnit]) -> None:
        self.display_format.display_output(data)


def prepare_input() -> dict:

    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('file_name', type=str, help='input file name')
    parser.add_argument('target_date', type=str, help='target date of vesting')
    args = parser.parse_args()
    file_name = args.file_name
    file_path = os.path.join(ROOT_DIR, file_name)
    target_date = datetime.strptime(args.target_date, '%Y-%m-%d')

    config = configparser.ConfigParser()
    config.read('config.ini')

    headers = config['input_info']['headers'].split(',')
    delim = config['input_info']['delim']

    return {'file_path': file_path, 'target_date': target_date, 'headers': headers, 'delim': delim}


if __name__ == '__main__':
    parameters = prepare_input()
    file_path = parameters['file_path']
    headers = parameters['headers']
    delim = parameters['delim']
    target_date = parameters['target_date']
    app = App(VestStocks(), CSVLoader(), DisplayResultSort())
    data = app.load_data(file_path=file_path, headers=headers, delim=delim)
    res = app.process_data(data, target_date)
    app.display(res)
