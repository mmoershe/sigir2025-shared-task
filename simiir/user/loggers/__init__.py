# Enumerators for the different actions that can be performed.
# Solution from: http://stackoverflow.com/a/2182437
# Why? Encourages consistency. No typos. It either exists or it does not.

import sys
sys.path.append("..") # Adds higher directory to python modules path.

from simiir.utils.enum import Enum

Actions = Enum(['START','QUERY', 'SERP', 'SNIPPET', 'DOC', 'MARK', 'UTTERANCE', 'CSRP', 'RESPONSE', 'MARKRESPONSE', 'STOP', 'UNKNOWN'])