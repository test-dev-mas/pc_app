import csv, os, serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from PIL import ImageTk, Image


class Model(serial.Serial):
    def __init__(self):
        super().__init__()

        self.arduino_port = None

        for port in serial.tools.list_ports.comports():
            if port.pid == 0x7523 and port.vid == 0x1a86:
                self.arduino_port = port.device

        if self.arduino_port is None:
            raise ValueError('Device not found')

        self.port = self.arduino_port
        self.baudrate = 115200
        self.timeout = 10
        self.open()


        # self.data = data

        self.header = ["Date/Time", "QR CODE", "POWER ON", "GROUND", "PILOT STATE A", "PILOT STATE B", "DIODE", "OVER CURRENT",
        "GFCI_L1_LOW LEAKAGE", "GFCI_L1_HIGH LEAKAGE", "GFCI_L2_LOW LEAKAGE", "GFCI_L2_HIGH LEAKAGE", "STUCK RELAY"]

        self.save(self.header)

    def save(self, data):
        dir_name = 'log'

        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
            print("Directory", dir_name, "created")
        else:
            print("Directory", dir_name, "already exists")

        with open(dir_name + '/01.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(data)

# three frames make up the app windows: navigation, test, individual result

# navigation frame
class navigation_frame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # self.rowconfigure(0, weight=1)
        # self.rowconfigure(1, weight=1)
        # self.rowconfigure(2, weight=1)
        # self.rowconfigure(3, weight=1)

        self.png = Image.open("msi_logo.png")
        self.png_resized = self.png.resize((250,48))
        self.img = ImageTk.PhotoImage(self.png_resized)
        self.logo = ttk.Label(self, image=self.img)
        self.logo.grid(row=0, column=0, sticky="nsew")

        self.command_button_1 = ttk.Button(self, text="Run Test", command=self.show_frame_2)
        self.command_button_1.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.command_button_2 = ttk.Button(self, text="Check Result", command=self.show_frame_3)
        self.command_button_2.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        self.version_number = ttk.Label(self, text="Versoin 0.1")
        self.version_number.grid(row=3, column=0, sticky="sw", padx=10, pady=10)

        self.grid(column=0, row=0, sticky="n")

        self.frames = {}
        self.frames[0] = result_frame(container)
        self.frames[1] = test_frame(container)

    def show_frame_2(self):
        frame = self.frames[1]
        frame.tkraise()

    def show_frame_3(self):
        frame = self.frames[0]
        frame.tkraise()

# test frame
class test_frame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.test_button_state = 0

        self.test_button = ttk.Button(self, text="Start",command=self.test_button_clicked)
        self.test_button.grid(column=0, rowspan=4, sticky="nsew", padx=10, pady=10)

        self.serial_number_label = ttk.Label(self, text="Serial Number")
        self.serial_number_label.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.serial_number_entry = ttk.Entry(self)
        self.serial_number_entry.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.operator_number_label = ttk.Label(self, text="Operator Number")
        self.operator_number_label.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

        self.operator_number_entry = ttk.Entry(self)
        self.operator_number_entry.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)

        self.test_window = ScrolledText(self)
        self.test_window.grid(row=4,columnspan=2)
        self.test_window.insert(tk.INSERT, "PC app ready" + '\n')

        self.grid(column=1, row=0, sticky="nsew")

        # set controller
        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def test_button_clicked(self):
        if self.test_button_state == 0:
            self.test_button_state = 1    
            self.test_button.configure(text="Abort")

            self.test_window.insert(tk.INSERT, "Starting test ..." + '\n')

            if self.controller:
                self.controller.start_test()

        elif self.test_button_state == 1:
            self.test_button_state = 0
            self.test_button.configure(text="Start")

            self.test_window.insert(tk.INSERT, "Stoping test ..." + '\n')

            if self.controller:
                self.controller.abort_test()

# results frame
class result_frame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        tree = ttk.Treeview(self)
        tree.grid(column=0, row=0, sticky="nsew")

        self.grid(column=1, row=0, sticky="nsew")

class Controller():
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def start_test(self):
        # TODO: SEND SERIAL TO AVR
        print("start test")

    def abort_test(self):
        # TODO: SEND SERIAL TO AVR
        print("abort test")

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # self.app_width = 1000
        # self.app_height = 800
        # self.centre_x = int(self.winfo_screenwidth()/2 - self.app_width/2)
        # self.centre_y = int(self.winfo_screenheight()/2 - self.app_height/2)

        self.title("GRIZZLE AUTOMATED TEST")
        # self.geometry(f'{self.app_width}x{self.app_height}+{self.centre_x}+{self.centre_y}')
        # self.minsize(self.app_width,self.app_height)

        # self.rowconfigure(0, weight=1)
        # self.rowconfigure(1, weight=1)
        # self.rowconfigure(2, weight=1)
        # self.rowconfigure(3, weight=1)
        # self.columnconfigure(0, weight=1)
        # self.columnconfigure(1, weight=6)

        # create a model
        model = Model()

        # create a view and place it on root window
        view = navigation_frame(self)
        # navigation_frame also handles switching of test_frame and result_frame

        # create a controller
        controller = Controller(model, view)

        # it's a little convoluted, frames[1] is a instance of test_frame created inside an instance of navigation_frame
        view.frames[1].set_controller(controller)

if __name__ == "__main__":
    app = App()
    app.mainloop()