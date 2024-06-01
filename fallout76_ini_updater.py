import os
import tkinter as tk
from tkinter import filedialog, messagebox

def update_ini_file(ini_file_path, data_folder_path):
    try:
        with open(ini_file_path, 'r') as file:
            lines = file.readlines()

        archive_section_found = False
        sresourcearchive2list_found = False
        new_lines = []
        for line in lines:
            new_lines.append(line)
            if line.strip() == '[Archive]':
                archive_section_found = True

        ba2_files = sorted(f for f in os.listdir(data_folder_path) if f.endswith('.ba2') and not f.startswith('SeventySix'))
        sresourcearchive2list = f'sResourceArchive2List = {", ".join(ba2_files)}\n'

        if archive_section_found:
            for i, line in enumerate(new_lines):
                if line.strip().startswith('sResourceArchive2List ='):
                    new_lines[i] = sresourcearchive2list
                    sresourcearchive2list_found = True
                    break

            if not sresourcearchive2list_found:
                for i, line in enumerate(new_lines):
                    if line.strip() == '[Archive]':
                        new_lines.insert(i + 1, sresourcearchive2list)
                        break

        with open(ini_file_path, 'w') as file:
            file.writelines(new_lines)
        
        messagebox.showinfo("Success", "The INI file was updated successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def browse_ini_file():
    ini_file_path = filedialog.askopenfilename(
        title="Select the Fallout76Custom.ini file",
        filetypes=[("INI files", "*.ini"), ("All files", "*.*")]
    )
    if ini_file_path:
        ini_path_entry.delete(0, tk.END)
        ini_path_entry.insert(0, ini_file_path)
        adjust_entry_widths()

def browse_data_folder():
    data_folder_path = filedialog.askdirectory(
        title="Select the Data folder"
    )
    if data_folder_path:
        data_path_entry.delete(0, tk.END)
        data_path_entry.insert(0, data_folder_path)
        adjust_entry_widths()

def process_files():
    ini_file_path = ini_path_entry.get()
    data_folder_path = data_path_entry.get()
    if not os.path.exists(ini_file_path):
        messagebox.showerror("Error", "The specified INI file does not exist.")
        return
    if not os.path.exists(data_folder_path):
        messagebox.showerror("Error", "The specified Data folder does not exist.")
        return
    update_ini_file(ini_file_path, data_folder_path)

def adjust_entry_widths():
    ini_text_length = len(ini_path_entry.get())
    data_text_length = len(data_path_entry.get())
    max_length = max(ini_text_length, data_text_length) + 5
    ini_path_entry.config(width=max_length)
    data_path_entry.config(width=max_length)

root = tk.Tk()
root.title("Fallout 76 INI Updater")

info_label = tk.Label(root, text="Update Fallout76Custom.ini with .ba2 files from Data folder.")
info_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

ini_path_label = tk.Label(root, text="INI File Path:")
ini_path_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)

ini_path_entry = tk.Entry(root)
ini_path_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

ini_browse_button = tk.Button(root, text="Browse...", command=browse_ini_file)
ini_browse_button.grid(row=1, column=2, padx=10, pady=5)

data_path_label = tk.Label(root, text="Data Folder Path:")
data_path_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)

data_path_entry = tk.Entry(root)
data_path_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

data_browse_button = tk.Button(root, text="Browse...", command=browse_data_folder)
data_browse_button.grid(row=2, column=2, padx=10, pady=5)

process_button = tk.Button(root, text="Update INI", command=process_files)
process_button.grid(row=3, column=0, columnspan=3, padx=10, pady=20)

user_name = os.getlogin()
default_ini_path = os.path.join('C:\\Users', user_name, 'Documents', 'My Games', 'Fallout 76', 'Fallout76Custom.ini')
default_data_path = r'C:\Program Files (x86)\Steam\steamapps\common\Fallout76\Data'

ini_path_entry.insert(0, default_ini_path)
data_path_entry.insert(0, default_data_path)
adjust_entry_widths()

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

root.mainloop()
