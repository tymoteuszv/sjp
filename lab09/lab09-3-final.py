import getopt
import sys
import locale
from datetime import datetime, timedelta


def usage():
    print("""
Usage: python script_name.py [options]

Options:
  -h, --help          Show this help message and exit
  -e, --elapsed       Calculate elapsed days from a specific date
  -t, --thursdays     Count the number of Thursdays between two dates
  -l, --leap_days     Count the number of leap days between two dates
""")


def order_dates(date_1, date_2):
    if date_1 > date_2:
        return date_2, date_1
    return date_1, date_2


def between_count_weekday(start: datetime, end: datetime, isoweekday: int):
    # make a generator object of days BETWEEN dates (the (start,end) interval)
    dates_between = (start + timedelta(x + 1) for x in range((end - start).days - 1))
    counter = 0
    for date in dates_between:
        if date.isoweekday() == isoweekday:
            counter += 1
    return counter


def between_count_yearday(start, end, month, day):
    # make a generator object of days BETWEEN dates (the (start,end) interval)
    dates_between = (start + timedelta(x + 1) for x in range((end - start).days - 1))
    counter = 0
    for date in dates_between:
        if date.month == month and date.day == day:
            counter += 1
    return counter


def parse_input_date(query: str):
    while True:
        unparsed_date = input(query)
        try:
            output = datetime.strptime(unparsed_date, "%d.%m.%Y")
            break
        except ValueError as err:
            print(err)
            print(query)
    return output


def main():
    locale.setlocale(locale.LC_TIME, "pl_PL")
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hetl", ["help", "elapsed", "thursdays", "leap_days"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit()
    if len(opts) == 0:
        usage()
        sys.exit()
    first_date = parse_input_date("Podaj pierwszą datę w formacie dd.mm.rrrr\n")
    second_date = parse_input_date("Podaj drugą datę w formacie dd.mm.rrrr\n")
    start, end = order_dates(first_date, second_date)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-e", "--elapsed"):
            days_elapsed = (end - start).days
            print(f"Days elapsed between {start.date()} and {end.date()}: {days_elapsed} days")
        elif o in ("-t", "--thursdays"):
            thursdays_count = between_count_weekday(start, end, 4)  # 4 to czwartek
            print(f"Number of Thursdays between {start.date()} and {end.date()}: {thursdays_count}")
        elif o in ("-l", "--leap_days"):
            leap_days_count = between_count_yearday(start, end, 2, 29)
            print(f"Number of leap days between {start.date()} and {end.date()}: {leap_days_count}")


if __name__ == "__main__":
    main()
