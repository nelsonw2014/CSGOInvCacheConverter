from PIL import ImageFile, Image


class CSGOInventoryCacheFile(ImageFile.ImageFile):
    format = "IIC"
    format_description = "CS:GO Inventory Image Cache"

    def _open(self):
        self.mode = "RGBA"
        self.size = 512, 384
        self.tile = [
            ("raw", (0, 0) + self.size, 0, ("BGRA", 0, 1))
        ]


def convert_cache_to_image(original_location, new_location):
    Image.register_open("IIC", CSGOInventoryCacheFile)
    Image.register_extension("IIC", ".iic")

    try:
        with open(original_location, "rb") as original_img:
            img = Image.open(original_img)
            img.save(new_location)
    except Exception as e:
        raise Exception("Originating file does not exist: ", e)