import json
import os
import urllib.request
from dotenv import load_dotenv
from pathlib import Path
from UtilLib.JSONHandler import JSONHandler

bus_svc_data: JSONHandler


def request_bus_svc_info(svc: str, direction: int, api_key: str):
    """
    Gets and returns information of the bus service. Does not cover bus route.

    :param svc: The Service Number
    :param direction: The service direction, either 1 or 2. For loops, use 1.
    :param api_key: The LTA API Key
    :return: Tuple containing:
             [0] -> Service Number,
             [1] -> Service Operator,
             [2] -> Direction,
             [3] -> Service Category,
             [4] -> Origin of Travel (in code),
             [5] -> Destination (in code),
             [6] -> Loop Description,
             [7] -> boolean stating whether this service is a loop
    """
    skip_val = 0
    while True:
        url = f"http://datamall2.mytransport.sg/ltaodataservice/BusServices?$skip={skip_val}"

        headers = {
            "AccountKey": api_key,
            "accept": "application/json"
        }

        request = urllib.request.Request(url=url, headers=headers, method="GET")

        with urllib.request.urlopen(request) as response:
            json_dict = response.read().decode("utf-8")
            dict_data = json.loads(json_dict)

            for data in dict_data["value"]:
                is_loop = False
                if data["ServiceNo"] == svc and data["Direction"] == direction:

                    if data["Direction"] == 1 and data["LoopDesc"] != "":
                        is_loop = True

                    return (
                        data["ServiceNo"],
                        data["Operator"],
                        data["Direction"],
                        data["Category"],
                        data["OriginCode"],
                        data["DestinationCode"],
                        data["LoopDesc"],
                        is_loop
                    )

            if len(dict_data["value"]) < 500:
                return (
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None
                )
            else:
                skip_val += 500


def store_bus_svc_data(api_key: str):
    global bus_svc_data
    bus_svc_data = JSONHandler("BusServiceData")

    curr_data = {"value": []}
    skip_val = 0
    while True:
        url = f"http://datamall2.mytransport.sg/ltaodataservice/BusServices?$skip={skip_val}"

        headers = {
            "AccountKey": api_key,
            "accept": "application/json"
        }

        request = urllib.request.Request(url=url, method="GET", headers=headers)

        with urllib.request.urlopen(request) as response:
            json_dict = response.read().decode("utf-8")
            dict_data = json.loads(json_dict)

            curr_data["value"].extend(dict_data["value"])

            if len(dict_data["value"]) < 500:
                break

            else:
                skip_val += 500

    bus_svc_data.update_json(curr_data)
    bus_svc_data.update_json_file()
    bus_svc_data.formulate_json()


def return_bus_svc_json(svc: str, direction: int):
    for data in bus_svc_data.return_specific_json("value"):
        is_loop = False
        if data["ServiceNo"] == svc and data["Direction"] == direction:

            if data["Direction"] == 1 and data["LoopDesc"] != "":
                is_loop = True

            return (
                data["ServiceNo"],
                data["Operator"],
                data["Direction"],
                data["Category"],
                data["OriginCode"],
                data["DestinationCode"],
                data["LoopDesc"],
                is_loop
            )


if __name__ == "__main__":
    ENV_PATH = os.path.join(Path(__file__).resolve().parent.parent, "RefKey.env")

    # Load ENV
    load_dotenv(dotenv_path=ENV_PATH)

    # Get Values from ENV
    API_KEY_LTA = os.getenv("API_KEY_LTA")

    returner = request_bus_svc_info("16M", 1, API_KEY_LTA)
    if returner[7] is False:
        print(
            f"=======================================================================================\n"
            f"[{returner[0]}] | {returner[1]}\n"
            f"{returner[3]} Service\n"
            f"{returner[4]} >>> {returner[5]} [Direction: {returner[2]}]\n"
            f"======================================================================================="
        )
    elif returner[7] is True:
        print(
            f"=======================================================================================\n"
            f"[{returner[0]}] | {returner[1]}\n"
            f"{returner[3]} Service\n"
            f"Loop @ {returner[6]} to {returner[5]}\n"
            f"======================================================================================="
        )
    else:
        print(
            f"=======================================================================================\n"
            f"This service does not exist.\n"
            f"======================================================================================="
        )
