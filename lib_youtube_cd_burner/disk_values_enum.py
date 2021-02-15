from enum import Enum


class DiskValues(Enum):
    """Used by CD. Represents values with _get_disk_val"""

    NO_DISK = 1
    OPEN = 2
    READING = 3
    DISK_IN_TRAY = 4
