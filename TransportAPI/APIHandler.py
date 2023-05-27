from TransportAPI.BusStopInfo import request_bus_stop_name_lta, return_bus_stop_name_json
from TransportAPI.BusArrival import request_bus_stop_timing
from TransportAPI.BusService import return_bus_svc_json


class TransportAPIHandler:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def request_arrival_time(self, bus_stop_code: str, explicit_buses: list):
        curr_stop_returner = request_bus_stop_name_lta(bus_stop_code, self.api_key)
        arrival_returner = request_bus_stop_timing(bus_stop_code, self.api_key, explicit_buses)
        main_returner = []

        if curr_stop_returner[2] is True:
            print(
                f"=======================================================================================\n"
                f"{curr_stop_returner[0]} @ {curr_stop_returner[1]} [{bus_stop_code}]\n"
                f"======================================================================================="
            )
            main_returner.append(f"{curr_stop_returner[0]} @ {curr_stop_returner[1]} [{bus_stop_code}]")
        else:
            print(
                f"=======================================================================================\n"
                f"Bus Stop No: {bus_stop_code} Services\n"
                f"======================================================================================="
            )
            main_returner.append(f"Bus Stop No: {bus_stop_code} Services")

        if len(arrival_returner) == 0:
            print(
                f"There is no bus services available.\n"
                f"======================================================================================="
            )
            main_returner.append(f"There is no bus services available.")
            return main_returner

        for arrival_data in arrival_returner:
            svc_info_returner = return_bus_svc_json(arrival_data[0], 1)

            if svc_info_returner[4] != arrival_data[18] and svc_info_returner[5] != arrival_data[19]:
                svc_info_returner = return_bus_svc_json(arrival_data[0], 2)

            if svc_info_returner[7] is False:
                svc_info = f"{return_bus_stop_name_json(svc_info_returner[4])[0]} >>> " \
                           f"{return_bus_stop_name_json(svc_info_returner[5])[0]} " \
                           f"[{svc_info_returner[3]}]"

            elif svc_info_returner[7] is True:
                svc_info = f"Loop @ {svc_info_returner[6]} to " \
                           f"{return_bus_stop_name_json(svc_info_returner[5])[0]} " \
                           f"[{svc_info_returner[3]}]"

            else:
                svc_info = f"This service does not exist."

            print(
                f"Service [{arrival_data[0]}] | {arrival_data[1]}\n"
                f"{svc_info}\n"
                f"=======================================================================================\n"
                f"{arrival_data[2]} | {arrival_data[5]} | {arrival_data[8]} | Visit: {arrival_data[11]}\n"
                f"{arrival_data[3]} | {arrival_data[6]} | {arrival_data[9]} | Visit: {arrival_data[12]}\n"
                f"{arrival_data[4]} | {arrival_data[7]} | {arrival_data[10]} | Visit: {arrival_data[13]}\n"
            )

            print(
                f"Estimated Duration: {arrival_data[14]} min" if arrival_data[17] is True else
                f"Estimated Duration (Visit 1): {arrival_data[15]} min\n"
                f"Estimated Duration (Visit 2): {arrival_data[16]} min"
            )

            print(
                f"======================================================================================="
            )

            main_returner.append(
                [
                    f"Service [{arrival_data[0]}] | {arrival_data[1]}",
                    f"{svc_info}",
                    f"{arrival_data[2]} | {arrival_data[5]} | {arrival_data[8]} | Visit: {arrival_data[11]}",
                    f"{arrival_data[3]} | {arrival_data[6]} | {arrival_data[9]} | Visit: {arrival_data[12]}",
                    f"{arrival_data[4]} | {arrival_data[7]} | {arrival_data[10]} | Visit: {arrival_data[13]}",
                    f"Estimated Duration: {arrival_data[14]} min" if arrival_data[17] is True else
                    f"Estimated Duration (Visit 1): {arrival_data[15]} min\n"
                    f"Estimated Duration (Visit 2): {arrival_data[16]} min"
                ]
            )
        return main_returner
