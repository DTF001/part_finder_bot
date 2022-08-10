import pandas as pd

# FIND_MACHINE
from fuzzywuzzy import process


# PART_FINDER
def finder(master, slave, your_pn):
    print_list = []
    for index in range(len(slave)):
        if your_pn == slave[index]:
            found_pn = master[index]
            for value in range(len(master)):
                if found_pn == master[value]:
                    print_list.append(slave[value])
    return print_list


# EXTRA_PART_FINDER
def extra_finder(slave, master, your_pn):
    print_list_adv = []
    for index in range(len(slave)):
        if your_pn in slave[index]:
            found_pn = master[index]
            for value in range(len(master)):
                if found_pn == master[value]:
                    print_list_adv.append(slave[value])
    print(print_list_adv)
    return print_list_adv


# INVENTORY_EXPLORER
def trax_inventory_explorer(inv_qry, columns, found, warehouses):
    df = pd.DataFrame(data=inv_qry, columns=columns)
    df2 = []
    for item in found:
        for item1 in warehouses:
            df1 = df[(df['pn'] == item) & (df['location'] == item1) & (df['qty_available'] != 0)]
            if not df1.empty:
                df1 = df1.reset_index(drop=True)
                pn = df1.loc[0]['pn']
                qty = df1['qty_available'].sum()
                loc_wh = df1.loc[0]['location']
                desc = df1.loc[0]['pn_description']
                uom = df1.loc[0]['stock_uom']
                list1 = [loc_wh, pn, desc, qty, uom]
                df2.append(list1)
    df2 = pd.DataFrame(data=df2, columns=columns)
    return df2