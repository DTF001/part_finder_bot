import pandas as pd

# DATASET_VDTM
pn_master_vdtm = pd.read_csv('pn_master_vdtm.csv', encoding='cp1252')
pns_vdtm = list(pn_master_vdtm['pn'])
pns_vdtm_int = list(pn_master_vdtm['pn_interchangeable'])
pn_vdtm_category = list(pn_master_vdtm['category'])

# CATALOG_INVENTORY_VDTM
inv_qry_vdtm = pd.read_csv('inv_qry_vdtm.csv', encoding='cp1252')
columns_vdtm = ['location', 'pn', 'pn_description', 'qty_available', 'stock_uom']
wh_list_vdtm = ['SVO', 'VKO', 'DME', 'SVO_SALES', 'KJA', 'SVO_TRS']
