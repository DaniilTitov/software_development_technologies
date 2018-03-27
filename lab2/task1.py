import pandas as pd
import json


def get_data_from_json(path="data.json"):
    """
    :param path: string type path to json file 
    :return: pandas DataFrame object
    """
    data = pd.read_json(path)
    df = pd.DataFrame(data=data["table"]["rows"], columns=data["table"]["columnNames"])
    return df


def get_parameter_values(parameter, data):

    clear_data = data.drop(data[data[parameter + "_qc"] != 0].index)
    result = {"start_date": clear_data["time"].min(),
              "end_date": clear_data["time"].max(),
              "num_records": len(clear_data),
              "min_" + parameter: clear_data[parameter].min(),
              "min_time": clear_data["time"].min(),
              "max_" + parameter: clear_data[parameter].min(),
              "max_time": clear_data["time"].max(),
              "avg_" + parameter: clear_data[parameter].mean()}

    return result


def process_data(parameters, data):
    result = {parameter: get_parameter_values(parameter, data) for parameter in parameters}
    return json.dumps(result, indent=4)


if __name__ == '__main__':
    parameters = ["current_speed", "temperature", "salinity"]
    data = get_data_from_json("data.json")
    processed_data = process_data(parameters, data)
    print(processed_data)
