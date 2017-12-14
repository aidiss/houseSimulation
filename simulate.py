"""Naval Fate.

Usage:
  simulate.py <project>


Options:
  -h --help     Show this screen.
  --version     Show version.
"""
from docopt import docopt
import subprocess

if __name__ == '__main__':
    arguments = docopt(__doc__, version='House simulator 0.1')
    project = arguments['<project>']
    res = subprocess.call(['python' , project + '.py'])
    print(res)