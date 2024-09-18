import tkinter as tk
from tkinter import ttk
from emco_usbhv import EMCO_USBhv
import time


class EMCO_USBhv_App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EMCO USBhv App in Python")

        # Create an instance of EMCO_USBhv
        self.hv = EMCO_USBhv()
        
        self.create_widgets()
        # Global binding of Enter key
        self.bind("<Return>", self.set_voltage_on_enter)
        self.bind("<KP_Enter>", self.set_voltage_on_enter)

        # Start periodic status updates
        self.update_status()

    def create_widgets(self):
        # EMCO Part# dropdown
        tk.Label(self, text="Power Supply:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.part_var = tk.StringVar(value="TBD")
        ttk.Combobox(self, textvariable=self.part_var, values=["TBD"], state="readonly").grid(row=0, column=1, padx=10, pady=5)

        # Output Voltage Vpgm
        tk.Label(self, text="Set Output Voltage (V):").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.voltage_var = tk.IntVar(value=500)
        voltage_spinbox = tk.Spinbox(self, from_=0, to=2000, increment=10, textvariable=self.voltage_var)
        voltage_spinbox.grid(row=1, column=1, padx=10, pady=5)

        # Bind Enter key to update voltage when pressed
        voltage_spinbox.bind("<Return>", self.set_voltage_on_enter)
        voltage_spinbox.bind("<KP_Enter>", self.set_voltage_on_enter)

        # Set Voltage Monitor
        tk.Label(self, text="Set Voltage Monitor:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.set_voltage_var = tk.StringVar(value="---")
        tk.Label(self, textvariable=self.set_voltage_var, relief="sunken").grid(row=2, column=1, padx=10, pady=5)

        # Output Voltage Monitor 1
        tk.Label(self, text="Output Voltage Monitor 1:").grid(row=3, column=0, padx=10, pady=5, sticky='w')
        self.monitor_var1 = tk.StringVar(value="---")
        tk.Label(self, textvariable=self.monitor_var1, relief="sunken").grid(row=3, column=1, padx=10, pady=5)

        # Output Voltage Monitor 2
        tk.Label(self, text="Output Voltage Monitor 2:").grid(row=4, column=0, padx=10, pady=5, sticky='w')
        self.monitor_var2 = tk.StringVar(value="---")
        tk.Label(self, textvariable=self.monitor_var2, relief="sunken").grid(row=4, column=1, padx=10, pady=5)

        # Enable and Disable buttons on the same row
        self.enable_button = tk.Button(self, text="Enable", command=self.enable)
        self.enable_button.grid(row=5, column=0, padx=10, pady=5)
        self.disable_button = tk.Button(self, text="Disable", command=self.disable, state="disabled")
        self.disable_button.grid(row=5, column=1, padx=10, pady=5)

        # Status label
        self.status_label = tk.Label(self, text="Disabled", bg="lightgray")
        self.status_label.grid(row=6, column=0, columnspan=3, padx=10, pady=5, sticky='we')

        # Reset and Close buttons
        tk.Button(self, text="Reset", command=self.reset).grid(row=7, column=0, padx=10, pady=5)
        tk.Button(self, text="Close", command=self.quit).grid(row=7, column=1, padx=10, pady=5)

    def enable(self):
        voltage = self.voltage_var.get()
        self.hv.set_voltage(voltage)
        self.hv.enable()
        time.sleep(0.3)  # Small delay to let the power supply stabilize

        # Update monitor and status
        self.update_status()

    def disable(self):
        self.hv.disable()
        time.sleep(0.3)  # Small delay to ensure disabling happens

        # Update monitor and status
        self.update_status()

    def set_voltage(self):
        """Function to update the voltage while HV is enabled."""
        voltage = self.voltage_var.get()
        self.hv.set_voltage(voltage)
        time.sleep(0.3)  # Small delay to let the power supply stabilize

        # Update the monitor with the new voltage
        self.update_status()

    def set_voltage_on_enter(self, event):
        """Update voltage when Enter key is pressed."""
        if self.disable_button['state'] == "normal":  # Only update if enabled
            self.set_voltage()

    def update_status(self):
        """Periodically update the voltage monitors and status label."""
        try:
            status = self.hv.status()

            # Update the values on the GUI
            self.set_voltage_var.set(f"{status['set_voltage']} V")
            self.monitor_var1.set(f"{status['voltage_monitor1']} V")
            self.monitor_var2.set(f"{status['voltage_monitor2']} V")

            # Update status label based on the HV enabled state
            if status['enabled']:
                self.status_label.config(text="Enabled", bg="red")
                self.enable_button.config(state="disabled")
                self.disable_button.config(state="normal")
            else:
                self.status_label.config(text="Disabled", bg="gray")
                self.enable_button.config(state="normal")
                self.disable_button.config(state="disabled")

            # Schedule the next update after 1000ms (1 second)
            self.after(1000, self.update_status)

        except Exception as e:
            print(f"Error updating status: {e}")

    def reset(self):
        self.voltage_var.set(500)
        self.set_voltage_var.set("---")
        self.monitor_var1.set("---")
        self.monitor_var2.set("---")
        self.status_label.config(text="Disabled", bg="green")
        self.enable_button.config(state="normal")
        self.disable_button.config(state="disabled")

if __name__ == "__main__":
    app = EMCO_USBhv_App()
    app.mainloop()
