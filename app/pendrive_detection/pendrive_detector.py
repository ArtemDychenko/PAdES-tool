import os
from typing import Optional
import psutil


class KeyFinder:

    def find_private_key_path(self) -> Optional[str]:
        for partition in psutil.disk_partitions():
            if partition.fstype.lower() in ["vfat", "exfat", "ntfs", "fat32"]:
                for entry in os.scandir(partition.mountpoint):
                    if entry.name.endswith('.pem') and entry.is_file():
                        return entry.path




# class find_class(object):
#     def __init__(self, class_):
#         self._class = class_
#     def __call__(self, device):
#         # first, let's check the device
#         if device.bDeviceClass == self._class:
#             return True
#         # ok, transverse all devices to find an
#         # interface that matches our class
#         for cfg in device:
#             # find_descriptor: what's it?
#             intf = usb.util.find_descriptor(
#                                         cfg,
#                                         bInterfaceClass=self._class
#                                 )
#             if intf is not None:
#                 return True
#         return False



# if __name__ == "__main__":
#     # pendrives = usb.core.find(find_all=1, custom_match=find_class(8))
#     #
#     # for pendrive in pendrives:
#     #     # print(pendrive)
#     find_usb_device_path()





