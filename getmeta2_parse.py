import os
import sys
import __future__
import numpy as np
import log_parser
import namespace

Parser = log_parser.LogParser()


ID = sys.argv[1]
try:
        Parser.parse_video_metainfo(ID)
except Exception as inst:
        print (type(inst), inst.args)#, inst)
        print ('SKIPPED ID={}'.format(ID))
        
