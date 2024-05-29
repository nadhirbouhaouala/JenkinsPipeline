import pandas as pd

def create_dataframe_adherent(list1 ,list2 ,list3 ,list4 ,list5 ,list6 ,list7 ,list8, list9, list10,
                                list11, list12, list13, list14, list15, list16, list17, columns_name):
    res = []
    for t in zip(list1 ,list2 ,list3 ,list4 ,list5 ,list6 ,list7 ,list8, list9, list10, list11, list12, 
                 list13, list14, list15, list16, list17):
        res.append(t)
    return pd.DataFrame(res,columns=columns_name)

def create_dataframe_entreprise(list1 ,list2 ,list3 ,list4 ,list5 ,list6 ,list7 ,list8, list9, list10,
                                list11, list12, list13, list14, list15, list16, list17, list18, columns_name):
    res = []
    for t in zip(list1 ,list2 ,list3 ,list4 ,list5 ,list6 ,list7 ,list8, list9, list10, list11, list12, 
                 list13, list14, list15, list16, list17, list18):
        res.append(t)
    return pd.DataFrame(res,columns=columns_name)

def create_dataframe_affiliations(list1 ,list2 ,list3 ,list4 ,list5 ,list6 ,list7 ,list8, list9, list10,
                                  list11, list12, list13, list14, list15, list16, list17, list18, list19,
                                  list20, list21, list22, list23, list24, list25, list26, list27, list28,
                                  list29, list30, list31, list32, list33, list34, list35, list36, list37, list38,
                                  columns_name):
    res = []
    for t in zip(list1 ,list2 ,list3 ,list4 ,list5 ,list6 ,list7 ,list8, list9, list10,
                 list11, list12, list13, list14, list15, list16, list17, list18, list19,
                 list20, list21, list22, list23, list24, list25, list26, list27, list28,
                 list29, list30, list31, list32, list33, list34, list35, list36, list37, list38):
        res.append(t)
    return pd.DataFrame(res,columns=columns_name)