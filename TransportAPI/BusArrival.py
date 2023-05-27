import datetime
import json
import urllib.request
from UtilLib.StringLib import *


SEATING = [("SEA", "Seating Available"), ("SDA", "Standing Available"), ("LSD", "Limited Standing")]
BUS_TYPE = [("SD", "Single Deck"), ("DD", "Double Deck"), ("BD", "Bendy")]


def interpret_seating(seating: str):
    for seating_data in SEATING:
        if seating == seating_data[0]:
            return seating_data[1]
    return ""


def interpret_type(bus_type: str):
    for type_data in BUS_TYPE:
        if bus_type == type_data[0]:
            return type_data[1]
    return ""


def calculate_est_duration(dur_1: int, dur_2: int, dur_3: int):
    if dur_1 != 0 and dur_2 != 0 and dur_3 != 0 and dur_1 < 1000:
        est_duration = (dur_1 + dur_2 + dur_3) / 3
    elif dur_2 != 0 and dur_3 != 0:
        est_duration = (dur_2 + dur_3) / 2
    elif dur_1 != 0 and dur_2 != 0 and dur_1 < 1000:
        est_duration = (dur_1 + dur_2) / 2
    elif dur_2 != 0:
        est_duration = dur_2
    else:
        est_duration = dur_1

    return round(est_duration, 1)


