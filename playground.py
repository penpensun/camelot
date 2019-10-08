from camelot import io;
from camelot.parsers.new_parser import NewParser;

sample_pdf_file = './page-316.pdf';
sample_image_file = './page-316.jpg';

def run_stream_parse():
    
    tables = io.read_pdf(sample_pdf_file, flavor='stream')
    print(tables);

def run_self_defined_parse():
    np = NewParser();
    np.extract_table(sample_pdf_file);

def test_show_coordinate():
    np = NewParser();
    np.test_show_coordinates(sample_pdf_file);

def test_find_line():
    np = NewParser();
    np.test_find_lines(sample_pdf_file, sample_image_file);

if __name__ == '__main__':
    #run_stream_parse();
    run_self_defined_parse();
    #test_show_coordinate();
    #test_find_line();
