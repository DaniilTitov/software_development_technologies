import pandas as pd


def get_data_from_json(path="data.json"):
    """
    :param path: string type path to json file 
    :return: pandas DataFrame object
    """
    df = pd.read_json(path)
    df1 = pd.DataFrame(data=df["table"]["rows"], columns=df["table"]["columnNames"])

    df1["time_created"] = pd.to_datetime(df1["time_created"])
    df1["time"] = pd.to_datetime(df1["time"])
    df1["time_modified"] = pd.to_datetime(df1["time_modified"])

    return df1


def remove_not_zero_rows(df, columns=None, trace=True):
    """
    This method removes all rows that contains value more 0 for 'columns' parameters
    :param df: pandas DataFrame
    :param columns: Array of strings 
    :param trace: If True there is message about removed rows, else no message. 
    :return: Processed DataFrame
    """

    if columns is None:
        columns = [
            "current_speed_qc",
            "current_direction_qc",
            "current_u_qc",
            "current_v_qc",
            "temperature_qc",
            "conductivity_qc",
            "salinity_qc",
            "sigma_t_qc"
        ]

    source_size = len(df)
    for column in columns:
        df.drop(df[df[column] > 0].index, inplace=True)

    if trace:
        print("Removed", source_size - len(df), "rows")

    return df


def get_min_max_parameters(df, parameters=None):
    """
    Method return list of dict of min, max, min_index, max_index for all 'parameters'
    :param df: Pandas DataFrame
    :param parameters: Array of strings
    :return: Value like [parameter1: {ind_min: ..., ind_max: ...}, parameter2: {ind_min: ..., ind_max: ...}, ...]
    """

    if parameters is None:
        parameters = [
            "temperature",
            "salinity",
            "conductivity"
        ]

    result = list()

    for parameter in parameters:

        ind_max = df[parameter].idxmax()
        # max_val = df[parameter][ind_max]

        ind_min = df[parameter].idxmin()
        # min_val = df[parameter][ind_min]

        result.append({parameter: {
            "ind_min": ind_min,
            "ind_max": ind_max,
            # "min": min_val,
            # "max": max_val
        }})

    return result

if __name__ == '__main__':
    df = get_data_from_json("data.json")
    df = remove_not_zero_rows(df)
    labels = ["current_speed", "current_direction"]
    parameters = get_min_max_parameters(df, labels)

    for i in parameters:
        row_indexes = list(list(i.values())[0].values())
        print("For parameter", list(i.keys())[0], ":")
        print(df.iloc[row_indexes, :], end="\n" + "=" * 60 + "\n\n\n")
