from PIL import ImageFile


class CSGOInventoryCacheFile(ImageFile.ImageFile):
    format = "IIC"
    format_description = "CS:GO Inventory Image Cache"

    def _open(self):
        self.mode = "RGBA"
        self.size = 512, 384
        self.tile = [
            ("raw", (0, 0) + self.size, 0, ("BGRA", 0, 1))
        ]
