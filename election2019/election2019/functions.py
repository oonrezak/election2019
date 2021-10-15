def fetch_files():
    """
    Fetches the data from each region.
    """
    
    # The files we want to access:
    search_terms = ['_NCR_Statistical Tables_0.xls',
     '_CARAGA_Statistical Tables.xls',
     '_CAR_Statistical Tables.xls',
     '_REGION IV-A_Statistical Tables.xls',
     '_REGION VII_Statistical Tables.xls',
     '_REGION X_Statistical Tables.xls',
     '_REGION IX_Statistical Tables.xls',
     '_ARMM_Statistical Tables.xls',
     '_MIMAROPA_Statistical Tables.xls',
     '_REGION VIII_Statistical Tables.xls',
     '_REGION I_Statistical Tables.xls',
     '_REGION V_Statistical Tables.xls',
     '_REGION II_Statistical Tables.xls',
     '_NIR_Statistical Tables.xls',
     '_REGION III_Statistical Tables.xls',
     '_REGION XI_Statistical Tables.xls',
     '_REGION VI_Statistical Tables.xls',
     '_REGION XII_Statistical Tables.xls',
     'Negros Occidental_Statistical Tables.xls',
     'Negros Oriental_Statistical Tables.xls']
    
    reg_voters_dict = {'_NCR_Statistical Tables_0.xls': 7074603,
                        '_CARAGA_Statistical Tables.xls': 1760582,
                        '_CAR_Statistical Tables.xls': 1013418,
                        '_REGION IV-A_Statistical Tables.xls': 8674351,
                        '_REGION VII_Statistical Tables.xls': 4946353,
                        '_REGION X_Statistical Tables.xls': 2855792,
                        '_REGION IX_Statistical Tables.xls': 2193033,
                        '_ARMM_Statistical Tables.xls': 2172959,
                        '_MIMAROPA_Statistical Tables.xls': 1831328,
                        '_REGION VIII_Statistical Tables.xls': 3051649,
                        '_REGION I_Statistical Tables.xls': 3331404,
                        '_REGION V_Statistical Tables.xls': 3647723,
                        '_REGION II_Statistical Tables.xls': 2194418,
                        '_NIR_Statistical Tables.xls': np.nan,
                        '_REGION III_Statistical Tables.xls': 6829661,
                        '_REGION XI_Statistical Tables.xls': 3026393,
                        '_REGION VI_Statistical Tables.xls': 4808839,
                        '_REGION XII_Statistical Tables.xls': 2431265}
        
    for root, dirs, files in os.walk(census_dir):
        # Create the df that will store the data:
        df_census = pd.DataFrame(index=search_terms)
        
        # Iterate through files and select the ones in search_terms
        for file in files:
            if file in search_terms:
                path = census_dir / str(file)
                
                # Read the sheets we want into the df_dict:
                    # T2 for total population and ages
                    # T8 for religion (INC)
                    # T10 for literacy 20 y/o and above
                df_dict = pd.read_excel(path, sheet_name=['T2', 'T8', 'T10'])
                
                # 1. Get the total population:
                df_dict['T2']
                total_pop = df_dict['T2'].iloc[5, 1]
                # Assign to column total_pop in df_census:
                df_census.loc[file, 'total_pop'] = total_pop
                
                # 2. Get the total population 18 and above:
                eighteen_over = df_dict['T2'].loc[24:86, 'Unnamed: 1'].sum()
                # Assign to column  eighteen_over in df_census:
                df_census.loc[file, 'eighteen_over'] = eighteen_over
