import subprocess
import shutil
from typing import Dict, List, Tuple, Union
TypeTupleOut = Tuple[int, str]

def get_subprocess_pipdeptree(fullpath=None) -> TypeTupleOut:
    if fullpath:
        return subprocess.getstatusoutput(rf'{fullpath} --json')
    else:
        return subprocess.getstatusoutput(r'pipdeptree --json')

wh = shutil.which("pipdeptree")
print(wh)
s, r = get_subprocess_pipdeptree(wh)
print(s)
