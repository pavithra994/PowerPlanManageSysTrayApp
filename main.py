"""
Name: Power Plan Change System Tray Application
Author :  Pavithra M. Weerapperuma
Developer Email   : pavithra.blog@gmail.com
Date Started : 24 Feb 2021

Description: This application can use to switch between your windows power options

"""
import os
import sys
from functools import partial
from PySide2 import QtWidgets, QtGui
from system import PowerConfig


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    """
    CREATE A SYSTEM TRAY ICON CLASS AND ADD MENU
    """

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.power_plan = PowerConfig()
        self.setToolTip(f'Selected Power Plan: {self.power_plan.active_mode_name}')

        self.menu = QtWidgets.QMenu(parent)

        self.open_app = dict()
        for i, _mode in enumerate(self.power_plan.full_mode_list):
            # print(_mode['name'])
            _m_name = _mode['name']
            _m_id = _mode['id']
            __check = "✓" if _mode["isActive"] else " "
            # self.open_app[_m_id] = menu.addAction(f'{_m_name} {__check}',lambda: activate_power_plan_util(i))
            self.open_app[_m_id] = self.menu.addAction(f'{_m_name} {__check}')
            self.open_app[_m_id].setData(_m_id)
            self.open_app[_m_id].triggered.connect(partial(self.activate_power_plan, self.open_app[_m_id]))

        exit_ = self.menu.addAction("Exit")
        exit_.triggered.connect(lambda: sys.exit())
        # exit_.setIcon(QtGui.QIcon("icon.png"))

        self.menu.addSeparator()
        self.setContextMenu(self.menu)
        self.activated.connect(self.onTrayIconActivated)

    def reload_val(self):
        self.power_plan.reload()
        if len(self.open_app.items()) != len(self.power_plan.full_mode_list):
            pass
        self.setToolTip(f'Selected Power Plan: {self.power_plan.active_mode_name}')
        for _mode in self.power_plan.full_mode_list:
            __check = "✓" if _mode["isActive"] else " "
            if self.open_app.__contains__(_mode["id"]):
                self.open_app[_mode["id"]].setText(f'{_mode["name"]} {__check}')
            else:
                self.open_app[_mode["id"]] = self.menu.addAction(f'{_mode["name"]} {__check}')
                self.open_app[_mode["id"]].setData(_mode["id"])
                self.open_app[_mode["id"]].triggered.connect(
                    partial(self.activate_power_plan, self.open_app[_mode["id"]]))

    def onTrayIconActivated(self, reason):
        """
        This function will trigger function on click or double click
        :param reason:
        :return:
        """
        if reason == self.DoubleClick:
            os.system('powercfg.cpl')

    def activate_power_plan(self, menu_item):
        p_id = menu_item.data()
        os.system(f'powercfg -SETACTIVE {p_id}')
        self.reload_val()


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon("icon.png"), w)
    tray_icon.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