#                 # Let's assign the registered voters to the df:
#                 df_census.loc[file, 'reg_voters'] = reg_voters_dict[file]
                
                # 3. Get the INC
                df_dict['T8'].index = df_dict['T8'].iloc[:,0]
                df_dict['T8'].drop(columns='TABLE 8  Total Population by R' +\
                    'eligious Affiliation and Sex: 2015', inplace=True)
                inc = df_dict['T8'].loc['Iglesia ni Cristo', 'Unnamed: 1']
                # Assign to column inc_members in df_census:
                df_census.loc[file, 'inc_members'] = inc
                # Calculate proportion of inc_members:
                df_census['inc_proportion'] = df_census.apply(lambda row: \
                    row['inc_members'] / row['total_pop'], axis=1)
                
                # 4. Get the literacy rate of 20 y/o and above:
                to_drop = ['Unnamed: ' + str(i) for i in [2, 3, 5, 6]]
                df_dict['T10'].drop(columns=to_drop, inplace=True)
                df_dict['T10'].columns = ['age_group', 'total', 'literate']
                literacyn = df_dict['T10'].loc[8:17]['literate'].sum()
                literacy = df_dict['T10'].loc[8:17]['literate'].sum() /\
                    df_dict['T10'].loc[8:17]['total'].sum()
                # Assign to column literacy in df_census:
                df_census.loc[file, 'literacy'] = literacyn
                df_census.loc[file, 'literacy_proportion'] = literacy
    
    df_census.loc['_REGION VI_Statistical Tables.xls']['total_pop'] += \
        df_census.loc['Negros Occidental_Statistical Tables.xls']['total_pop']
    df_census.loc['_REGION VI_Statistical Tables.xls']['eighteen_over'] += \
        df_census.loc['Negros Occidental_Statistical Tables.xls']['eighteen_over']
    df_census.loc['_REGION VI_Statistical Tables.xls']['inc_members'] += \
        df_census.loc['Negros Occidental_Statistical Tables.xls']['inc_members']
    df_census.loc['_REGION VI_Statistical Tables.xls']['literacy'] += \
        df_census.loc['Negros Occidental_Statistical Tables.xls']['literacy']
    df_census.loc['_REGION VI_Statistical Tables.xls']['inc_proportion'] = \
        (df_census.loc['_REGION VI_Statistical Tables.xls']['inc_proportion']\
        + df_census.loc\
        ['Negros Occidental_Statistical Tables.xls']['inc_proportion']) / 2
    df_census.loc['_REGION VI_Statistical Tables.xls']['literacy_proportion']\
        = (df_census.loc\
        ['_REGION VI_Statistical Tables.xls']['literacy_proportion'] \
        + df_census.loc\
        ['Negros Occidental_Statistical Tables.xls']['literacy_proportion']) / 2

    df_census.loc['_REGION VII_Statistical Tables.xls']['total_pop'] += \
        df_census.loc['Negros Oriental_Statistical Tables.xls']['total_pop']
    df_census.loc['_REGION VII_Statistical Tables.xls']['eighteen_over'] += \
        df_census.loc['Negros Oriental_Statistical Tables.xls']['eighteen_over']
    df_census.loc['_REGION VII_Statistical Tables.xls']['inc_members'] += \
        df_census.loc['Negros Oriental_Statistical Tables.xls']['inc_members']
    df_census.loc['_REGION VII_Statistical Tables.xls']['literacy'] += \
        df_census.loc['Negros Oriental_Statistical Tables.xls']['literacy']
    df_census.loc['_REGION VII_Statistical Tables.xls']['inc_proportion'] = \
        (df_census.loc\
        ['_REGION VII_Statistical Tables.xls']['inc_proportion'] + \
        df_census.loc['Negros Oriental_Statistical Tables.xls']['inc_proportion']) / 2
    df_census.loc\
        ['_REGION VII_Statistical Tables.xls']['literacy_proportion'] = (df_census.loc['_REGION VII_Statistical Tables.xls']['literacy_proportion'] + df_census.loc['Negros Oriental_Statistical Tables.xls']['literacy_proportion']) / 2
    
    df_census.drop(['Negros Occidental_Statistical Tables.xls', 
                    'Negros Oriental_Statistical Tables.xls', 
                    '_NIR_Statistical Tables.xls'], inplace=True)
      
    return df_census
    
def sorter(list_1, list_2, reverse=False):
    """
    Sorts list_1 and list_2 based on list_2's values;
    Useful for processing data before plotting them.
    
    list_1 and list_2 must be of equal length.
    
    Parameters
    ----------
    list_1 : list
    list_2 : list
        list to sort by
        note that both will be sorted
    
    reverse : bool
        if True descending
        if False ascending
    
    Returns
    -------
    tuple
        (list_1_sorted, list_2_sorted) both sorted by list_2
    
    """
    lists = [(l1, l2) for l1, l2 in zip(list_1, list_2)]
    lists.sort(reverse=reverse, key=lambda x: x[1])
    list_1_sorted = [item[0] for item in lists]
    list_2_sorted = [item[1] for item in lists]
    
    return (list_1_sorted, list_2_sorted)