import os

from utils import get_mode_details


class PowerConfig:
    def __init__(self):
        self.reload()

    @property
    def full_mode_list(self):
        __all = os.popen('powercfg -LIST').read()
        all_modes_list = []
        __count = 0
        for line in __all.splitlines():
            try:
                x_name, x_id = get_mode_details(line)
                all_modes_list.append({
                    "name":x_name,
                    "id":x_id,
                    "isActive":x_id==self.active_mode_id
                })
            except ValueError:
                pass

        return all_modes_list

    def reload(self):
        self.active_mode_name, self.active_mode_id = get_mode_details(os.popen('powercfg -GETACTIVESCHEME').read())

