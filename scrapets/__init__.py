__title__ = 'scrapets'
__version__ = "0.1.1"

import os
import sys

if __package__ is None :
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

# path = os.path.realpath(os.path.abspath(__file__))
# sys.path.insert(0, os.path.join(os.path.dirname(path), 'packages/'))
