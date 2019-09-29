from camelot import io;
from camelot.parsers.new_parser import NewParser;

def run_stream_parse():
    sample_pdf_file = './page-316.pdf';
    tables = io.read_pdf(sample_pdf_file, flavor='stream')
    print(tables);

def run_self_defined_parse():
    sample_pdf_file = './page-316.pdf';
    np = NewParser();
    np.extract_table(sample_pdf_file);


if __name__ == '__main__':
    #run_stream_parse();
    run_self_defined_parse();
