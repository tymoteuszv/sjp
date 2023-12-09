from datetime import datetime, timedelta
import re
import locale
from zoneinfo import ZoneInfo


class TimeConverter:
    UTC = ZoneInfo('UTC')
    CET = ZoneInfo('CET')
    TIME_UNITS = ["d", "h", "m", "s"]
    DATE_FORMAT = "%a, %-d %b %Y, %X %Z"

    def __init__(self):
        locale.setlocale(locale.LC_TIME, "pl_PL")
        while True:
            user_input = input(
                'Podaj różnicę czasu w formacie XXd XXh XXm XXs, gdzie kolejność i odstępy nie mają znaczenia'
                'a wszystkie argumenty są opcjonalne\n')
            if not self.is_valid_input(user_input):
                print("Niepoprawnie wprowadzone dane")
            else:
                break
        parsed_input = self.parse_input_to_dict(user_input)
        self.timedelta_from_input = self.to_timedelta(parsed_input)
        self.utc_time = datetime.now(tz=TimeConverter.UTC)
        self.cet_time = self.utc_time.astimezone(TimeConverter.CET)
        self.pretty_print()

    @staticmethod
    def is_valid_input(user_input) -> bool:
        regular_expression = rf"^([0-9]+[{''.join(TimeConverter.TIME_UNITS)}]){{0,4}}$"
        for character in TimeConverter.TIME_UNITS:
            if user_input.count(character) > 1:
                return False
        return bool(re.match(regular_expression, user_input))

    @staticmethod
    def parse_input_to_dict(user_input) -> dict[str, int]:
        parsed_time_dict = {}
        start_index = 0
        for end_index, character in enumerate(user_input):
            if character in TimeConverter.TIME_UNITS:
                parsed_time_dict[character] = int(user_input[start_index:end_index])
                start_index = end_index + 1
        for character in TimeConverter.TIME_UNITS:
            if character not in parsed_time_dict:
                parsed_time_dict[character] = 0
        return parsed_time_dict

    @staticmethod
    def to_timedelta(time_dict) -> timedelta:
        return timedelta(days=time_dict.get("d", 0), hours=time_dict.get("h", 0),
                         minutes=time_dict.get("m", 0), seconds=time_dict.get("s", 0))

    def pretty_print(self) -> None:
        print("{:10}{}".format("teraz:", self.cet_time.strftime(TimeConverter.DATE_FORMAT)))
        print("{:10}{}".format("GMT:", self.utc_time.strftime(TimeConverter.DATE_FORMAT)).replace("UTC", "GMT"))
        print("{:10}{}".format("wcześniej:",
                               (self.cet_time - self.timedelta_from_input).strftime(TimeConverter.DATE_FORMAT)))
        print("{:10}{}".format("później:",
                               (self.cet_time + self.timedelta_from_input).strftime(TimeConverter.DATE_FORMAT)))


if __name__ == "__main__":
    TimeConverter()
