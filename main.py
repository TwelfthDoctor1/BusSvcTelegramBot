import os
import telebot
from dotenv import load_dotenv
from pathlib import Path
from telebot import types
from TransportAPI.APIHandler import TransportAPIHandler
from TransportAPI.BusStopInfo import store_bus_stop_data, request_bus_stop_code_from_name, get_nearby_bus_stops, \
    return_bus_stop_name_json
from TransportAPI.BusService import store_bus_svc_data
from UtilLib.JSONHandler import JSONHandler

ENV_PATH = os.path.join(Path(__file__).resolve().parent, "RefKey.env")

# Load ENV
load_dotenv(dotenv_path=ENV_PATH)

# Get Values from ENV
API_KEY_TG = os.getenv("BOT_KEY")
API_KEY_LTA = os.getenv("API_KEY_LTA")
ENV_LIST = [API_KEY_LTA]

# API Handling & Data Caching
api_handler = TransportAPIHandler(API_KEY_LTA)
store_bus_stop_data(API_KEY_LTA)
store_bus_svc_data(API_KEY_LTA)

bot = telebot.TeleBot(API_KEY_TG)

# ======================================================================================================================
# JSON Memory Handling
json_mem = JSONHandler("MemoryData")
gen_state = json_mem.generate_json(dict())
json_mem.formulate_json()


# ======================================================================================================================
# Commands
@bot.message_handler(commands=["start"])
def bot_svc_start(message: types.Message):
    msg = "Welcome to the Bus Timings Telegram Bot.\n" \
          "To start, please type /query_timing or /search.\n\n" \
          "Program created by TwelfthDoctor1."
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=["query_timing"])
def query_timing(message: types.Message):
    sent_msg = bot.send_message(
        message.chat.id,
        "Enter either the following to query bus timings:"
        "\n- 5-digit Bus Stop Code"
        "\n- Bus Stop Name and/or Road Name (i.e. Aft Blk 87 @ Zion Road OR Aft Blk 87)"
    )
    bot.register_next_step_handler(sent_msg, filter_explicit_buses)


@bot.message_handler(commands=["filter"])
def filter_preface(message: types.Message):
    mem_dict = json_mem.return_specific_json(f"{message.chat.username}")

    if mem_dict["bus_mem"] == "":
        bot.send_message(message.chat.id, "You cannot filter for explicit buses if you have not queried for a bus "
                                          "timing. Please use /query_timing or /search instead.")
        return

    return filter_explicit_buses(message, mem_dict["bus_mem"])


def filter_explicit_buses(message: types.Message, bus_stop_code: str or list = ""):
    msg = f"Bus Stops matching {bus_stop_code}\n"
    if message.text == "/cancel":
        bot.send_message(message.chat.id, "Action cancelled.")
        return

    if bus_stop_code == "":
        bus_stop_code = message.text

    if not bus_stop_code.isdigit() and not isinstance(bus_stop_code, list):
        bus_stop_info_data = bus_stop_code.split("@")

        for i in range(len(bus_stop_info_data)):
            bus_stop_info_data[i] = bus_stop_info_data[i].strip()

        if len(bus_stop_info_data) == 1:
            bus_stop_code = request_bus_stop_code_from_name(bus_stop_info_data[0])
        else:
            bus_stop_code = request_bus_stop_code_from_name(bus_stop_info_data[0], bus_stop_info_data[1])

    if isinstance(bus_stop_code, str):
        inner_filter_proc(message, bus_stop_code)

    elif isinstance(bus_stop_code, list):
        for i in range(len(bus_stop_code)):
            msg += f"\n{i + 1}. {bus_stop_code[i][1]} @ {bus_stop_code[i][2]} [{bus_stop_code[i][0]}]"

        msg += "\n\nEnter the list number to view the bus timings for that bus stop or /cancel to stop filter: "

        sent_msg = bot.send_message(message.chat.id, msg)
        bot.register_next_step_handler(sent_msg, pre_filter_get_bus_stop, bus_stop_code)


def pre_filter_get_bus_stop(message: types.Message, bus_stop_code):
    if message.text == "/cancel":
        bot.send_message(message.chat.id, "Action cancelled.")
        return

    elif message.text.isdigit() is False:
        bot.send_message(message.chat.id, "Unknown option. Please try again.")
        return filter_explicit_buses(message, bus_stop_code)

    elif int(message.text) <= 0 or int(message.text) > len(bus_stop_code):
        bot.send_message(message.chat.id, "Option out of range. Please try again.")
        return filter_explicit_buses(message, bus_stop_code)

    return inner_filter_proc(message, bus_stop_code[int(message.text) - 1][0])


def inner_filter_proc(message: types.Message, bus_stop_code: str = ""):
    svc_list = api_handler.request_bus_stop_svc_list(bus_stop_code)

    bot.send_message(message.chat.id, "Enter the explicit bus services to see only. Otherwise leave 0"
                     " to see all services. (i.e.: 5, 12e, 46)")

    sent_msg = bot.send_message(message.chat.id, f"Services:\n{svc_list}")
    bot.register_next_step_handler(sent_msg, parse_data, bus_stop_code)


