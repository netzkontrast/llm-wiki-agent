import sys
from pathlib import Path
import re

content = Path(".decompose_context.md").read_text()
# We are supposed to run /wiki-decompose but that's an agent command.
# For now, I will manually create the plan file.
