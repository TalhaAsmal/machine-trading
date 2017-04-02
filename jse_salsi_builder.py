import pandas as pd
from os import path

jse_salsi = ['BIL',
            'SNH',
            'SOL',
            'VOD',
            'AGL',
            'MNP',
            'MEI',
            'REM',
            'AMS',
            'ANG',
            'GRT',
            'GFI',
            'MRP',
            'NTC',
            'SGL',
            'PFG',
            'IMP',
            'AVI',
            'TKG',
            'KIO',
            'IPL',
            'CLS',
            'EXX',
            'ASR',
            'NHM',
            'HAR',
            'ARI',
            'EOH',
            'COH',
            'KAP',
            'BAW',
            'TON',
            'NPK',
            'SPG',
            'ITE',
            'RCL',
            'LON',
            'SAC',
            'ILV',
            'BLU',
            'AFE',
            'ZED',
            'IPF',
            'OMN',
            'DTC',
            'GND',
            'AWA',
            'NT1',
            'RBP',
            'EMI',
            'ADH',
            'WBO',
            'MSP',
            'AIP',
            'MPT',
            'ASC',
            'PAN',
            'CAT',
            'AFX',
            'MUR',
            'ARL',
            'RFG',
            'IAP',
            'MTA',
            'CIL',
            'NVS',
            'BWN',
            'HDC',
            'CLR',
            'RBX',
            'CGR',
            'TEX',
            'AFT',
            'ACT',
            'PGL',
            'HSP',
            'GRF',
            'ADR']

add_sep_2016 = ['ACL', 'APN', 'NEP', 'S32']
rem_sep_2016 = ['ADR', 'AWA', 'GRF']

add_dec_2016 = ['GLN', 'GRF', 'LHC', 'SAP']
rem_dec_2016 = ['NHM', 'RFG', 'WBO']

add_mar_2017 = ['AWA', 'CSB', 'EQU', 'PPC']
rem_mar_2017 = ['APN', 'EMI', 'LHC', 'REM', 'SAC', 'TEX']

mod_lists = ['sep_2016', 'dec_2016', 'mar_2017']

for mod_list in mod_lists:
    add_list = eval('add_' + mod_list)
    rem_list = eval('rem_' + mod_list)
    jse_salsi = jse_salsi + add_list
    jse_salsi = [a for a in jse_salsi if a not in rem_list]

out_data = pd.DataFrame(data=['JSE:' + a for a in jse_salsi], columns=['stocks'])
out_data.to_csv(path.join('stock_lists', 'jse_salsi.csv'), index=False)

