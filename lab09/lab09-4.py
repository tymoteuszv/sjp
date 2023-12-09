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
  -d, --date          Specify date offset in dd.mm.rrrr.hh.mm.ss format
""")


def get_timestamp(raw_log_entry: str) -> str:
    # get the string between [ and ], replace comma with dot (locale)
    return raw_log_entry[raw_log_entry.find('[') + 1:raw_log_entry.find(']')].lstrip(" +")


def parse(timestamp: str) -> (datetime, bool):
    try:
        parsed = datetime.strptime(timestamp, "%b%d %H:%M")
    except ValueError:
        seconds, microseconds = timestamp.split(".")
        parsed = timedelta(seconds=int(seconds), microseconds=int(microseconds))
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
    offset = parsed_time
    parsed_time = base_time + offset
    converted_timestamp = datetime.strftime(parsed_time, "%a %b %-d %H:%M:%S %Y")
    return "[{}]{}".format(converted_timestamp, message)


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:d:", ["help", "input=", "date="])
    except getopt.GetoptError as err:
        print(err)
        sys.exit()
    if len(opts) == 0:
        usage()
        sys.exit()
    offset_date = None
    input_stream = sys.stdin
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-i", "--input"):
            input_stream = open(a, "r")
        elif o in ("-d", "--date"):
            unparsed_date = a
            try:
                offset_date = datetime.strptime(unparsed_date, "%d.%m.%Y.%H.%M.%S")
            except ValueError as err:
                print(err)
                usage()
                sys.exit()
    if offset_date is None:
        raise ValueError("Offset date not set")
    for line in input_stream:
        print(process_line(line, offset_date))


if __name__ == "__main__":
    locale.setlocale(locale.LC_TIME, "pl_PL")
    main()

