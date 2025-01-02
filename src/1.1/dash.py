import tkinter as tk
from tkinter import ttk, filedialog
import os
import subprocess 
from PIL import Image, ImageTk
import sys
# import sys
# Function to open directory selector
instances=0
status_string=""
directories=[]
processes=[]
first=True
# daemon_frames=[]
current_dframe=5
if sys.platform=='win32':
    creation_flags=subprocess.CREATE_NO_WINDOW
else: 
    creation_flags = 0
def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_entry.delete(0, tk.END)  # Clear existing text
        directory_entry.insert(0, directory)  # Set selected directory
        print(f"Selected Directory: {directory}")
        
# Function to handle enabling HTTP port
def enable_http():
    global instances, status_string, directories, daemon_frames, current_dframe, first
    http_port = http_port_entry.get()
    directory = directory_entry.get()
    verbose = verbose_http.get()
    if directory == "":
        print("Directory not selected")
    elif verbose==False:
        args=[directory, http_port]
        exe=r"http.exe"
        print([exe]+args)
        # os.system(f'start cmd /k "{exe} {directory} {http_port}')
        process=subprocess.Popen([exe, directory, http_port],creationflags=creation_flags)
        processes.append(process)
        print(f"HTTP port {http_port} enabled!")
        instances+=1
        status_string="Current Instances:"+str(instances)+"\n"
        status.config(state=tk.NORMAL)
        status.delete("1.0",tk.END)
        directories.append(str(http_port)+":"+directory)
        status.insert(tk.END, status_string)
        status.insert(tk.END, "\n".join(directories))
        status.config(state=tk.DISABLED)
        if first:
            daemon_section=tk.Label(root, text="Running Daemons:", bg="white")
            daemon_section.grid(row=4, column=0, sticky="w")
            first=False
            daemon_frame=tk.Frame(root, bg="white")
            daemon_frame.grid(row=current_dframe, column=0, columnspan=2, sticky="ew")
            current_dframe+=1
            daemon_frame.grid_columnconfigure(0,weight=1)
            directory_label=tk.Label(daemon_frame, text="Directory", bg="white")
            directory_label.grid(row=0, column=0, sticky="w")
            port_label=tk.Label(daemon_frame, text="Port", bg="white")
            port_label.grid(row=0, column=1)
            
        daemon_frame=tk.Frame(root, bg="white")
        daemon_frame.grid(row=current_dframe, column=0, columnspan=3, sticky="ew")
        current_dframe+=1
        daemon_frame.grid_columnconfigure(0,weight=1)
        directory_label=tk.Label(daemon_frame, text=directory, bg="white")
        directory_label.grid(row=0, column=0, sticky="w")
        port_label=tk.Label(daemon_frame, text=str(http_port), bg="white")
        port_label.grid(row=0, column=1, sticky="ew", padx=25)
        stop_button=ttk.Button(daemon_frame, text="Stop", command=lambda: [process.terminate(), daemon_frame.destroy()])
        stop_button.grid(row=0, column=2,sticky="e")
        # daemon_frames.append(daemon_frame)
    elif verbose==True:
         args=[directory, http_port]
         exe=r"http.exe"
         print([exe]+args)
         os.system(f'start cmd /k "{exe} {directory} {http_port}')
         print(f"HTTP port {http_port} enabled!")
# Function to handle enabling HTTPS port
def enable_https():
    https_port = https_port_entry.get()
    print(f"HTTPS port {https_port} enabled!")
def isAlive():
    global processes, instances, status_string, directories
    for x in processes:
        if x.poll() is None:
            pass
        else:
            instances-=1
            status_string="Current Instances:"+str(instances)+"\n"
            directories.pop(processes.index(x))
            processes.remove(x)
            status.config(state=tk.NORMAL)
            status.delete("1.0",tk.END)
            status.insert(tk.END,status_string)
            status.insert(tk.END,"\n".join(directories))
            status.config(state=tk.DISABLED) 
    root.after(3000,isAlive)
def killRandom():
    global processes 
    processes[0].terminate()
# Create the main window
root = tk.Tk()
root.title("DASH: Configure Web Server")
root.iconbitmap("logo.ico")
root.configure(bg="white")  
image=Image.open("logo_final.png")
image=image.resize((200,150),Image.Resampling.LANCZOS)
# gc.disable()
image=ImageTk.PhotoImage(image)

sub_frame=tk.Frame(root, bg="white")
sub_frame.grid(row=0, column=0, columnspan=3)
image_label=tk.Label(sub_frame, image=image, highlightthickness=0, borderwidth=0)
image_label.grid(row=0, column=0, columnspan=3, sticky="w")
status=tk.Text(sub_frame, wrap="word", height=10, width=30, font=("Helvetica",10))
instances=0
status_string="Current Instances:"+str(instances)
status.insert(tk.END, status_string)
status.config(state=tk.DISABLED)
status.grid(row=0, column=3)
# gc.enable()
# Directory field with selector button
directory_label = tk.Label(root, text="Directory:", bg="white")
directory_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

default_directory=tk.StringVar(value="C:/DASH/www")
directory_entry = ttk.Entry(root, width=40, textvariable=default_directory)
directory_entry.grid(row=1, column=1, padx=0, pady=5, columnspan=1)

directory_button = ttk.Button(root, text="Select", command=select_directory)
directory_button.grid(row=1, column=2, padx=10, pady=5)

# HTTP port field and button
default_http=tk.IntVar(value=80)
http_port_label = tk.Label(root, text="HTTP Port:", bg="white")
http_port_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
sub_frame=tk.Frame(root, bg="white")
sub_frame.grid(row=2,column=1, sticky="w")

http_port_entry = ttk.Entry(sub_frame, width=10, textvariable=default_http)
http_port_entry.grid(row=0, column=0, padx=0, pady=5, sticky="w")
# http_port_entry.configure(width=10)

verbose_http=tk.BooleanVar()
verbose_http_check = ttk.Checkbutton(sub_frame, variable=verbose_http)
verbose_http_check.grid(row=0, column=1, padx=0, pady=0, sticky="w")
verbose_label=tk.Label(sub_frame, text="Verbose")
verbose_label.grid(row=0,column=2)

http_button = ttk.Button(root, text="Start", command=enable_http)
http_button.grid(row=2, column=2, padx=10, pady=5)

# HTTPS port field and button
https_port_label = tk.Label(root, text="HTTPS Port:", bg="white")
https_port_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

https_default=tk.IntVar(value=443)
sub_frame=tk.Frame(root, bg="white")
sub_frame.grid(row=3, column=1, sticky="w")
https_port_entry = ttk.Entry(sub_frame,width=10, textvariable=https_default)
https_port_entry.grid(row=0, column=0, padx=0, pady=5, sticky="w")
# https_port_entry.configure(width=10)

verbose_https=tk.BooleanVar()
verbose_https_check = ttk.Checkbutton(sub_frame, variable=verbose_https)
verbose_https_check.grid(row=0, column=1, padx=0, pady=0, sticky="w")
verbose_label=tk.Label(sub_frame, text="Verbose")
verbose_label.grid(row=0,column=2)    

https_button = ttk.Button(root, text="Start", command=enable_https)
https_button.grid(row=3, column=2, padx=10, pady=5)



root.after(0,isAlive)

root.mainloop()