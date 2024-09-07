# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\PC\Desktop\ART TUTORIALS\SHORTCUTS & STUFF\session_drawing\ui\display_session.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_session_display(object):
    def setupUi(self, session_display):
        session_display.setObjectName("session_display")
        session_display.resize(754, 725)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(session_display.sizePolicy().hasHeightForWidth())
        session_display.setSizePolicy(sizePolicy)
        session_display.setMinimumSize(QtCore.QSize(650, 1))
        session_display.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        session_display.setFont(font)
        session_display.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        session_display.setWindowTitle("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:\\Users\\PC\\Desktop\\ART TUTORIALS\\SHORTCUTS & STUFF\\session_drawing\\ui\\resources/icons/DARK-32x32.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        session_display.setWindowIcon(icon)
        session_display.setStyleSheet("background: rgb(0,0,0)")
        self.verticalLayout = QtWidgets.QVBoxLayout(session_display)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.image_display = QtWidgets.QLabel(session_display)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image_display.sizePolicy().hasHeightForWidth())
        self.image_display.setSizePolicy(sizePolicy)
        self.image_display.setMinimumSize(QtCore.QSize(1, 1))
        self.image_display.setMouseTracking(False)
        self.image_display.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.image_display.setStyleSheet("background: rgb(0,0,0)")
        self.image_display.setFrameShape(QtWidgets.QFrame.Box)
        self.image_display.setFrameShadow(QtWidgets.QFrame.Plain)
        self.image_display.setText("")
        self.image_display.setScaledContents(False)
        self.image_display.setAlignment(QtCore.Qt.AlignCenter)
        self.image_display.setObjectName("image_display")
        self.verticalLayout.addWidget(self.image_display)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_4.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.session_info = QtWidgets.QLabel(session_display)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.session_info.sizePolicy().hasHeightForWidth())
        self.session_info.setSizePolicy(sizePolicy)
        self.session_info.setMinimumSize(QtCore.QSize(70, 25))
        self.session_info.setMaximumSize(QtCore.QSize(59, 25))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.session_info.setFont(font)
        self.session_info.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.session_info.setAutoFillBackground(False)
        self.session_info.setStyleSheet("color: \"white\"")
        self.session_info.setAlignment(QtCore.Qt.AlignCenter)
        self.session_info.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.session_info.setObjectName("session_info")
        self.horizontalLayout.addWidget(self.session_info)
        self.grid_button = QtWidgets.QPushButton(session_display)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grid_button.sizePolicy().hasHeightForWidth())
        self.grid_button.setSizePolicy(sizePolicy)
        self.grid_button.setMinimumSize(QtCore.QSize(40, 0))
        self.grid_button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.grid_button.setStyleSheet("background: rgb(130, 130, 130);")
        self.grid_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("C:\\Users\\PC\\Desktop\\ART TUTORIALS\\SHORTCUTS & STUFF\\session_drawing\\ui\\resources/icons/grid_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.grid_button.setIcon(icon1)
        self.grid_button.setIconSize(QtCore.QSize(15, 15))
        self.grid_button.setCheckable(True)
        self.grid_button.setObjectName("grid_button")
        self.horizontalLayout.addWidget(self.grid_button)
        self.grayscale_button = QtWidgets.QPushButton(session_display)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grayscale_button.sizePolicy().hasHeightForWidth())
        self.grayscale_button.setSizePolicy(sizePolicy)
        self.grayscale_button.setMinimumSize(QtCore.QSize(40, 0))
        self.grayscale_button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.grayscale_button.setMouseTracking(False)
        self.grayscale_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.grayscale_button.setStyleSheet("background: rgb(130, 130, 130);")
        self.grayscale_button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/grayscale.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.grayscale_button.setIcon(icon2)
        self.grayscale_button.setIconSize(QtCore.QSize(15, 15))
        self.grayscale_button.setCheckable(True)
        self.grayscale_button.setObjectName("grayscale_button")
        self.horizontalLayout.addWidget(self.grayscale_button)
        self.lock_scale_button = QtWidgets.QPushButton(session_display)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lock_scale_button.sizePolicy().hasHeightForWidth())
        self.lock_scale_button.setSizePolicy(sizePolicy)
        self.lock_scale_button.setMinimumSize(QtCore.QSize(40, 0))
        self.lock_scale_button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.lock_scale_button.setStyleSheet("background: rgb(130, 130, 130);")
        self.lock_scale_button.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("C:\\Users\\PC\\Desktop\\ART TUTORIALS\\SHORTCUTS & STUFF\\session_drawing\\ui\\resources/icons/lock_scale.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.lock_scale_button.setIcon(icon3)
        self.lock_scale_button.setIconSize(QtCore.QSize(15, 15))
        self.lock_scale_button.setCheckable(True)
        self.lock_scale_button.setObjectName("lock_scale_button")
        self.horizontalLayout.addWidget(self.lock_scale_button)
        self.flip_horizontal_button = QtWidgets.QPushButton(session_display)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.flip_horizontal_button.sizePolicy().hasHeightForWidth())
        self.flip_horizontal_button.setSizePolicy(sizePolicy)
        self.flip_horizontal_button.setMinimumSize(QtCore.QSize(40, 0))
        self.flip_horizontal_button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.flip_horizontal_button.setMouseTracking(False)
        self.flip_horizontal_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.flip_horizontal_button.setStyleSheet("background: rgb(130, 130, 130);")
        self.flip_horizontal_button.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/icons/flip horizontal.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.flip_horizontal_button.setIcon(icon4)
        self.flip_horizontal_button.setIconSize(QtCore.QSize(15, 15))
        self.flip_horizontal_button.setCheckable(True)
        self.flip_horizontal_button.setObjectName("flip_horizontal_button")
        self.horizontalLayout.addWidget(self.flip_horizontal_button)
        self.flip_vertical_button = QtWidgets.QPushButton(session_display)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.flip_vertical_button.sizePolicy().hasHeightForWidth())
        self.flip_vertical_button.setSizePolicy(sizePolicy)
        self.flip_vertical_button.setMinimumSize(QtCore.QSize(40, 0))
        self.flip_vertical_button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.flip_vertical_button.setMouseTracking(False)
        self.flip_vertical_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.flip_vertical_button.setStyleSheet("background: rgb(130, 130, 130);")
        self.flip_vertical_button.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/icons/flip vertical.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.flip_vertical_button.setIcon(icon5)
        self.flip_vertical_button.setIconSize(QtCore.QSize(15, 15))
        self.flip_vertical_button.setCheckable(True)
        self.flip_vertical_button.setObjectName("flip_vertical_button")
        self.horizontalLayout.addWidget(self.flip_vertical_button)
        self.previous_image = QtWidgets.QPushButton(session_display)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previous_image.sizePolicy().hasHeightForWidth())
        self.previous_image.setSizePolicy(sizePolicy)
        self.previous_image.setMinimumSize(QtCore.QSize(40, 0))
        self.previous_image.setMaximumSize(QtCore.QSize(40, 16777215))
        self.previous_image.setMouseTracking(False)
        self.previous_image.setFocusPolicy(QtCore.Qt.NoFocus)
        self.previous_image.setStyleSheet("background: rgb(130, 130, 130);")
        self.previous_image.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/icons/arrow left.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.previous_image.setIcon(icon6)
        self.previous_image.setIconSize(QtCore.QSize(15, 15))
        self.previous_image.setCheckable(False)
        self.previous_image.setObjectName("previous_image")
        self.horizontalLayout.addWidget(self.previous_image)
        self.pause_timer = QtWidgets.QPushButton(session_display)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pause_timer.sizePolicy().hasHeightForWidth())
        self.pause_timer.setSizePolicy(sizePolicy)
        self.pause_timer.setMinimumSize(QtCore.QSize(40, 0))
        self.pause_timer.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pause_timer.setMouseTracking(False)
        self.pause_timer.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pause_timer.setStyleSheet("background: rgb(130, 130, 130);")
        self.pause_timer.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/icons/Pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pause_timer.setIcon(icon7)
        self.pause_timer.setIconSize(QtCore.QSize(15, 15))
        self.pause_timer.setCheckable(True)
        self.pause_timer.setObjectName("pause_timer")
        self.horizontalLayout.addWidget(self.pause_timer)
        self.stop_session = QtWidgets.QPushButton(session_display)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stop_session.sizePolicy().hasHeightForWidth())
        self.stop_session.setSizePolicy(sizePolicy)
        self.stop_session.setMinimumSize(QtCore.QSize(40, 0))
        self.stop_session.setMaximumSize(QtCore.QSize(40, 16777215))
        self.stop_session.setMouseTracking(False)
        self.stop_session.setFocusPolicy(QtCore.Qt.NoFocus)
        self.stop_session.setStyleSheet("background: rgb(130, 130, 130);")
        self.stop_session.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/icons/Square.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stop_session.setIcon(icon8)
        self.stop_session.setIconSize(QtCore.QSize(15, 15))
        self.stop_session.setCheckable(False)
        self.stop_session.setObjectName("stop_session")
        self.horizontalLayout.addWidget(self.stop_session)
        self.next_image = QtWidgets.QPushButton(session_display)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.next_image.sizePolicy().hasHeightForWidth())
        self.next_image.setSizePolicy(sizePolicy)
        self.next_image.setMinimumSize(QtCore.QSize(40, 0))
        self.next_image.setMaximumSize(QtCore.QSize(40, 16777215))
        self.next_image.setMouseTracking(False)
        self.next_image.setFocusPolicy(QtCore.Qt.NoFocus)
        self.next_image.setStyleSheet("background: rgb(130, 130, 130);")
        self.next_image.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/icons/arrow right.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.next_image.setIcon(icon9)
        self.next_image.setIconSize(QtCore.QSize(15, 15))
        self.next_image.setCheckable(False)
        self.next_image.setObjectName("next_image")
        self.horizontalLayout.addWidget(self.next_image)
        self.copy_image_path_button = QtWidgets.QPushButton(session_display)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.copy_image_path_button.sizePolicy().hasHeightForWidth())
        self.copy_image_path_button.setSizePolicy(sizePolicy)
        self.copy_image_path_button.setMinimumSize(QtCore.QSize(40, 0))
        self.copy_image_path_button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.copy_image_path_button.setStyleSheet("background: rgb(130, 130, 130);")
        self.copy_image_path_button.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("C:\\Users\\PC\\Desktop\\ART TUTORIALS\\SHORTCUTS & STUFF\\session_drawing\\ui\\resources/icons/copy-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.copy_image_path_button.setIcon(icon10)
        self.copy_image_path_button.setIconSize(QtCore.QSize(15, 15))
        self.copy_image_path_button.setCheckable(False)
        self.copy_image_path_button.setObjectName("copy_image_path_button")
        self.horizontalLayout.addWidget(self.copy_image_path_button)
        self.open_folder_button = QtWidgets.QPushButton(session_display)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.open_folder_button.sizePolicy().hasHeightForWidth())
        self.open_folder_button.setSizePolicy(sizePolicy)
        self.open_folder_button.setMinimumSize(QtCore.QSize(40, 0))
        self.open_folder_button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.open_folder_button.setStyleSheet("background: rgb(130, 130, 130);")
        self.open_folder_button.setText("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("C:\\Users\\PC\\Desktop\\ART TUTORIALS\\SHORTCUTS & STUFF\\session_drawing\\ui\\resources/icons/folder-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.open_folder_button.setIcon(icon11)
        self.open_folder_button.setIconSize(QtCore.QSize(15, 15))
        self.open_folder_button.setCheckable(False)
        self.open_folder_button.setObjectName("open_folder_button")
        self.horizontalLayout.addWidget(self.open_folder_button)
        self.delete_image_button = QtWidgets.QPushButton(session_display)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delete_image_button.sizePolicy().hasHeightForWidth())
        self.delete_image_button.setSizePolicy(sizePolicy)
        self.delete_image_button.setMinimumSize(QtCore.QSize(40, 0))
        self.delete_image_button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.delete_image_button.setStyleSheet("background: rgb(130, 130, 130);")
        self.delete_image_button.setText("")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("C:\\Users\\PC\\Desktop\\ART TUTORIALS\\SHORTCUTS & STUFF\\session_drawing\\ui\\resources/icons/trash-can.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_image_button.setIcon(icon12)
        self.delete_image_button.setIconSize(QtCore.QSize(15, 15))
        self.delete_image_button.setCheckable(False)
        self.delete_image_button.setObjectName("delete_image_button")
        self.horizontalLayout.addWidget(self.delete_image_button)
        self.show_main_window_button = QtWidgets.QPushButton(session_display)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.show_main_window_button.sizePolicy().hasHeightForWidth())
        self.show_main_window_button.setSizePolicy(sizePolicy)
        self.show_main_window_button.setMinimumSize(QtCore.QSize(40, 0))
        self.show_main_window_button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.show_main_window_button.setStyleSheet("background: rgb(130, 130, 130);")
        self.show_main_window_button.setText("")
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("C:\\Users\\PC\\Desktop\\ART TUTORIALS\\SHORTCUTS & STUFF\\session_drawing\\ui\\resources/icons/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.show_main_window_button.setIcon(icon13)
        self.show_main_window_button.setIconSize(QtCore.QSize(15, 15))
        self.show_main_window_button.setObjectName("show_main_window_button")
        self.horizontalLayout.addWidget(self.show_main_window_button)
        self.timer_display = QtWidgets.QLabel(session_display)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timer_display.sizePolicy().hasHeightForWidth())
        self.timer_display.setSizePolicy(sizePolicy)
        self.timer_display.setMinimumSize(QtCore.QSize(70, 25))
        self.timer_display.setMaximumSize(QtCore.QSize(50, 25))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.timer_display.setFont(font)
        self.timer_display.setStyleSheet("color: \'white\';")
        self.timer_display.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.timer_display.setFrameShadow(QtWidgets.QFrame.Plain)
        self.timer_display.setLineWidth(1)
        self.timer_display.setAlignment(QtCore.Qt.AlignCenter)
        self.timer_display.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.timer_display.setObjectName("timer_display")
        self.horizontalLayout.addWidget(self.timer_display)
        self.horizontalLayout_4.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(session_display)
        QtCore.QMetaObject.connectSlotsByName(session_display)

    def retranslateUi(self, session_display):
        _translate = QtCore.QCoreApplication.translate
        self.session_info.setText(_translate("session_display", "{info}"))
        self.grid_button.setToolTip(_translate("session_display", "[G] Toggle grid, [CTRL + G] Grid settings"))
        self.grayscale_button.setToolTip(_translate("session_display", "[T] Toggle grayscale"))
        self.lock_scale_button.setToolTip(_translate("session_display", "[R] Prevent rescaling of the window\""))
        self.flip_horizontal_button.setToolTip(_translate("session_display", "[H] Horizontal Flip"))
        self.flip_vertical_button.setToolTip(_translate("session_display", "[V] Vertical Flip"))
        self.previous_image.setToolTip(_translate("session_display", "[Left] Previous image"))
        self.previous_image.setShortcut(_translate("session_display", "Left"))
        self.pause_timer.setToolTip(_translate("session_display", "[Space] Pause Timer"))
        self.pause_timer.setShortcut(_translate("session_display", "Space"))
        self.stop_session.setToolTip(_translate("session_display", "[Esc] Stop Session and closes window"))
        self.stop_session.setShortcut(_translate("session_display", "Esc"))
        self.next_image.setToolTip(_translate("session_display", "[Right] Next Image"))
        self.next_image.setShortcut(_translate("session_display", "Right"))
        self.copy_image_path_button.setToolTip(_translate("session_display", "[C] Copy image path to clipboard"))
        self.open_folder_button.setToolTip(_translate("session_display", "[O] Open image folder"))
        self.delete_image_button.setToolTip(_translate("session_display", "[Ctrl + D] Delete image"))
        self.show_main_window_button.setToolTip(_translate("session_display", "[Tab] Open settings window"))
        self.timer_display.setText(_translate("session_display", "00:00"))
import resources_config_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    session_display = QtWidgets.QWidget()
    ui = Ui_session_display()
    ui.setupUi(session_display)
    session_display.show()
    sys.exit(app.exec_())