def request_bus_stop_timing(bus_stop_code: int or str, api_key: str, svc_num: list,
                            fallback_header: bool = False, debug: bool = False):
    """
    Core Function to get and return the Timings of Services for a Bus Stop.
    For a specific number in Services, define the Service Number.
    :param bus_stop_code: The 5-digit Bus Stop code. Should be in string, integer not recommended for it may remove
                          leading zeros.
    :param api_key: The API Key to allow calling of API services.
    :param svc_num: A list of Bus Service Numbers to explicitly see. Optional, either string or integer is accepted in a
                    list.
    :param fallback_header: A boolean state that determines whether the fallback header should be used. (Shows the code)
    :param debug: A boolean state to show debug text
    :return: A Tuple of 18 values (exc. !):
             [0] -> Service Number,
             [1] -> Service Operator,
             [2] -> First Bus Timing in XX min @ XX:XX:XX,
             [3] -> Second Bus Timing in XX min @ XX:XX:XX,
             [4] -> Third Bus Timing in XX min @ XX:XX:XX,
             [5] -> First Bus Seating Availability,
             [6] -> Second Bus Seating Availability,
             [7] -> Third Bus Seating Availability,
             [8] -> First Bus Type,
             [9] -> Second Bus Type,
             [10] -> Third Bus Type,
             [11] -> First Bus Visit Status,
             [12] -> Second Bus Visit Status,
             [13] -> Third Bus Visit Status,
             [14] -> Estimated Duration for all 3 buses,
             [15] -> Estimated Duration for 1st Visit Buses,
             [16] -> Estimated Duration for 2nd Visit Buses,
             [17] -> Boolean State to state whether all buses are on 1st Visit only,
             [18] -> Origin Bus Stop,
             [19] -> Destination Bus Stop,
             [!] -> Note: For 14 to 17, bool state is to be used to determine on which type of duration(s) to be shown.
    """
    # URL Construct
    url = f"http://datamall2.mytransport.sg/ltaodataservice/BusArrivalv2?BusStopCode={bus_stop_code}"

    # Service Specific Addition - To use sep. method instead
    # if svc_num != "":
    #     URL += f"&ServiceNo={svc_num}"

    # Header Data
    headers = {
        "AccountKey": api_key,
        "accept": "application/json"
    }

    request = urllib.request.Request(url=url, method="GET", headers=headers)

    dt = datetime.datetime.now()
    bus_list = []
    sp_bus_list = []
    bus_stop_list = []
    sorted_sp_bus = []
    with urllib.request.urlopen(request) as response:
        json_data = response.read().decode("utf-8")
        dict_data = json.loads(json_data)
        inc = 0

        # Sort Numbers in Ascending Order
        for bus_svc in dict_data["Services"]:
            if bus_svc["ServiceNo"].isdigit() is True:
                # Pure Number
                # print(f"Bus {bus_svc['ServiceNo']} is a pure number.")
                bus_list.append((int(bus_svc["ServiceNo"]), inc))
            else:
                # Numbers with Letters
                # print(f"Bus {bus_svc['ServiceNo']} has characters.")
                sp_bus_list.append((bus_svc["ServiceNo"], inc))
            inc += 1

        bus_list = sorted(bus_list)
        # print(bus_list)
        # print(sp_bus_list)

        # Sort Numbers with Letters
        for sp_bus in sp_bus_list:
            has_sorted = False

            # Sort based on matchable numbers
            for i in range(len(bus_list)):
                if len(sorted_sp_bus) > 0:
                    has_repeated = False
                    for sp_bus_test in sorted_sp_bus:
                        # print(f"If {sp_bus[0]} is equal to {sp_bus_test}")
                        if sp_bus[0] == sp_bus_test:
                            has_repeated = True

                    if has_repeated is True:
                        continue

                # print(f"If {sp_bus[0]} starts with {bus_list[i][0]}")
                if sp_bus[0].startswith(str(bus_list[i][0])) is True:
                    # print(f"Found match with Bus {bus_list[i][0]} for {sp_bus[0]}.")
                    has_sorted = True
                    bus_list.insert(i + 1, sp_bus)
                    sorted_sp_bus.append(sp_bus[0])

            # Sort based on numbers in sequence
            if has_sorted is False:
                check_list = UPPERCASE_LETTERS + LOWERCASE__LETTERS
                if check_endswith(sp_bus[0], check_list) is True:
                    sp_n_bus = int(end_split(sp_bus[0], check_list)[0])

                else:
                    continue

                for i in range(len(bus_list)):
                    if (check_endswith(str(bus_list[i][0]), check_list) is True and check_startswith(
                            str(bus_list[i][0]), check_list) is False):
                        check_val_1 = int(end_split(str(bus_list[i][0]), check_list)[0])

                    elif str(bus_list[i][0]).isdigit() is True:
                        check_val_1 = int(bus_list[i][0])

                    else:
                        continue

                    if (check_endswith(str(bus_list[i + 1][0]), check_list) is True and check_startswith(
                            str(bus_list[i + 1][0]), check_list) is False):
                        check_val_2 = int(end_split(str(bus_list[i + 1][0]), check_list)[0])

                    elif str(bus_list[i + 1][0]).isdigit() is True:
                        check_val_2 = int(bus_list[i + 1][0])

                    else:
                        continue

                    if check_val_1 < sp_n_bus < check_val_2:
                        bus_list.insert(i + 1, sp_bus)
                        has_sorted = True
                        break

                    elif check_val_1 == sp_n_bus:
                        bus_list.insert(i + 1, sp_bus)
                        has_sorted = True
                        break

                    if i + 1 == len(bus_list) - 1:
                        break

            # print(sorted_sp_bus)

            if has_sorted is True:
                continue
            else:
                # print(f"No related numbers for {sp_bus[0]}. Appending at end...")
                bus_list.append(sp_bus)
                sorted_sp_bus.append(sp_bus)

        # print(bus_list)

        if fallback_header is True and debug is True:
            print(
                f"=======================================================================================\n"
                f"Bus Stop No: {bus_stop_code} Services\n"
                f"======================================================================================="
            )

        # for bus_svc in dict_data["Services"]:
        for bus_ref in bus_list:
            # Should there be an explicit to see list of bus stop numbers
            # i.e. 3 to be seen from 3, 34, ...
            if len(svc_num) > 0:
                for svc_check in svc_num:
                    svc_check_test = False
                    if svc_check == str(bus_ref[0]):
                        svc_check_test = True
                        break

                if svc_check_test is False:
                    continue

            bus_svc = dict_data["Services"][bus_ref[1]]

            # Handle 1st Bus
            if bus_svc["NextBus"]["EstimatedArrival"] != "":
                nb_dt = bus_svc["NextBus"]["EstimatedArrival"].split("+")[0]
                nb_date = nb_dt.split("T")[0].split("-")
                nb_time = nb_dt.split("T")[1].split(":")

                dt_nb = datetime.datetime(
                    day=int(nb_date[2]),
                    month=int(nb_date[1]),
                    year=int(nb_date[0]),
                    hour=int(nb_time[0]),
                    minute=int(nb_time[1]),
                    second=int(nb_time[2])
                )

                duration = round((dt_nb - dt).seconds / 60)
                if duration < 1 or duration > 1000:
                    next_bus = "Arriving"
                    duration = 0
                else:
                    next_bus = f"{duration} min"

            else:
                next_bus = "Not in Service"
                nb_time = ["X", "X", "X"]
                duration = -1

            # Handle 2nd Bus
            if bus_svc["NextBus2"]["EstimatedArrival"] != "":
                nb_dt2 = bus_svc["NextBus2"]["EstimatedArrival"].split("+")[0]
                nb_date2 = nb_dt2.split("T")[0].split("-")
                nb_time2 = nb_dt2.split("T")[1].split(":")

                dt_nb2 = datetime.datetime(
                    day=int(nb_date2[2]),
                    month=int(nb_date2[1]),
                    year=int(nb_date2[0]),
                    hour=int(nb_time2[0]),
                    minute=int(nb_time2[1]),
                    second=int(nb_time2[2])
                )

                duration2 = round((dt_nb2 - dt).seconds / 60)
                if duration2 < 1 or duration2 > 1000:
                    next_bus2 = "Arriving"
                    duration2 = 0
                else:
                    next_bus2 = f"{duration2} min"

            else:
                next_bus2 = "Not in Service"
                nb_time2 = ["X", "X", "X"]
                duration2 = -1

            # Handle 3rd Bus
            if bus_svc["NextBus3"]["EstimatedArrival"] != "":
                nb_dt3 = bus_svc["NextBus3"]["EstimatedArrival"].split("+")[0]
                nb_date3 = nb_dt3.split("T")[0].split("-")
                nb_time3 = nb_dt3.split("T")[1].split(":")

                dt_nb3 = datetime.datetime(
                    day=int(nb_date3[2]),
                    month=int(nb_date3[1]),
                    year=int(nb_date3[0]),
                    hour=int(nb_time3[0]),
                    minute=int(nb_time3[1]),
                    second=int(nb_time3[2])
                )

                duration3 = round((dt_nb3 - dt).seconds / 60)
                if duration3 < 1 or duration3 > 1000:
                    next_bus3 = "Arriving"
                    duration3 = 0
                else:
                    next_bus3 = f"{duration3} min"

            else:
                next_bus3 = "Not in Service"
                nb_time3 = ["X", "X", "X"]
                duration3 = -1

            # Deal with Post-Time Buses
            if duration3 < 0 or duration3 is None:
                # Remove 3rd bus
                next_bus3 = "Not in Service"
                nb_time3 = ["X", "X", "X"]
                duration3 = 0
                bus_svc['NextBus3']['Load'] = ""
                bus_svc['NextBus3']['Type'] = ""
                bus_svc['NextBus3']['VisitNumber'] = ""

            if duration2 < 0 or duration2 is None:
                # Move 3rd bus to 2nd
                duration2 = duration3
                next_bus2 = next_bus3
                nb_time2 = nb_time3
                bus_svc['NextBus2']['Load'] = bus_svc['NextBus3']['Load']
                bus_svc['NextBus2']['Type'] = bus_svc['NextBus3']['Type']
                bus_svc['NextBus2']['VisitNumber'] = bus_svc['NextBus3']['VisitNumber']

                # Remove 3rd bus
                next_bus3 = "Not in Service"
                nb_time3 = ["X", "X", "X"]
                duration3 = 0
                bus_svc['NextBus3']['Load'] = ""
                bus_svc['NextBus3']['Type'] = ""
                bus_svc['NextBus3']['VisitNumber'] = ""

            if duration < 0 or duration is None:
                # Move 2nd bus to 1st
                duration = duration2
                next_bus = next_bus2
                nb_time = nb_time2
                bus_svc['NextBus']['Load'] = bus_svc['NextBus2']['Load']
                bus_svc['NextBus']['Type'] = bus_svc['NextBus2']['Type']
                bus_svc['NextBus']['VisitNumber'] = bus_svc['NextBus2']['VisitNumber']

                # Remove 2nd bus
                next_bus2 = "Not in Service"
                nb_time2 = ["X", "X", "X"]
                duration2 = 0
                bus_svc['NextBus2']['Load'] = ""
                bus_svc['NextBus2']['Type'] = ""
                bus_svc['NextBus2']['VisitNumber'] = ""

            # Estimation of Durations
            if (bus_svc['NextBus']['VisitNumber'] == "1" or bus_svc['NextBus']['VisitNumber'] == "") and \
                    (bus_svc['NextBus2']['VisitNumber'] == "1" or bus_svc['NextBus2']['VisitNumber'] == "") and \
                    (bus_svc['NextBus3']['VisitNumber'] == "1" or bus_svc['NextBus3']['VisitNumber'] == ""):
                one_visit = True
                est_dur = calculate_est_duration(duration, duration2, duration3)
                est_dur_1 = 0
                est_dur_2 = 0
            else:
                one_visit = False
                visit_1 = []
                visit_2 = []

                for i in range(1, 4):
                    if i == 1:
                        key_ref = 'NextBus'
                        dur = duration
                    else:
                        key_ref = f'NextBus{i}'

                        if i == 2:
                            dur = duration2
                        else:
                            dur = duration3

                    if bus_svc[key_ref]['VisitNumber'] == "1":
                        visit_1.append(dur)
                    else:
                        visit_2.append(dur)

                if len(visit_1) < 3:
                    for i in range(3 - len(visit_1)):
                        visit_1.append(0)

                if len(visit_2) < 3:
                    for i in range(3 - len(visit_2)):
                        visit_2.append(0)

                est_dur = 0
                est_dur_1 = calculate_est_duration(visit_1[0], visit_1[1], visit_1[2])
                est_dur_2 = calculate_est_duration(visit_2[0], visit_2[1], visit_2[2])

            if debug is True:
                print(
                    f"Service [{bus_svc['ServiceNo']}] | {bus_svc['Operator']}\n"
                    f"=======================================================================================\n"
                    f"1. {next_bus} @ {nb_time[0]}:{nb_time[1]}:{nb_time[2]} ({bus_svc['NextBus']['EstimatedArrival']})"
                    f" | {interpret_seating(bus_svc['NextBus']['Load'])} | {interpret_type(bus_svc['NextBus']['Type'])}"
                    f" | Visit: {bus_svc['NextBus']['VisitNumber']}\n"
                    f"2. {next_bus2} @ {nb_time2[0]}:{nb_time2[1]}:{nb_time2[2]} "
                    f"({bus_svc['NextBus2']['EstimatedArrival']}) | {interpret_seating(bus_svc['NextBus2']['Load'])} | "
                    f"{interpret_type(bus_svc['NextBus2']['Type'])}"
                    f" | Visit: {bus_svc['NextBus2']['VisitNumber']}\n"
                    f"3. {next_bus3} @ {nb_time3[0]}:{nb_time3[1]}:{nb_time3[2]} "
                    f"({bus_svc['NextBus3']['EstimatedArrival']}) | {interpret_seating(bus_svc['NextBus3']['Load'])} | "
                    f"{interpret_type(bus_svc['NextBus3']['Type'])}"
                    f" | Visit: {bus_svc['NextBus3']['VisitNumber']}\n"
                )

                print(
                    f"Estimated Duration: {est_dur} mins" if one_visit is True else
                    f"Estimated Duration (Visit 1): {est_dur_1} mins\nEstimated Duration (Visit 2): {est_dur_2} mins"
                )

                print(
                    f"======================================================================================="
                )

            # Append Compiled Data
            bus_stop_list.append(
                (
                    bus_svc['ServiceNo'],  # [0]
                    bus_svc['Operator'],  # [1]
                    f"1.  {next_bus} @ {nb_time[0]}:{nb_time[1]}:{nb_time[2]}",  # [2]
                    f"2.  {next_bus2} @ {nb_time2[0]}:{nb_time2[1]}:{nb_time2[2]}",  # [3]
                    f"3.  {next_bus3} @ {nb_time3[0]}:{nb_time3[1]}:{nb_time3[2]}",  # [4]
                    interpret_seating(bus_svc['NextBus']['Load']),  # [5]
                    interpret_seating(bus_svc['NextBus2']['Load']),  # [6]
                    interpret_seating(bus_svc['NextBus3']['Load']),  # [7]
                    interpret_type(bus_svc['NextBus']['Type']),  # [8]
                    interpret_type(bus_svc['NextBus2']['Type']),  # [9]
                    interpret_type(bus_svc['NextBus3']['Type']),  # [10]
                    bus_svc['NextBus']['VisitNumber'] if bus_svc['NextBus']['VisitNumber'] != "" else "X",  # [11]
                    bus_svc['NextBus2']['VisitNumber'] if bus_svc['NextBus2']['VisitNumber'] != "" else "X",  # [12]
                    bus_svc['NextBus3']['VisitNumber'] if bus_svc['NextBus3']['VisitNumber'] != "" else "X",  # [13]
                    est_dur,  # [14]
                    est_dur_1,  # [15]
                    est_dur_2,  # [16]
                    one_visit,  # [17]
                    bus_svc['NextBus']['OriginCode'],  # [18]
                    bus_svc['NextBus']['DestinationCode']  # [19]
                )
            )

        return bus_stop_list
