from datetime import datetime, timedelta
import locale
import getopt
import sys
from zoneinfo import ZoneInfo


def usage():
    print("""
Usage: python script_name.py [options]

example usage for the log from dream.ist:
-i dmesg.t.log -d 30.06.2022.18.59.32.CEST

Options:
  -h, --help          Show this help message and exit
  -i, --input         Specify input file
  -d, --date          Specify date offset in dd.mm.rrrr.hh.mm.ss.zzz format (zzz is timezone like UTC or CET or CEST)
""")


def get_timestamp(raw_log_entry: str) -> str:
    """Get timestamp in seconds.microseconds format from a single line between [ and ], return it as a string"""
    return raw_log_entry[raw_log_entry.find('[') + 1:raw_log_entry.find(']')].lstrip(" +")


def parse(timestamp: str) -> (datetime, bool):
    """Parse timestamp in format seconds.microseconds and return timedelta object"""
    seconds, microseconds = timestamp.split(".")
    parsed = timedelta(seconds=int(seconds), microseconds=int(microseconds))
    return parsed


test_input = "07.12.2023"
test_date = datetime.strptime(test_input, "%d.%m.%Y")


def process_line(raw_line: str, base_time: datetime) -> str:
    """Process a single line of log and return it with the timestamp converted to CET"""
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
    parsed_time.replace(fold=1)
    converted_timestamp = parsed_time.astimezone(tz=ZoneInfo("Europe/Warsaw")).strftime("%a %b %-d %H:%M:%S %Y")
    return "[{}]{}".format(converted_timestamp, message)


def main():
    """Set the locale and execute the task specified in the lab instructions"""
    locale.setlocale(locale.LC_TIME, "pl_PL")
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
                offset_date = datetime.strptime(unparsed_date, "%d.%m.%Y.%H.%M.%S.%Z")
                offset_date = offset_date.astimezone(tz=ZoneInfo("UTC"))
            except ValueError as err:
                print(err)
                usage()
                sys.exit()
    if offset_date is None:
        raise ValueError("Offset date not set")
    for line in input_stream:
        print(process_line(line, offset_date))


if __name__ == "__main__":

    main()
