import tkinter as tk
from tkinter import ttk, filedialog
import os

"""
    Author: Abbhinav Bharadwaj
    Release Date: 01/01/25
    Purpose: Simple GUI for first release of DASH - Distributed Architecture for Scalable Hosting
    Reason: The server handlers are independent of this GUI once called, hence tkinter has been 
    used for prototyping initial releases.
    Dependencies: none
    Note: This application is a manager and serves no purpose without http.exe, https.exe, etc.  
    Compile with pyinstaller: "pyinstaller --icon=icon.ico --noconsole dash.py"
    If there are linker errors, try without --noconsole or disabling the antivirus. 
"""
def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_entry.delete(0, tk.END) 
        directory_entry.insert(0, directory)
        print(f"Selected Directory: {directory}")
        
def enable_http():
    http_port = http_port_entry.get()
    directory = directory_entry.get()
    if directory == "":
        print("Directory not selected")
    else:
        args=[directory, http_port]
        exe=r"http.exe"
        print([exe]+args)
        os.system(f'start cmd /k "{exe} {directory} {http_port}')
        print(f"HTTP port {http_port} enabled!")

def enable_https():
    https_port = https_port_entry.get()
    print(f"HTTPS port {https_port} enabled!")

root = tk.Tk()
root.title("DASH: Configure Web Server")
root.iconbitmap("logo.ico")
root.configure(bg="white")  

directory_label = tk.Label(root, text="Directory:", bg="white")
directory_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

directory_entry = ttk.Entry(root, width=40)
directory_entry.grid(row=0, column=1, padx=5, pady=5)

directory_button = ttk.Button(root, text="Select", command=select_directory)
directory_button.grid(row=0, column=2, padx=5, pady=5)

http_port_label = tk.Label(root, text="HTTP Port:", bg="white")
http_port_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

http_port_entry = ttk.Entry(root, width=40)
http_port_entry.grid(row=1, column=1, padx=0, pady=5)

http_button = ttk.Button(root, text="Start", command=enable_http)
http_button.grid(row=1, column=2, padx=5, pady=5)

https_port_label = tk.Label(root, text="HTTPS Port:", bg="white")
https_port_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

https_port_entry = ttk.Entry(root,width=40)
https_port_entry.grid(row=2, column=1, padx=0, pady=5)

https_button = ttk.Button(root, text="Start", command=enable_https)
https_button.grid(row=2, column=2, padx=5, pady=5)

root.mainloop()
