# convert XLSX to TSV

import os
import pandas as pd

local_path = os.getcwd() + "\\periodo-projects\\"
xlsx_file = local_path + 'rdm-bu-period.xlsx'
xls = pd.ExcelFile(xlsx_file)
sheet_index = 2
output_tsv_file = local_path + 'rdm-bu-period-levels.tsv'
df = xls.parse(sheet_index)
df.to_csv(output_tsv_file, sep='\t', index=False)