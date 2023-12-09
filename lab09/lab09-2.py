import getopt
import sys
import calendar
import locale
from datetime import datetime


def usage():
    print("""
Usage: python script_name.py [options]

Options:
  -h, --help          Show this help message and exit
  -w, --weekday       Find and display the current weekday
  -s, --first_weekday Find and display the weekday of the first day of the current month
  -c, --show_calendar Display the calendar for the current month
""")


def find_weekday(date):
    return date.strftime("%A")


def find_month_weekday(date):
    date = date.replace(day=1)
    return find_weekday(date)


def print_month(date):
    cal = calendar.TextCalendar()
    cal.prmonth(date.year, date.month)


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
        opts, args = getopt.getopt(sys.argv[1:], "hwsc", ["help", "weekday", "first_weekday", "show_calendar"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit()
    if len(opts) == 0:
        usage()
        sys.exit()
    date = parse_input_date("Podaj datę w formacie dd.mm.rrrr\n")

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-w", "--weekday"):
            print("Dzisiejszy dzień tygodnia: {}".format(find_weekday(date)))
        elif o in ("-s", "--first_weekday"):
            print("Pierwszy dzień tego miesiąca to {}".format(find_month_weekday(date)))
        elif o in ("-c", "--show_calendar"):
            print_month(date)


if __name__ == "__main__":
    main()
