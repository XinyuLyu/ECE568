# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 16:18:59 2018

@author: admin
"""

# coding=utf-8
import json 
data1={"Next Day Value":1100}
# =============================================================================
# data2={ "Meta Data": {
#         "1: Symbol": "MSFT",
#         "2: Indicator": "On Balance Volume (OBV)",
#         "3: Last Refreshed": "2018-04-20",
#         "4: Interval": "weekly",
#         "5: Time Zone": "US/Eastern Time"
#     },
#     "Technical Analysis: OBV": {
#         "2018-04-20": {
#             "OBV": "156547648.0000"
#         },
#         "2018-04-13": {
#             "OBV": "33759353.0000"
#      }
#         }
#     }
# =============================================================================
in_json = json.dumps(data1)
print in_json
#json = json.dumps(data)
#print json.dumps(data, sort_keys=True, indent=1, separators=(',', ': '))
#print json
#num1 = argv[1]
#num2 = argv[2]
#sum = int(num1) + int(num2)
#print sum