'''
These functions are for the quantification of white matter lesions.
'''

import matplotlib as mpl
import pandas as pd
import zipfile


def binary_cmap(c):
    return mpl.colors.ListedColormap([(0, 0, 0, 0), c])


def select_matching_patients(testgroup, controlgroup, nmatches=5, traits=[2, 3]):
    '''
    Select patients from control group matching patients in test group in selected traits.
    
    arguments:
        testgroup:     dataframe of test group (e. g. Fabry cohort)
        controlgroup:  dataframe of control group
        nmatches:      number of patients to be matched per patient in test group
        traits:        column indices in testgroup to be matched
    
    returns:
        ids:           list of patient ids selected from control group
    '''
    
    print('Patients:\t', testgroup.shape[0], '\nMatches each:\t', nmatches, '\nTraits:\t \t', [testgroup.columns[t] for t in traits])
    
    ids = []  # gets filled with selected patient ids
    
    for _, patient in testgroup.iterrows():

        traitnames = [testgroup.columns[t] for t in traits]
        matchtraits = dict([[t, patient[t]] for t in traitnames])

        comparison = (controlgroup[traitnames] == pd.Series(matchtraits)).all(axis=1)
        matches = controlgroup.loc[comparison, 'Participant ID'].tolist()
        
        selected_ids = []
        i = 0 
        replacements = 0
        while len(selected_ids) < nmatches and i < len(matches):
            mid = matches[i]
            file = '/mnt/project/Bulk/Brain MRI/T2 FLAIR/'+str(mid)[:2]+'/'+str(mid)+'_20253_2_0.zip'
            try:
                with zipfile.ZipFile(file, 'r') as zf:
                    zf.read('T2_FLAIR/T2_FLAIR.nii.gz')
                    selected_ids.append(mid)
            except:
                replacements += 1
            i += 1
            
        controlgroup = controlgroup.loc[~controlgroup.loc[:, 'Participant ID'].isin(selected_ids)]  # remove selected matches to prevent duplicates in control group
        if len(selected_ids) != nmatches:
            print('!! Only ', len(selected_ids), ' found for patient ', patient['Participant ID'], '.', sep='')
        ids.extend(selected_ids)
    
    return ids