import os


def get_mode_details(value,flat=True):
    if value.startswith("Power Scheme GUID:"):
        __value = value.split(' ',4)
        if flat:
            return __value[4].strip(" () *"),__value[3]
        return {"name":__value[4].strip(" () *"), "id":__value[3]}
    else:
        raise ValueError("invalid value input")


def activate_power_plan_util(p_id):
    print("clicked..",p_id)
    # os.system(f'powercfg -SETACTIVE {p_id}')


