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

from ..image_processing import adaptive_threshold;
from ..image_processing import find_lines;

from .lattice import Lattice;

class NewParser(BaseParser):

    def __init__(self, y_tol=0.5):
        self.y_tol = y_tol;
        pass;
    
    def extract_table(self, filename):
        self._generate_layout(filename, {});
        #print(self.horizontal_text);
        self.align_lines();


    def test_find_lines(self, filename, imagename):
        lattice_parser = Lattice();
        lattice_parser._generate_layout(filename, {});
        #lattice_parser._generate_image();
        #print(lattice_parser.imagename);
        image, threshold = adaptive_threshold(imagename, \
            process_background=False, 
            blocksize=lattice_parser.threshold_blocksize, 
            c = lattice_parser.threshold_constant)
        #print(image);
        print('type of image: ', type(image));
        print('shape of image: ', image.shape);
        from PIL import Image;
        converted_img = Image.fromarray(image);
        converted_img.save('./converted_img.png');
        #converted_img.show();
        converted_thresh_img = Image.fromarray(threshold);
        converted_thresh_img.save('./converted_thresh_img.png');
        #converted_thresh_img.show();
        print('threshold.shape: ', threshold.shape);
        #fine line
        mask, segment = find_lines(threshold, regions= None, direction = 'horizontal', \
            line_scale=  lattice_parser.line_scale, iterations = lattice_parser.iterations);
        print('mask: ');
        print('type of mask: ', type(mask));
        print('shape of mask: ', mask.shape);
        findline_thresh_img = Image.fromarray(mask);
        findline_thresh_img.save('./test_find_line_img.png');


    def test_show_coordinates(self, filename):
        self._generate_layout(filename, {});
        sorted_hor_text=  sorted(self.horizontal_text, key = lambda x: -x.y0);
        for i in sorted_hor_text:
            print(i.get_text()[:-1], '  ', i.y0, '  ', i.y1);

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

            


        



