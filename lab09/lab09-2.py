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
    """Find the weekday of a given date and return it as a string"""
    return date.strftime("%A")


def find_month_weekday(date):
    """Find the weekday of the first day of the month of a given date and return it as a string"""
    date = date.replace(day=1)
    return find_weekday(date)


def print_month(date):
    """Print the calendar for the month of a given date"""
    cal = calendar.TextCalendar()
    cal.prmonth(date.year, date.month)


def parse_input_date(query: str):
    """Parse input date in dd.mm.yyyy format and return it as a datetime object"""
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
    """Set the locale and execute the task specified in the lab instructions"""
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
