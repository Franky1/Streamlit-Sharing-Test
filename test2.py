import glob
import shutil
import subprocess


def get_subprocess_pipdeptree(fullpath=None):
    if fullpath:
        return subprocess.getstatusoutput(rf'{fullpath} --json')
    else:
        return subprocess.getstatusoutput(r'pipdeptree --json')

# wh = shutil.which("pipdeptree")
# print(wh)
# s, r = get_subprocess_pipdeptree(wh)
# print(s)

results = glob.glob('C:/WinPython/**/pipdeptree*', recursive=True)
print(results)
