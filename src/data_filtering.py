import pandas as pd
import geopandas as gpd

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

def create_geo_df(data_path: str):
    return gpd.read_file('data/us_states.json')

def create_tornado_count(data: pd.DataFrame, year=int):
    tornado_count = data[data['yr']==year].groupby('st', as_index=False).size()
    tornado_count.rename(columns={"size":"count"}, inplace=True)
    return tornado_count

def create_merged_data(tornado_count_df: pd.DataFrame, geo_df: gpd.GeoDataFrame):
    geo_count_df: gpd.GeoDataFrame = geo_df.merge(tornado_count_df, left_on='id', right_on='st', how='outer')
    geo_count_df.drop(['st'], axis=1, inplace=True)
    geo_count_df = geo_count_df.fillna(value={"count": 0})
    return geo_count_df