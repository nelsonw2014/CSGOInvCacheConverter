from PIL import Image
from cicc.image import CSGOInventoryCacheFile
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.ttk as ttk
import ctypes
import ctypes.wintypes
import os

def convert_cache_to_image(original_location: str, new_location: str):
    Image.register_open("IIC", CSGOInventoryCacheFile)
    Image.register_extension("IIC", ".iic")

    try:
        with open(original_location, "rb") as original_img:
            img = Image.open(original_img)
            img.save(new_location)
    except FileNotFoundError as e:
        raise FileNotFoundError("Originating file does not exist: ", e)


class CSGOInvCacheConverterApplet(ttk.LabelFrame):
    def __init__(self, master=None):
        ttk.LabelFrame.__init__(self, master, padding=10, text="CS:GO Inventory Cache Image Converter")
        self.pack()
        self.orig_loc = tk.StringVar()
        self.orig_loc.set("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Counter-Strike Global Offensive\\csgo\\resource\\flash\\econ\\weapons\\cached")

        docspath_buffer = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(0, 5, 0, 0, docspath_buffer)
        self.save_loc = tk.StringVar()
        self.save_loc.set(docspath_buffer.value)

        self.save_ext = tk.StringVar()
        self.save_ext.set(".png")

        self.orig_loc_button = ttk.Button(self)
        self.orig_loc_button["text"] = "Choose Location"
        self.orig_loc_button["command"] = self.get_originating_location
        self.orig_loc_button.grid(column=3, row=0, sticky="w", padx=5)

        self.save_loc_button = ttk.Button(self)
        self.save_loc_button["text"] = "Choose Location"
        self.save_loc_button["command"] = self.get_save_location
        self.save_loc_button.grid(column=3, row=1, sticky="w", padx=5)

        self.conv_button = ttk.Button(self)
        self.conv_button["text"] = "Convert"
        self.conv_button["command"] = self.convert
        self.conv_button.grid(column=3, row=3, sticky="w", padx=5)

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

        self.loading_bar = ttk.Progressbar(self)
        self.loading_bar["mode"] = "determinate"
        self.loading_bar["value"] = 0
        self.loading_bar.grid(pady=10, column=0, row=4, columnspan=4, sticky="nesw")

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
            self.update_idletasks()
            self.loading_bar["value"] += 1
            convert_cache_to_image(
                os.path.join(self.orig_loc.get(), image),
                os.path.join(self.save_loc.get(), image.rstrip(".iic") + self.save_ext.get())
            )


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title("CS:GO Inv Cache Converter")
    root.resizable(0, 0)
    app = CSGOInvCacheConverterApplet(master=root)
    app.mainloop()