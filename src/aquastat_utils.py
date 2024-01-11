from src.utils import get_dataframe

FILE_NAME = '../dat/fao_aquastat.csv'
CSV_URL = 'https://yaon.org/data.csv'

aquastat_df = None


def get_aquastat():
    global aquastat_df

    if aquastat_df is not None:
        print('Returning cached dataframe')
        return aquastat_df.copy()

    # Download the data from https://yaon.org/data.csv
    import_df = get_dataframe(file_path=FILE_NAME, url=CSV_URL)
    if import_df is None:
        print('Could not get the AQUASTAT Dataframe!')
        return None

    # Format dataframe
    import_df.drop(columns=['Unnamed: 0'], inplace=True)
    df = import_df.pivot_table(index=['Country', 'Year'], columns='Variable', values='Value', aggfunc='first')
    df.reset_index(inplace=True)

    aquastat_df = df

    return df
