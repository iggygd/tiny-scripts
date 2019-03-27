import pandas as pd

def load():
    '''
    Pokemon data from https://www.kaggle.com/n2cholas/competitive-pokemon-dataset
    '''
    dfm = pd.read_csv('data/move-data.csv')
    dfp = pd.read_csv('data/pokemon-data.csv', delimiter=';')

    return dfp, dfm