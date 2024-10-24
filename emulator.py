import tkinter as tk
import subprocess
import os
import sys

# Settings
VENDOR_NAMES = [
    'Vendor 1', 'Vendor 2', 'Vendor 3', 'Vendor 4',
    'Vendor 5', 'Vendor 6', 
]
DRIVE_LETTER = 'A'
SHAREPOINT_COMPANY_FOLDER = "SharePoint Company Folder"

# Set the script folder as working directory
os.chdir(os.path.dirname(sys.argv[0]))

# GUI settings
root = tk.Tk()
root.title(f"NetShare Emulator Manager")

label = tk.Label(root, text="Select the vendor you want to emulate the path for.")
label.grid(row=0, column=0, columnspan=3, padx=10, pady=15)

output_text = tk.Text(root, height=10, width=50)
output_text.grid(row=1, column=0, columnspan=3, padx=15, pady=20)

def print_to_output(text):
    output_text.insert(tk.END, f"- {text}\n\n")
    output_text.see(tk.END)

def remove_drive():
    subprocess.call(f"net use {DRIVE_LETTER}: /d /y", shell=True)
    print_to_output(f"Removing {DRIVE_LETTER}:\\...")

def open_folder(path):
    subprocess.call(f"explorer {path}", shell=True)

def emulate_folder(sharepoint_dir, emulated_dir, vendor, open_folder_flag):
    remove_drive()
    cmd = f"net use {DRIVE_LETTER}: \"{emulated_dir}\""
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    if process.returncode != 0:
        print_to_output(f"Error while emulating {DRIVE_LETTER}:\\ for {vendor}.")
    else:
        print_to_output(f"{DRIVE_LETTER}:\\ set for {vendor}.")
        if open_folder_flag:
            open_folder(sharepoint_dir)

def check_folder(vendor):
    root_dir = os.path.join(os.path.expanduser('~'), SHAREPOINT_COMPANY_FOLDER)
    subfolders = [f.name for f in os.scandir(root_dir) if f.is_dir()]

    for folder in subfolders:
        if vendor.lower() in folder.lower() and "general" in folder.lower():
            sharepoint_dir = os.path.join(root_dir, folder)
            emulated_dir = sharepoint_dir.replace("C:", "\\\\localhost\\c$")
            return sharepoint_dir, emulated_dir
    return None, None

def create_button(vendor_name):
    sharepoint_dir, emulated_dir = check_folder(vendor_name)
    if sharepoint_dir and emulated_dir:
        return tk.Button(root, text=vendor_name, 
                         command=lambda: emulate_folder(sharepoint_dir, emulated_dir, vendor_name, open_folder_var.get()))
    else:
        # Aggiungi un pulsante di debug o una stampa per vedere cosa succede
        print(f"Cartella non trovata per {vendor_name}.")
        return tk.Button(root, text=f"{vendor_name} (Not found)", state=tk.DISABLED)


# Checkbox to open folder right after connection
open_folder_var = tk.BooleanVar()
open_folder_checkbox = tk.Checkbutton(root, text="Open folder after connection", variable=open_folder_var)
open_folder_checkbox.grid(row=len(VENDOR_NAMES) + 2, column=0, padx=15, pady=10)

# Set vendor buttons
for i, vendor in enumerate(VENDOR_NAMES, start=1):
    button = create_button(vendor)
    if button:
        row, col = (i - 1) // 3 + 2, (i - 1) % 3
        button.grid(row=row, column=col, padx=15, pady=10)

# Button to remove any existing connection on drive A:
remove_button = tk.Button(root, text="Remove Drive Connection", command=remove_drive)
remove_button.grid(row=len(VENDOR_NAMES) + 3, column=0, padx=15, pady=10)

# Set close button
close_button = tk.Button(root, text="Close", command=root.quit)
close_button.grid(row=len(VENDOR_NAMES) + 3, column=2, padx=15, pady=10, sticky="e")

root.mainloop()
