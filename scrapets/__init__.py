__title__ = 'scrapets'
__version__="0.1.0"

import os
import sys

path = os.path.realpath(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(path), 'packages/'))
