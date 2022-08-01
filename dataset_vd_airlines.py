import pandas as pd

# DATASET_AIRLINES
pn_master_airlines = pd.read_csv('pn_master_abc.csv', encoding='cp1252')
pns_airlines = list(pn_master_airlines['pn'])
pns_airlines_int = list(pn_master_airlines['pn_interchangeable'])
pn_airlines_category = list(pn_master_airlines['category'])

# CATALOG_INVENTORY_AIRLINES
inv_qry_airlines = pd.read_csv('inv_qry_airlines.csv', encoding='cp1252', low_memory=False)
columns_airlines = ['location', 'pn', 'pn_description', 'qty_available', 'stock_uom']
wh_list_airlines = ['FRA', 'VKO-ATR-SV', 'SHJ', 'SVO', 'FRA-ATR', 'SVO-ATRAN', 'LGG ATR', 'LEJ', 'SHJ_ATRAN', 'LGG_ABC',
                    'UTG-ATR-SV', 'KJA-ATR-SV', 'RIX-ATR-SV', 'DME-ATR-SV', 'LEJ_ATRAN', 'ORD', 'KJA', 'PVG']
