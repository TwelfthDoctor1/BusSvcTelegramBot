import os
import telebot
from dotenv import load_dotenv
from pathlib import Path
from telebot import types
from TransportAPI.APIHandler import TransportAPIHandler
from TransportAPI.BusStopInfo import store_bus_stop_data, request_bus_stop_code_from_name
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
gen_state = json_mem.generate_json({"NULL_DATA": ""})  # Temp Dict creation
json_mem.formulate_json()

if gen_state:
    json_mem.delete_json_entry("NULL_DATA")  # Temp Dict Removal


# ======================================================================================================================
# Commands
@bot.message_handler(commands=["start"])
def bot_svc_start(message: types.Message):
    msg = "Welcome to the Bus Timings Telegram Bot.\n" \
          "To start, please type /query_timing.\n\n" \
          "Program created by TwelfthDoctor1."
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=["query_timing"])
def query_timing(message: types.Message):
    sent_msg = bot.send_message(
        message.chat.id,
        "Enter either the following to query bus timings:"
        "\n- 5-digit Bus Stop Code"
        "\n- Bus Stop Name and/or Road Name (i.e. Aft Blk 87 @ Zion Road)"
    )
    bot.register_next_step_handler(sent_msg, explicit_buses)


def explicit_buses(message: types.Message):
    if message.text == "/cancel":
        bot.send_message(message.chat.id, "Action cancelled.")
        return

    bus_stop_code = message.text
    sent_msg = bot.send_message(message.chat.id, "Enter the explicit bus services to see only. Otherwise leave 0"
                                                 " to see all services. (i.e.: 5, 12e, 46)")
    bot.register_next_step_handler(sent_msg, parse_data, bus_stop_code)


def parse_data(message: types.Message, bus_stop_info: str, bus_svc_list_str: str = ""):
    mem_dict = dict()

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
        "List of Commands\n\nTo refresh: /refresh\nTo query: /query_timing\nTo clear: /clear"
    )

    # Save data to JSON Mem
    json_mem.update_specific_json(f"{message.chat.username}", mem_dict)
    json_mem.update_json_file()


@bot.message_handler(commands=["refresh"])
def refresh_timings(message: types.Message):
    mem_dict = json_mem.return_specific_json(f"{message.chat.username}")

    if mem_dict["bus_mem"] == "":
        bot.send_message(message.chat.id, "You have not queried for a bus timing. Please use /query_timing instead.")
        return

    parse_data(message, mem_dict["bus_mem"], mem_dict["svc_mem"])


@bot.message_handler(commands=["clear"])
def clear_mem(message: types.Message):
    mem_dict = json_mem.return_specific_json(f"{message.chat.username}")

    mem_dict["bus_mem"] = ""
    mem_dict["svc_mem"] = []

    json_mem.update_specific_json(f"{message.chat.username}", mem_dict)
    json_mem.update_json_file()

    bot.send_message(message.chat.id, "Memory cleared. Please use /query_timing to start again.")


# Start Bot and detect commands
bot.infinity_polling()
