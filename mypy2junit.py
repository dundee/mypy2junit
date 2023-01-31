import argparse
import fileinput
import re
import sys
from typing import List, Tuple

__version__ = '1.9.0'

RESULT_REGEX = re.compile(
    # errors -> error if found only one error
    r'Found (?P<count>\d+) errors?'
)
REPLACES = {
    ord('<'): '&lt;',
    ord('"'): '&quot;',
    ord('&'): '&amp;',
}


def process_lines(lines: List[str]) -> Tuple[str, bool]:
    result = {'count': '0', 'total_files': '0'}
    failures = []
    output = ''

    for line in lines:
        if line.startswith('Found '):
            match = re.match(
                RESULT_REGEX,
                line
            )
            if match:
                result = match.groupdict()
            continue

        # example: Success: no issues found in 9 source files
        if line.startswith('Success: no issues found in '):
            break

        file_, line, type_, *message = line.split(':')
        type_ = type_.strip()

        if type_ == 'error':
            failures.append((file_, line, type_, message))

    output += f"""<?xml version="1.0" encoding="utf-8"?>
<testsuite errors="0" failures="{result['count']}" name="" skips="0" tests="{result['count']}" time="0.0">"""

    for failure in failures:
        msg = f"{failure[0]}:{failure[1]}: {failure[2]}: "
        msg += ':'.join(failure[3]).strip().translate(REPLACES)
        output += f"""
    <testcase classname="{failure[0]}" name="{failure[0]}:{failure[1]}" file="{failure[0]}" line="{failure[1]}" time="0.0">
        <failure message="Mypy error on {failure[0]}:{failure[1]}" type="WARNING" file="{failure[0]}" line="{failure[1]}">{msg}</failure>
    </testcase>"""

    output += """
</testsuite>"""

    return output, int(result['count']) == 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', metavar='FILE', nargs='*', help='files to read, if empty, stdin is used')
    parser.add_argument('--output',
                        type=str,
                        dest='output',
                        help='Filename to output to')
    parser.add_argument('--tee', action='store_true')

    args = parser.parse_args()
    if args.tee and not args.output:
        print("You must specify --output if using --tee")
        return -1

    output, status = process_lines(
        list(fileinput.input(files=args.files if len(args.files) > 0 else ('-', )))
    )

    if args.output:
        with open(args.output, 'w') as file:
            file.write(output)

    if not args.output or args.tee:
        print(
            output
        )

    if not status:
        sys.exit(1)


if __name__ == "__main__":
    main()
