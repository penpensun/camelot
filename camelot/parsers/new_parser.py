from __future__ import division
import os
import logging
import warnings

import numpy as np
import pandas as pd

from .base import BaseParser
from ..core import TextEdges, Table
from ..utils import (text_in_bbox, get_table_index, compute_accuracy,
                     compute_whitespace)

class NewParser(BaseParser):

    def __init__(self, y_tol=0.5):
        self.y_tol = y_tol;
        pass;
    
    def extract_table(self, filename):
        self._generate_layout(filename, {});
        #print(self.horizontal_text);
        self.align_lines();

    def align_lines (self):
        lines = [];
        merge_count = [];
        sorted_hor_text = sorted(self.horizontal_text, key = lambda x: -x.y0);
        current_line_y = sorted_hor_text[0].y0;
        current_line = [sorted_hor_text[0]]
        current_merge_count = 1;
        for index in range(1, len(sorted_hor_text)):
            if (current_line_y - sorted_hor_text[index].y0) <= self.y_tol:
                current_line.append(sorted_hor_text[index]);
                current_line_y = ( current_line_y * (len(current_line)-1) + sorted_hor_text[index].y0)\
                    / len(current_line);
                current_merge_count += 1;
            else:
                lines.append(current_line);
                current_line = [sorted_hor_text[index]];
                current_line_y = sorted_hor_text[index].y0;
                merge_count.append(current_merge_count);
                current_merge_count = 1;

        for i in range(0,len(lines)):
            print('line: '+str(i)+' merge count: '+str(merge_count[i]));
            for item in lines[i]:
                print(item.get_text()[:-1]);

            


        



