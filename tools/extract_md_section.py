import sys
import re
import os

ALLOWED_DIRS = [os.path.abspath('wiki'), os.path.abspath('todo'), os.path.abspath('.agents')]

def main():
    if len(sys.argv) < 3:
        print("Usage: python extract_md_section.py <filepath> <target_header>")
        sys.exit(1)

    filepath = sys.argv[1]
    target_header = sys.argv[2]

    try:
        abs_filepath = os.path.abspath(filepath)
        is_allowed = any(abs_filepath.startswith(d) for d in ALLOWED_DIRS)
        if not is_allowed:
            raise Exception(f"SecurityError: Path {abs_filepath} is outside allowed directories.")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

    in_section = False
    buffer = []

    # Identify target_header level
    target_match = re.match(r'^(#{1,6})\s+', target_header)
    target_level = len(target_match.group(1)) if target_match else 0

    try:
        with open(filepath, 'r') as f:
            for line in f:
                header_match = re.match(r'^(#{1,6})\s+(.*)', line)

                if in_section:
                    if header_match:
                        level = len(header_match.group(1))
                        if level <= target_level:
                            break
                    buffer.append(line)
                else:
                    # check if current line is the target header or matches the target exactly
                    if line.strip() == target_header.strip() or (header_match and line.startswith(target_header)):
                        in_section = True
                        buffer.append(line)

        print(''.join(buffer))
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == '__main__':
    main()
