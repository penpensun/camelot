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

        # converted_img.show();
        # Find lines
        mask, segments = find_lines(threshold, regions = None, direction='horizontal', \
            line_scale =lattice_parser.line_scale);
        
        # the height and width of the image
        print('the height of the image: ', image.shape[0]);
        print('the width of the image: ', image.shape[1]);

        print('type of mask: ', type(mask));
        line_coord = np.argwhere(mask >0);
        print('coord of line: ');
        print(line_coord);
        print('shape of coordinate of line: ', line_coord.shape);
        print('unique y: ');
        print(np.unique(line_coord[:, 0]));
        unique_y_coords = np.unique(line_coord[:, 0]);

        line_image = Image.fromarray(mask);
        line_image.save('./line_img.png');
        # test case of line coordinate [0]
        max_img_y = image.shape[0];
        max_img_x = image.shape[1];
        max_pdf_y = 842;
        max_pdf_x = 595;

        converted_y_coords = []
        print('line coordinate y_0 :', line_coord[0,0]);
        print('converted line coordinate converted y coords: ', 
            self.convert_img_y_to_pdf(line_coord[0,0], max_img_y = max_img_y, max_pdf_y = max_pdf_y));
        for y_coord in unique_y_coords:
            converted_y_coords.append( self.convert_img_y_to_pdf(y_coord, \
                max_img_y = max_img_y, \
                max_pdf_y = max_pdf_y));
            print('converted y coord: ', 
                self.convert_img_y_to_pdf(y_coord, \
                max_img_y = max_img_y, \
                max_pdf_y = max_pdf_y));

    # convert the image coordinates to pdf coordinates
    def convert_img_coords_to_pdf(self, img_x, img_y, max_img_x, max_img_y, max_pdf_x, max_pdf_y):
        pdf_x = self.convert_img_x_to_pdf(img_x, max_img_x, max_pdf_x);
        pdf_y = self.convert_img_y_to_pdf(img_y, max_img_y, max_pdf_y);
        return (pdf_x, pdf_y);
    # convert 
    def convert_img_x_to_pdf(self, img_x, max_img_x, max_pdf_x):
        return round(img_x/max_img_x * max_pdf_x, 2)
    
    def convert_img_y_to_pdf(self, img_y, max_img_y, max_pdf_y):
        return round((max_img_y - img_y) / max_img_y * max_pdf_y, 2);

    def test_show_coordinates(self, filename):
        self._generate_layout(filename, {});
        sorted_hor_text=  sorted(self.horizontal_text, key = lambda x: -x.y0);
        for i in sorted_hor_text:
            print(i.get_text()[:-1], '  ', i.y0, '  ', i.y1);

    def align_lines (self):
        lines = [];
        merge_count = [];
        table_areas = [];
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

        # find the table area
        idx = 0;
        while idx < len(lines):
            if idx >= len(lines):
                break;
            current_table = [];
            # start of the table
            if (len(lines[idx]) > 1):
                current_table.append(lines[idx]); # append the line to the table
                idx +=1;
                if idx >= len(lines): # if the index already reaches the length, then break
                    break;
                while len(lines[idx]) > 1:
                    current_table.append(lines[idx]);
                    idx+=1;
                    if idx >= len(lines):
                        break;
            table_areas.append(current_table);
            idx += 1;

        # Remove the table less than 3 rows
        refined_table_areas = [];
        print('number of tables: ', len(table_areas));
        for table in table_areas:
            print('number of rows in table: ', len(table));
            if len(table) >=3:
                refined_table_areas.append(table);
        table_areas = refined_table_areas;
        print('number of tables: ', len(table_areas));

        # output table
        with open('test_table_output', 'w') as test_table_writer:
            test_table_writer.write('Totally '+str(len(table_areas))+' tables.\n');
            for table_idx in range(0,len(table_areas)):
                test_table_writer.write('table: ' + str(table_idx+1)+ '\n');
                for line in table_areas[table_idx]:
                    test_table_writer.write('row start:\n');
                    for text_field in line:
                        test_table_writer.write(
                            str(text_field.x0)+' '+ \
                            str(text_field.x1)+' '+ \
                            str(text_field.y0)+' '+ \
                            str(text_field.y1)+ ' '+\
                            text_field.get_text());
        
                    
        



    


        



