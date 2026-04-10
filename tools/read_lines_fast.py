import sys
import itertools
import os

ALLOWED_DIRS = [os.path.abspath('wiki'), os.path.abspath('todo'), os.path.abspath('.agents')]

def main():
    if len(sys.argv) < 4:
        print("Usage: python read_lines_fast.py <filepath> <start_line> <end_line>")
        sys.exit(1)

    filepath = sys.argv[1]
    start_line = int(sys.argv[2])
    end_line = int(sys.argv[3])

    try:
        abs_filepath = os.path.abspath(filepath)
        is_allowed = any(abs_filepath.startswith(d) for d in ALLOWED_DIRS)
        if not is_allowed:
            raise Exception(f"SecurityError: Path {abs_filepath} is outside allowed directories.")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(filepath, 'r') as f:
            lines = list(itertools.islice(f, start_line, end_line))
            for line in lines:
                print(line, end='')
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == '__main__':
    main()
