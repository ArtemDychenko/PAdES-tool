import os
import sys
from typing import Optional
import psutil

if sys.platform == "linux":
    import pyudev

if sys.platform == "win32":
    import wmi


class PenDriveFinder:
    """
    A utility class to detect pen drives and locate private key files (*.pem) stored
    on them on various operating systems(Windows, Linux, macOS).
    """
    def __init__(self):
        self.wmi_client = None


    @staticmethod
    def check_os() -> str:
        """
        Determines the current operating system (Linux, Windows, macOS)
        :return:
            str - A str of detected operating system, e.g. "linux", "win32", "darwin"
        """
        return sys.platform

    def find_all_pen_drives(self) -> Optional[list]:
        """
        Detects and lists all connected pen drives across different operating systems (Linux, Windows, macOS).
        It determines the current operating system and delegates the task to an OS-specific function.
        :return:
            list - A list of detected pen drive mount points (partitions or whole drives).
            None - if no pen drives are detected.
        """
        if self.check_os() == "linux":
            return self.find_all_pen_drives_linux()
        elif self.check_os() == "win32":
            return self.find_all_pen_drives_win()
        elif self.check_os() == "darwin":
            pass #TODO implement macos function

    def find_all_pen_drives_linux(self) -> Optional[list]:
        """
        Scans all connected and mounted drives to detect all pen drives on Linux systems.

        :return:
            list - A list of detected pen drive mount points (partitions or whole drives).
            None - if no pen drives are detected.
        """
        context = pyudev.Context()
        pen_drives = []

        partition_mounts = {p.device: p.mountpoint for p in psutil.disk_partitions()}

        for device in context.list_devices(subsystem="block", DEVTYPE="disk"):
            if device.attributes.asstring("removable") == "1":
                mount_point = partition_mounts.get(device.device_node)
                if mount_point:
                    pen_drives.append(mount_point)
                else:
                    for part in context.list_devices(subsystem="block", DEVTYPE="partition", parent=device):
                        mount_point = partition_mounts.get(part.device_node)
                        if mount_point:
                            pen_drives.append(mount_point)

        return pen_drives if pen_drives else None


    def find_all_pen_drives_win(self) -> Optional[list]:
        """
        Scans all connected and mounted drives to detect all pen drives on Windows systems.

        :return:
            list - A list of detected pen drive mount points (partitions or whole drives).
            None - if no pen drives are detected.
        """
        if self.wmi_client is None:
            self.wmi_client = wmi.WMI()

        pen_drives = []

        for drive in self.wmi_client.Win32_DiskDrive():
            if drive.InterfaceType == "USB":
                for partition in drive.associators("Win32_DiskDriveToDiskPartition"):
                    for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                        pen_drives.append(logical_disk.DeviceID)

        return pen_drives if pen_drives else None

    def find_pen_drive_with_private_key(self, pen_drives: list) -> Optional[str]:
        """
        Scans all connected and mounted drives to detect a pen drive containing a private key (*.pem) file.
        :param:
            pen_drives: list - A list of detected pen drive mount points (partitions or whole drives).
        :return:
            str - Mount point of the partition containing the `.pem` private key file, or
            None - If no partition with a `.pem` file is found.
        """
        for pen_drive in pen_drives:
            for entry in os.scandir(pen_drive):
                if entry.name.endswith(".pem") and entry.is_file():
                    return pen_drive
        return None


    def get_private_key_path(self, pen_drive_path: str) -> Optional[str]:
        """
        Searches the specified pen drive (mount point) for a private key (*.pem) file.
        :param pen_drive_path: str - The mount point of the pen drive to scan.
        :return:
            str - Full path to the `.pem` private key file if found, or
            None - If no `.pem` file is found on the provided pen drive path.
        """
        for entry in os.scandir(pen_drive_path):
            if entry.name.endswith(".pem") and entry.is_file():
                return entry.path


