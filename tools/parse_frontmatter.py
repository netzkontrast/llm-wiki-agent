import sys
import re
import json
import os

ALLOWED_DIRS = [os.path.abspath('wiki'), os.path.abspath('todo'), os.path.abspath('.agents')]

def main():
    if len(sys.argv) < 2:
        print(json.dumps({}))
        sys.exit(0)

    filepath = sys.argv[1]

    try:
        abs_filepath = os.path.abspath(filepath)
        is_allowed = any(abs_filepath.startswith(d) for d in ALLOWED_DIRS)
        if not is_allowed:
            raise Exception(f"SecurityError: Path {abs_filepath} is outside allowed directories.")
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except Exception:
        print(json.dumps({}))
        sys.exit(0)

    match = re.search(r'^\s*---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        print(json.dumps({}))
        sys.exit(0)

    frontmatter = match.group(1)
    result = {}

    lines = frontmatter.split('\n')
    current_key = None
    current_val = []
    in_multiline = False

    for line in lines:
        if not line.strip():
            continue

        kv_match = re.match(r'^\s*([\w-]+)\s*:\s*(.*)$', line)
        if kv_match:
            if current_key and current_val:
                 val_str = " ".join(current_val).strip()
                 result[current_key] = val_str

            key = kv_match.group(1)
            val = kv_match.group(2).strip()

            if val == '>':
                in_multiline = True
                current_key = key
                current_val = []
            else:
                in_multiline = False
                list_match = re.match(r'^\[(.*)\]$', val)
                if list_match:
                    items = list_match.group(1).split(',')
                    val = [item.strip().strip('"').strip("'") for item in items if item.strip()]
                elif val.startswith('"') and val.endswith('"'):
                    val = val[1:-1]
                elif val.startswith("'") and val.endswith("'"):
                    val = val[1:-1]

                result[key] = val
                current_key = None
        elif in_multiline:
            current_val.append(line.strip())

    if current_key and current_val:
        val_str = " ".join(current_val).strip()
        result[current_key] = val_str

    print(json.dumps(result))

if __name__ == '__main__':
    main()
