from camelot import io;

sample_pdf_file = './5079927-页面-316-318.pdf';
tables = io.read_pdf(sample_pdf_file, flavor='stream')
print(tables);
