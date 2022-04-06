from display_result import DisplayResult

class DisplayResultSort(DisplayResult):

    def display_output(self, data: dict) -> None:
        res = sorted(list(data.values()))
        ret = list(map(str, res))
        print('\n'.join(ret))