from pathlib import Path
import os

"""
This script converts all the jupyter notebook to html files in a dir and subdirs 
"""

files = Path('.').glob("**/*")
files_ipynb = [ i for i in (list(files)) if str(i).endswith('.ipynb')]
for i in files_ipynb:
    if not str(i.parent).split("/")[-1] == '.ipynb_checkpoints':
        _ = f'jupyter nbconvert --to html {i}'
        try:
            os.system(_)
        except:
            pass
