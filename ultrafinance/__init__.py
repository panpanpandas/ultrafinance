""" ultrafinance package """
import os, re, sys

import logging
LOG = logging.getLogger()

# library paths
"""
LIB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'lib')
for entry in os.listdir(LIB):
    filePath = os.path.join(LIB, entry)
    if os.path.isfile(filePath) and re.search(r".*\.(zip|egg|tar\.gz|tgz)$", filePath):
        LOG.debug("...appending library %s to sys.path" % filePath)
        sys.path.append(filePath)
"""