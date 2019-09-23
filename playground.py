from camelot import io;

sample_pdf_file = '/home/peng/Workspace/data/finance_helper/annual_reports/5079927-页面-316-318.pdf';
tables = io.read_pdf(sample_pdf_file, flavor='stream')
print(tables);
