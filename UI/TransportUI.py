import sys
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QTableWidget
from TransportAPI.BusArrival import request_bus_stop_timing
from TransportAPI.BusService import return_bus_svc_json
from TransportAPI.BusStopInfo import request_bus_stop_name_lta, return_bus_stop_name_json
from UI.UI_TransportUI import Ui_TransportService


class TransportMenu(QMainWindow):
    def __init__(self, parser: list, parent=None):
        super().__init__(parent=parent)
        self.ui = Ui_TransportService()
        self.parser = parser

        # Setup UI
        self.ui.setupUi(self)

        # Lock Cells
        self.lockCells()

    def parseBusStopNumber(self):
        bus_count = 0
        bus_stop_num = self.ui.BusStopNumber.text()
        svc_list_str = self.ui.ExplicitSvcList.text()

        if svc_list_str == "":
            bus_svc_list = []

        else:
            bus_svc_list = svc_list_str.split(",")

            for i in range(len(bus_svc_list)):
                bus_svc_list[i] = bus_svc_list[i].strip()

        # Request For Data

        header_check = request_bus_stop_name_lta(bus_stop_num, self.parser[0])
        fallback_header = not header_check[2]
        bus_stop_list = request_bus_stop_timing(
            bus_stop_num, self.parser[0], bus_svc_list, fallback_header)

        # Clear Table
        self.ui.BusStopTable.clear()

        # Create Table w Row & Columns
        bus_num = len(bus_stop_list)
        self.ui.BusStopTable.setRowCount(bus_num * 10)
        self.ui.BusStopTable.setColumnCount(5)

        if fallback_header is False:
            self.ui.BusStopTable.setItem(0, 0, QTableWidgetItem(f"{header_check[0]} @ {header_check[1]}"))
            self.ui.BusStopTable.setItem(0, 1, QTableWidgetItem(f"[{bus_stop_num}]"))
        else:
            self.ui.BusStopTable.setItem(0, 0, QTableWidgetItem(f"Bus Services for: "))
            self.ui.BusStopTable.setItem(0, 1, QTableWidgetItem(f"{bus_stop_num}"))

        # Populate Table
        for bus in bus_stop_list:
            # Handle Row
            row_designation = [1, 2, 3, 4, 5, 6, 7, 8, 9]

            for i in range(bus_count):
                for j in range(len(row_designation)):
                    k = row_designation[j]
                    k += 10
                    row_designation[j] = k

            # Service Header
            self.ui.BusStopTable.setItem(row_designation[0], 0, QTableWidgetItem(f"Service [{bus[0]}]"))
            self.ui.BusStopTable.setItem(row_designation[0], 1, QTableWidgetItem(f"{bus[1]}"))

            svc_info_returner = return_bus_svc_json(bus[0], 1)

            if svc_info_returner[4] != bus[18] and svc_info_returner[5] != bus[19]:
                svc_info_returner = return_bus_svc_json(bus[0], 2)

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

            self.ui.BusStopTable.setItem(row_designation[1], 0, QTableWidgetItem(svc_info))

            # Next Bus
            self.ui.BusStopTable.setItem(row_designation[3], 0, QTableWidgetItem(f"{bus[2]}"))
            self.ui.BusStopTable.setItem(row_designation[3], 1, QTableWidgetItem(f"{bus[5]}"))
            self.ui.BusStopTable.setItem(row_designation[3], 2, QTableWidgetItem(f"{bus[8]}"))
            self.ui.BusStopTable.setItem(row_designation[3], 3, QTableWidgetItem(f"Visit: {bus[11]}"))

            # 2nd Bus
            self.ui.BusStopTable.setItem(row_designation[4], 0, QTableWidgetItem(f"{bus[3]}"))
            self.ui.BusStopTable.setItem(row_designation[4], 1, QTableWidgetItem(f"{bus[6]}"))
            self.ui.BusStopTable.setItem(row_designation[4], 2, QTableWidgetItem(f"{bus[9]}"))
            self.ui.BusStopTable.setItem(row_designation[4], 3, QTableWidgetItem(f"Visit: {bus[12]}"))

            # 3rd Bus
            self.ui.BusStopTable.setItem(row_designation[5], 0, QTableWidgetItem(f"{bus[4]}"))
            self.ui.BusStopTable.setItem(row_designation[5], 1, QTableWidgetItem(f"{bus[7]}"))
            self.ui.BusStopTable.setItem(row_designation[5], 2, QTableWidgetItem(f"{bus[10]}"))
            self.ui.BusStopTable.setItem(row_designation[5], 3, QTableWidgetItem(f"Visit: {bus[13]}"))

            # Estimated Time
            if bus[17] is True:
                self.ui.BusStopTable.setItem(row_designation[7], 0, QTableWidgetItem(f"Estimated Duration:"))
                self.ui.BusStopTable.setItem(row_designation[7], 1, QTableWidgetItem(f"{bus[14]} min"))
            else:
                self.ui.BusStopTable.setItem(row_designation[7], 0, QTableWidgetItem(f"Estimated Duration (Visit 1):"))
                self.ui.BusStopTable.setItem(row_designation[7], 1, QTableWidgetItem(f"{bus[15]} min"))
                self.ui.BusStopTable.setItem(row_designation[8], 0, QTableWidgetItem(f"Estimated Duration (Visit 2):"))
                self.ui.BusStopTable.setItem(row_designation[8], 1, QTableWidgetItem(f"{bus[16]} min"))

            bus_count += 1

        # Update Table
        self.updateTable()
        self.updateTable()

        self.ui.statusbar.showMessage("Bus Arrival Timing Data acquired & loaded.", 2000)

    def resizeEvent(self, a0: QResizeEvent):
        self.ui.BusStopTable.update()
        self.ui.BusStopTable.resizeRowsToContents()
        self.ui.BusStopTable.resizeColumnsToContents()
        QMainWindow.resizeEvent(self, a0)

    def lockCells(self):
        self.ui.BusStopTable.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    def updateTable(self):
        self.ui.BusStopTable.update()
        self.ui.BusStopTable.resizeRowsToContents()
        self.ui.BusStopTable.resizeColumnsToContents()
        self.lockCells()


def parse_to_ui(parser: list):
    app = QApplication(sys.argv)
    window = TransportMenu(parser=parser)
    window.show()
    app.exec()
