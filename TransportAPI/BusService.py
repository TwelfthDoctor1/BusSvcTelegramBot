import json
import os
import urllib.request
from dotenv import load_dotenv
from pathlib import Path
from UtilLib.JSONHandler import JSONHandler

bus_svc_data: JSONHandler

dbl_loop_data = {
    "42": "Lengkong Empat & Fidelio St",
    "92": "Science Pk Dr & Mount Sinai Dr",
    "291": "Tampines St 81 & Tampines St 33",
    "293": "Tampines St 71 & Tampines Ave 7",
    "307": "Choa Chu Kang St 62 & Teck Whye Lane",
    "358": "Pasir Ris Dr 10 & Pasir Ris Dr 4",
    "359": "Pasir Ris St 71 & Pasir Ris Dr 2",
    "811": "Yishun Ave 5 & Yishun Ave 1",
    "812": "Yishun Ave 4 & Yishun Ave 3",
    "911": "Woodlands Ave 2 & Woodlands Ctr Rd",
    "912": "Woodlands Ave 7 & Woodlands Ctr Rd",
    "913": "Woodlands Circle & Woodlands Ave 3"
}


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
        url = f"https://datamall2.mytransport.sg/ltaodataservice/BusServices?$skip={skip_val}"

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
        url = f"https://datamall2.mytransport.sg/ltaodataservice/BusServices?$skip={skip_val}"

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

            for (k, v) in dbl_loop_data.items():
                if k == data["ServiceNo"]:
                    data["LoopDesc"] = v

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


def get_bus_svc_list():
    bus_svc_list = []
    for data in bus_svc_data.return_specific_json("value"):
        if data["ServiceNo"] not in bus_svc_list:
            bus_svc_list.append(data["ServiceNo"])

    return sort_bus_svc_list(bus_svc_list)


def sort_bus_svc_list(svc_list: list):
    reg_num_svc = []
    sp_svc_list = []
    sep_sp_svc_list = {}
    final_svc_list = []

    for svc in svc_list:
        if svc.isdigit():
            reg_num_svc.append(int(svc))
            # print(f"APPEND {svc} to REG LIST")
        else:
            sp_svc_list.append(svc)
            # print(f"APPEND {svc} to SP LIST")

    reg_num_svc = sorted(reg_num_svc)

    for sp_svc in sp_svc_list:
        num = ""
        svc_uid = ""
        for i in sp_svc:
            if i.isdigit():
                num += i
            else:
                svc_uid += i

        sep_sp_svc_list[int(num)] = svc_uid

        # print(f"K: {num} V: {svc_uid}")

    for svc in reg_num_svc:
        if svc not in sep_sp_svc_list:
            final_svc_list.append(str(svc))
            # print(f"APPEND {svc} to LIST")
        else:
            final_svc_list.append(str(svc))
            # print(f"APPEND {svc} to LIST")

            final_svc_list.append(str(svc) + str(sep_sp_svc_list[svc]))
            # print(f"APPEND {str(svc) + str(sep_sp_svc_list[svc])} to LIST")

    return final_svc_list


def get_bus_svc_directions(svc: str):
    bus_svc_list = []
    for data in bus_svc_data.return_specific_json("value"):
        # print(f"{data["ServiceNo"]} || {svc}")
        is_loop = False
        if data["ServiceNo"] == svc:

            if data["Direction"] == 1 and data["LoopDesc"] != "":
                is_loop = True

            for (k, v) in dbl_loop_data.items():
                if k == data["ServiceNo"]:
                    data["LoopDesc"] = v

            bus_svc_list.append((
                data["ServiceNo"],
                data["Direction"],
                data["Category"],
                data["OriginCode"],
                data["DestinationCode"],
                data["LoopDesc"],
                is_loop
            ))

            # print(f"LEN: {len(bus_svc_list)}")

            if is_loop or len(bus_svc_list) == 2:
                # print(F"EXIT FUNC: \n {bus_svc_list}")
                return bus_svc_list

    return bus_svc_list


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
