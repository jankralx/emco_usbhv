import tkinter as tk
from tkinter import ttk

class EMCO_USBhv_App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EMCO USBhv App in Python")

        self.create_widgets()

    def create_widgets(self):
        # EMCO Part# dropdown
        tk.Label(self, text="Power Supply:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.part_var = tk.StringVar(value="TBD")
        ttk.Combobox(self, textvariable=self.part_var, values=["TBD"], state="readonly").grid(row=0, column=1, padx=10, pady=5)

        # Output Voltage Vpgm
        tk.Label(self, text="Set Output Voltage (V):").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.voltage_var = tk.IntVar(value=500)
        tk.Spinbox(self, from_=0, to=2000, textvariable=self.voltage_var).grid(row=1, column=1, padx=10, pady=5)

        # Output Voltage Monitor 1
        tk.Label(self, text="Output Voltage Monitor 1:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.monitor_var = tk.StringVar(value="---")
        tk.Label(self, textvariable=self.monitor_var, relief="sunken").grid(row=2, column=1, padx=10, pady=5)

        # Output Voltage Monitor 2
        tk.Label(self, text="Output Voltage Monitor 2:").grid(row=3, column=0, padx=10, pady=5, sticky='w')
        self.monitor_var = tk.StringVar(value="---")
        tk.Label(self, textvariable=self.monitor_var, relief="sunken").grid(row=3, column=1, padx=10, pady=5)

        # Enable and Disable buttons
        self.enable_button = tk.Button(self, text="Enable", command=self.enable)
        self.enable_button.grid(row=4, column=0, padx=10, pady=5)
        self.disable_button = tk.Button(self, text="Disable", command=self.disable, state="disabled")
        self.disable_button.grid(row=4, column=1, padx=10, pady=5)
        # Status label
        tk.Label(self, text="Disabled", bg="lightgray").grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky='we')
        
        # Reset and Close buttons
        tk.Button(self, text="Reset", command=self.reset).grid(row=6, column=0, padx=10, pady=5)
        tk.Button(self, text="Close", command=self.quit).grid(row=6, column=1, padx=10, pady=5)

    def enable(self):
        self.monitor_var.set(self.voltage_var.get())
        self.enable_button.config(state="disabled")
        self.disable_button.config(state="normal")

    def disable(self):
        self.monitor_var.set("---")
        self.enable_button.config(state="normal")
        self.disable_button.config(state="disabled")

    def reset(self):
        self.voltage_var.set(500)
        self.monitor_var.set("---")
        self.enable_button.config(state="normal")
        self.disable_button.config(state="disabled")

if __name__ == "__main__":
    app = EMCO_USBhv_App()
    app.mainloop()
