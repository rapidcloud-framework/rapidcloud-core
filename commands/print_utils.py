# #!/usr/bin/env python3

__author__ = "Igor Royzis"
__license__ = "MIT"


import json
import logging
import os
from tabulate import tabulate

logger = logging.getLogger(__name__)

def print_grid_from_json(json_list, cols=None, totals=None, title=""):
    print(f"\n{title} COUNT: {len(json_list)}")
    # print(json.dumps(json_list, indent=2, default=str))
    
    # make sure json is not empty
    if len(json_list) == 0:
        return
    
    if cols is None:
        # use all cols
        cols = json_list[0].keys()
    else:
        # remove non-existing cols
        new_cols = []
        for col in cols:
            if col in json_list[0]:
                new_cols.append(col)
        cols = new_cols

    grid = []
    tot = {}
    i = 1
    for item in json_list:
        row = [i]
        for col in cols:
            if col in item:
                row.append(item[col])
        if totals is not None:
            for col in totals:
                if col in tot:
                    tot[col] += item[col]
                else:
                    tot[col] = item[col]
        grid.append(row)
        i += 1

    if totals is not None:
        grid.append("")
        tot_row = [""]
        for col in cols:
            if col in tot:
                tot_row.append(tot[col])
            else:
                tot_row.append("")
        grid.append(tot_row)
        grid.append("")
    print("")
    print(tabulate(grid, cols))
    print("\n")


def info(msg, title=None):
    if os.getenv('RAPIDCLOUD_TEST_MODE') == "true":
        if title:
            print("--------------------------------------")
            print(title)
            print("--------------------------------------")
        if type(msg) == dict:
            print(json.dumps(msg, indent=2, default=str))
        else:
            print(msg)

