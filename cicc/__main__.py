import ctypes
import ctypes.wintypes
import os
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.ttk as ttk

from cicc.image import convert_cache_to_image


class CSGOInvCacheConverterApplet(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master, padding=10, borderwidth=5)
        self.pack()
        self.orig_loc = tk.StringVar()
        self.orig_loc.set("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Counter-Strike Global Offensive\\csgo\\resource\\flash\\econ\\weapons\\cached")

        docspath_buffer = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(0, 5, 0, 0, docspath_buffer)
        self.save_loc = tk.StringVar()
        self.save_loc.set(docspath_buffer.value)

        self.save_ext = tk.StringVar()
        self.save_ext.set(".png")

        self.progress_text = tk.StringVar()
        self.progress_text.set("0 / 0")

        self.progress_file = tk.StringVar()
        self.progress_file.set("None")

        self.orig_loc_button = ttk.Button(self)
        self.orig_loc_button["text"] = "Choose Location"
        self.orig_loc_button["command"] = self.get_originating_location
        self.orig_loc_button.grid(column=3, row=0, sticky="nsew", padx=5)

        self.save_loc_button = ttk.Button(self)
        self.save_loc_button["text"] = "Choose Location"
        self.save_loc_button["command"] = self.get_save_location
        self.save_loc_button.grid(column=3, row=1, sticky="nsew", padx=5)

        self.conv_button = ttk.Button(self)
        self.conv_button["text"] = "Convert"
        self.conv_button["command"] = self.convert
        self.conv_button.grid(column=3, row=2, sticky="nsew", padx=5)

        self.orig_loc_label = ttk.Label(self)
        self.orig_loc_label["text"] = "Cache Location: "
        self.orig_loc_label.grid(column=0, row=0, sticky="e")

        self.orig_loc_text = ttk.Entry(self)
        self.orig_loc_text["textvariable"] = self.orig_loc
        self.orig_loc_text["width"] = 50
        self.orig_loc_text.grid(column=1, row=0, columnspan=2)

        self.save_loc_label = ttk.Label(self)
        self.save_loc_label["text"] = "Output Location: "
        self.save_loc_label.grid(column=0, row=1, sticky="e")

        self.save_loc_text = ttk.Entry(self)
        self.save_loc_text["textvariable"] = self.save_loc
        self.save_loc_text["width"] = 50
        self.save_loc_text.grid(column=1, row=1, columnspan=2)

        self.save_ext_label = ttk.Label(self)
        self.save_ext_label["text"] = "Extension: "
        self.save_ext_label.grid(column=0, row=2, sticky="e")

        self.save_ext_dropdown = ttk.Combobox(self)
        self.save_ext_dropdown["values"] = [".png", ".jpeg", ".bmp", ".gif"]
        self.save_ext_dropdown["textvariable"] = self.save_ext
        self.save_ext_dropdown.grid(column=1, row=2, sticky="w")

        self.separator = ttk.Separator(self)
        self.separator["orient"] = "horizontal"
        self.separator.grid(pady=15, column=0, row=3, columnspan=4, sticky="nesw")

        self.loading_bar = ttk.Progressbar(self)
        self.loading_bar["mode"] = "determinate"
        self.loading_bar["value"] = 0
        self.loading_bar.grid(column=0, row=4, columnspan=3, sticky="nesw")

        self.progress_ratio_label = ttk.Label(self)
        self.progress_ratio_label["textvariable"] = self.progress_text
        self.progress_ratio_label.grid(column=3, row=4)

        self.converting_label = ttk.Label(self)
        self.converting_label["text"] = "Converting: "
        self.converting_label.grid(column=0, row=5,  sticky="e")

        self.progress_file_label = ttk.Label(self)
        self.progress_file_label["textvariable"] = self.progress_file
        self.progress_file_label.grid(column=1, row=5, columnspan=3, sticky="nesw")

    def get_originating_location(self):
        new_location = filedialog.askdirectory(
            initialdir=self.orig_loc.get(),
            mustexist=True
        )

        if new_location != "":
            new_location = new_location.replace("/", "\\")
            self.orig_loc.set(new_location)

    def get_save_location(self):
        new_location = filedialog.askdirectory(
            initialdir=self.save_loc.get(),
            mustexist=True
        )
        if new_location != "":
            new_location = new_location.replace("/", "\\")
            self.save_loc.set(new_location)

    def convert(self):
        self.loading_bar["maximum"] = len(os.listdir(self.orig_loc.get()))
        self.loading_bar["value"] = 0
        for image in os.listdir(self.orig_loc.get()):
            try:
                convert_cache_to_image(
                    os.path.join(self.orig_loc.get(), image),
                    os.path.join(self.save_loc.get(), image.rstrip(".iic") + self.save_ext.get())
                )
            except Exception as e:
                print("Failed to convert:", e)
            self.loading_bar["value"] += 1
            self.progress_file.set(image.rstrip(".iic") + self.save_ext.get())
            self.progress_text.set(str(self.loading_bar["value"]) + " / " + str(self.loading_bar["maximum"]))
            self.update_idletasks()
        self.progress_file.set("None")


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title("CS:GO Inventory Cache Image Converter")
    root.resizable(0, 0)
    app = CSGOInvCacheConverterApplet(master=root)
    app.mainloop()