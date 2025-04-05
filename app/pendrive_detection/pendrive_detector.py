import os
from typing import Optional
import psutil


class PenDriveFinder:
    """
    A utility class to detect pen drives and locate private key files (*.pem) stored on them.
    """

    def find_pendrive_with_private_key(self) -> Optional[str]:
        """
        Scans all connected and mounted drives to detect a pen drive containing a private key (*.pem) file.
        :return:
            str - Mount point of the partition containing the `.pem` private key file, or
            None - If no partition with a `.pem` file is found.
        """
        for partition in psutil.disk_partitions():
            if partition.fstype.lower() in ["hfs", "apfs", "vfat", "exfat", "ntfs", "fat32"]:
                for entry in os.scandir(partition.mountpoint):
                    if entry.name.endswith(".pem") and entry.is_file():
                        return partition.mountpoint


    def get_private_key_path(self, pendrive_path: str) -> Optional[str]:
        """
        Searches the specified pen drive (mount point) for a private key (*.pem) file.
        :param pen drive_path: str - The mount point of the pen drive to scan.
        :return:
            str - Full path to the `.pem` private key file if found, or
            None - If no `.pem` file is found on the provided pen drive path.
        """
        for entry in os.scandir(pendrive_path):
            if entry.name.endswith(".pem") and entry.is_file():
                return entry.path