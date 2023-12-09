from datetime import datetime, timedelta
import locale
import getopt
import sys


def usage():
    print("""
Usage: python script_name.py [options]

Options:
  -h, --help          Show this help message and exit
  -i, --input         Specify input file
""")


def get_timestamp(raw_log_entry: str) -> str:
    # get the string between [ and ], replace comma with dot (locale)
    return raw_log_entry[raw_log_entry.find('[') + 1:raw_log_entry.find(']')].lstrip(" +")


def parse(timestamp: str) -> (datetime, bool):
    try:
        parsed = datetime.strptime(timestamp, "%b%d %H:%M")
    except ValueError:
        parsed = datetime.strptime(timestamp, "%S,%f")
    return parsed


test_input = "07.12.2023"
test_date = datetime.strptime(test_input, "%d.%m.%Y")


def process_line(raw_line: str, base_time: datetime) -> str:
    line = raw_line
    line = line.rstrip()
    raw_timestamp = get_timestamp(line)
    try:
        message = line.split(']', 1)[1]
    except IndexError:
        return line
    parsed_time = parse(raw_timestamp)
    offset = timedelta(seconds=parsed_time.second, microseconds=parsed_time.microsecond)
    parsed_time = base_time + offset
    converted_timestamp = datetime.strftime(parsed_time, "%a %b%-d %H:%M %Y")
    return "[{}]{}".format(converted_timestamp, message)


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:", ["help", "input="])
    except getopt.GetoptError as err:
        print(err)
        sys.exit()
    if len(opts) == 0:
        usage()
        sys.exit()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-w", "--weekday"):
            print("Dzisiejszy dzień tygodnia: {}".format(find_weekday(date)))
    with open("../dmesg.h.log", "r") as file:
        base_time = None
        for line in file:
            print(process_line(line, test_date))


if __name__ == "__main__":
    locale.setlocale(locale.LC_TIME, "pl_PL")
    main()

