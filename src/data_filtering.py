import pandas as pd

def create_df(data_path: str):
    df = pd.read_csv(data_path)
    df.reset_index(drop=True, inplace=True)


    df['date'] = pd.to_datetime(df['date'])
    df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S')
    df['st'] = df['st'].astype('str')

    # combine lat/long columns together for easier usage
    df['sgeo'] = [[df['slat'][i],df['slon'][i]] for i in range(len(df)) ]
    df['egeo'] = [[df['elat'][i],df['elon'][i]] for i in range(len(df)) ]
    df.drop(['slat', 'slon', 'elat', 'elon'], axis=1, inplace=True)
    return df