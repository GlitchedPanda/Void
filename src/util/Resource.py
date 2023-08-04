import sys
from pathlib import Path

is_exe = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

def get_log_path():
    if is_exe:
        return Path(sys.executable).parent / 'Void.log'
    else:
        return Path(sys.argv[0]).parent.parent / "Void.log"
    