def parse_data(message: types.Message, bus_stop_info: str, bus_svc_list_str: str = ""):
    mem_dict = json_mem.return_specific_json(f"{message.chat.username}")

    if message.text == "/cancel":
        bot.send_message(message.chat.id, "Action cancelled.")
        return

    if bus_stop_info.isdigit():
        bus_stop_code = bus_stop_info

    else:
        bus_stop_info_data = bus_stop_info.split("@")

        for i in range(len(bus_stop_info_data)):
            bus_stop_info_data[i] = bus_stop_info_data[i].strip()

        if len(bus_stop_info_data) == 1:
            bus_stop_code = request_bus_stop_code_from_name(bus_stop_info_data[0])
        else:
            bus_stop_code = request_bus_stop_code_from_name(bus_stop_info_data[0], bus_stop_info_data[1])

    if bus_svc_list_str == "":
        bus_svc_list_str = message.text

    if bus_svc_list_str == "0":
        bus_svc_list = []
        mem_dict["svc_mem"] = []

    elif isinstance(bus_svc_list_str, list):
        bus_svc_list = bus_svc_list_str
        mem_dict["svc_mem"] = bus_svc_list

    else:
        bus_svc_list = bus_svc_list_str.split(",")

        for i in range(len(bus_svc_list)):
            bus_svc_list[i] = bus_svc_list[i].strip()

        mem_dict["svc_mem"] = bus_svc_list

    # Formulate Header & Get Arrival Time

    # Custom Bus Stop
    mem_dict["bus_mem"] = bus_stop_code
    returner = api_handler.request_arrival_time(bus_stop_code, bus_svc_list)

    bot.send_message(message.chat.id, returner[0])

    if len(returner) == 1:
        return

    for i in range(1, len(returner)):
        if isinstance(returner[i], str) and i == 1:
            bot.send_message(message.chat.id, returner[i])
            break

        bot.send_message(
            message.chat.id,
            f"{returner[i][0]}\n{returner[i][1]}\n\n{returner[i][2]}\n{returner[i][3]}\n{returner[i][4]}\n"
            f"\n{returner[i][5]}"
        )

    bot.send_message(
        message.chat.id,
        "List of Commands\n\nTo refresh: /refresh\nTo query: /query_timing\nTo search: /search\nTo filter: /filter"
        "\nTo clear: /clear"
    )

    # Save data to JSON Mem
    json_mem.update_specific_json(f"{message.chat.username}", mem_dict)
    json_mem.update_json_file()


@bot.message_handler(commands=["refresh"])
def refresh_timings(message: types.Message):
    mem_dict = json_mem.return_specific_json(f"{message.chat.username}")

    if mem_dict["bus_mem"] == "":
        bot.send_message(
            message.chat.id, "You have not queried for a bus timing. Please use /query_timing or /search instead."
        )
        return

    parse_data(message, mem_dict["bus_mem"], mem_dict["svc_mem"])


@bot.message_handler(commands=["clear"])
def clear_mem(message: types.Message):
    mem_dict = json_mem.return_specific_json(f"{message.chat.username}")

    mem_dict["bus_mem"] = ""
    mem_dict["svc_mem"] = []

    json_mem.update_specific_json(f"{message.chat.username}", mem_dict)
    json_mem.update_json_file()

    bot.send_message(message.chat.id, "Memory cleared. Please use /query_timing or /search to start again.")


@bot.message_handler(commands=["search"])
def search_query(message: types.Message):
    button_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    location_button = types.KeyboardButton("Send Location", request_location=True)
    cancel_button = types.KeyboardButton("Cancel")
    button_kb.add(location_button, cancel_button)

    sent_msg = bot.send_message(
        message.chat.id, "Select the \"Send Location\" button to send your location, or use the \"Attachment\" button "
                         "to send a location. To exit, press \"Cancel\".",
        reply_markup=button_kb
    )
    bot.register_next_step_handler(sent_msg, search_query_proc)


def search_query_proc(message: types.Message):
    if message.text == "Cancel":
        bot.send_message(message.chat.id, "Action cancelled.", reply_markup=types.ReplyKeyboardRemove())
        return

    lon = message.location.longitude
    lat = message.location.latitude

    nearby_stops = get_nearby_bus_stops(lon, lat)

    msg = "Nearby Bus Stops\n"

    if len(nearby_stops) == 0:
        msg += f"\nNo nearby Bus Stops."

    else:
        for i in range(len(nearby_stops)):
            msg += f"\n{i + 1}. {nearby_stops[i][2]} @ {nearby_stops[i][1]} [{nearby_stops[i][0]}] " \
                   f"({nearby_stops[i][3]} m)"

        msg += "\n\nEnter the list number to view the bus timings for that bus stop or /cancel to stop: "

    sent_msg = bot.send_message(message.chat.id, msg, reply_markup=types.ReplyKeyboardRemove())

    bot.register_next_step_handler(sent_msg, post_search_query, nearby_stops)


