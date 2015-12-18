from PIL import Image
from cicc.image import CSGOInventoryCacheFile
from os import getenv
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.ttk as ttk


def convert_cache_to_image(original_location: str, new_location: str):
    Image.register_open("IIC", CSGOInventoryCacheFile)
    Image.register_extension("IIC", ".iic")

    try:
        with open(original_location, "rb") as original_img:
            img = Image.open(original_img)
            img.save(new_location)
    except FileNotFoundError as e:
        raise FileNotFoundError("Originating file does not exist: ", e)


class Application(ttk.Frame):
    def __init__(self, master=None, width=400, height=200):
        self.content = ttk.Frame.__init__(self, master, width=width, height=height)
        self.grid(column=0, row=0)
        self.orig_loc = tk.StringVar()
        self.orig_loc.set("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Counter-Strike Global Offensive\\csgo\\resource\\flash\\econ\\weapons\\cached")
        self.save_loc = tk.StringVar()
        self.save_loc.set("C:")

        self.orig_loc_button = ttk.Button(self)
        self.orig_loc_button["text"] = "Choose Inventory Cache Directory"
        self.orig_loc_button["command"] = self.get_originating_location
        self.orig_loc_button.grid(column=2, row=0)

        self.save_loc_button = ttk.Button(self)
        self.save_loc_button["text"] = "Choose Image Save Location"
        self.save_loc_button["command"] = self.get_save_location
        self.save_loc_button.grid(column=2, row=1)

        self.orig_loc_text = ttk.Label(self)
        self.orig_loc_text["textvariable"] = self.orig_loc
        self.orig_loc_text["width"] = 50
        self.orig_loc_text.grid(column=0, row=0, columnspan=2)

        self.save_loc_text = ttk.Label(self)
        self.save_loc_text["textvariable"] = self.save_loc
        self.save_loc_text["width"] = 50
        self.save_loc_text.grid(column=0, row=1, columnspan=2)

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

root = tk.Tk()
app = Application(master=root)
app.mainloop()