def post_search_query(message: types.Message, nearby_stops: list):
    if message.text == "/cancel":
        bot.send_message(message.chat.id, "Action cancelled.")
        return

    elif message.text.isdigit() is False:
        bot.send_message(message.chat.id, "Unknown option. Please try again.")
        return search_query(message)

    elif int(message.text) <= 0 or int(message.text) > len(nearby_stops):
        bot.send_message(message.chat.id, "Option out of range. Please try again.")
        return search_query(message)

    return filter_explicit_buses(message, nearby_stops[int(message.text) - 1][0])


@bot.message_handler(commands=["add_to_favourites"])
def add_to_favourites(message: types.Message):
    mem_dict = json_mem.return_specific_json(f"{message.chat.username}")

    if mem_dict["bus_mem"] == "":
        bot.send_message(
            message.chat.id, "You have not queried for a bus timing. Please use /query_timing or /search instead."
        )
        return

    # ERROR AREA
    if mem_dict.get("favourites") is not None:
        mem_dict["favourites"].append([mem_dict["bus_mem"], mem_dict["svc_mem"]])

    else:
        mem_dict["favourites"] = [[mem_dict["bus_mem"], mem_dict["svc_mem"]]]

    json_mem.update_specific_json(f"{message.chat.username}", mem_dict)
    json_mem.update_json_file()

    bot.send_message(message.chat.id, "The current bus timing query has been added to favourites.")


@bot.message_handler(commands=["favourites"])
def list_favourites(message: types.Message):
    mem_dict = json_mem.return_specific_json(f"{message.chat.username}")

    if mem_dict.get("favourites") is None or mem_dict.get("favourites") == []:
        bot.send_message(
            message.chat.id, "No favourite bus timing queries."
        )
        return

    msg = "Bus Timing Favourites\n"

    for i in range(len(mem_dict["favourites"])):
        msg += f"\n{i + 1}. {return_bus_stop_name_json(mem_dict['favourites'][i][0])[0]} | " \
               f"{str(mem_dict['favourites'][i][1])}"

    msg += f"\n\nEnter the list number to view the bus timings for that bus stop or /cancel to stop: "

    sent_msg = bot.send_message(message.chat.id, msg)

    bot.register_next_step_handler(sent_msg, fav_post_proc, mem_dict["favourites"])


def fav_post_proc(message: types.Message, fav_list):
    if message.text == "/cancel":
        bot.send_message(message.chat.id, "Action cancelled.")
        return

    elif message.text.isdigit() is False:
        bot.send_message(message.chat.id, "Unknown option. Please try again.")
        return list_favourites(message)

    elif int(message.text) <= 0 or int(message.text) > len(fav_list):
        bot.send_message(message.chat.id, "Option out of range. Please try again.")
        return list_favourites(message)

    return parse_data(message, fav_list[int(message.text) - 1][0], fav_list[int(message.text) - 1][1])


@bot.message_handler(commands=["delete_from_favourites"])
def delete_favourites_list(message: types.Message):
    mem_dict = json_mem.return_specific_json(f"{message.chat.username}")

    if mem_dict.get("favourites") is None or len(mem_dict["favourites"]) == 0:
        bot.send_message(
            message.chat.id, "No favourite bus timing queries."
        )
        return

    msg = "Bus Timing Favourites\n"

    for i in range(len(mem_dict["favourites"])):
        msg += f"\n{i + 1}. {return_bus_stop_name_json(mem_dict['favourites'][i][0])[0]} | " \
               f"{str(mem_dict['favourites'][i][1])}"

    msg += f"\n\nEnter the list number to delete that bus timing for that bus stop or /cancel to stop: "

    sent_msg = bot.send_message(message.chat.id, msg)

    bot.register_next_step_handler(sent_msg, del_fav_proc, mem_dict["favourites"])


def del_fav_proc(message: types.Message, fav_list):
    if message.text == "/cancel":
        bot.send_message(message.chat.id, "Action cancelled.")
        return

    elif message.text.isdigit() is False:
        bot.send_message(message.chat.id, "Unknown option. Please try again.")
        return delete_favourites_list(message)

    elif int(message.text) <= 0 or int(message.text) > len(fav_list):
        bot.send_message(message.chat.id, "Option out of range. Please try again.")
        return delete_favourites_list(message)

    mem_dict = json_mem.return_specific_json(f"{message.chat.username}")

    mem_dict["favourites"].pop(int(message.text) - 1)

    json_mem.update_specific_json(f"{message.chat.username}", mem_dict)
    json_mem.update_json_file()

    bot.send_message(message.chat.id, "The selected bus timing has been deleted from favourites.")


# Start Bot and detect commands
bot.infinity_polling()
