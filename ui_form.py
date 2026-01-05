# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QDial, QFrame,
    QHBoxLayout, QLabel, QMainWindow, QPlainTextEdit,
    QPushButton, QSizePolicy, QSpinBox, QStatusBar,
    QVBoxLayout, QWidget)

from pyqtgraph import PlotWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(872, 689)
        MainWindow.setMinimumSize(QSize(300, 200))
        MainWindow.setAcceptDrops(True)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setStyleSheet(u"QPushButton {background-color: rgb(78, 143, 173)}\n"
"QFrame {background-color: rgb(27, 27, 27)}\n"
"line {background-color: rgb(35, 35, 35)}\n"
"QSpinBox{background-color: rgb(35, 35, 35)}\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.inputFrame = QFrame(self.centralwidget)
        self.inputFrame.setObjectName(u"inputFrame")
        self.inputFrame.setGeometry(QRect(10, 10, 301, 271))
        self.inputFrame.setAutoFillBackground(False)
        self.inputFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.inputFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.inputFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_3 = QLabel(self.inputFrame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16777215, 20))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label_3.setFont(font)

        self.verticalLayout.addWidget(self.label_3, 0, Qt.AlignmentFlag.AlignHCenter)

        self.fileInputFrame = QFrame(self.inputFrame)
        self.fileInputFrame.setObjectName(u"fileInputFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileInputFrame.sizePolicy().hasHeightForWidth())
        self.fileInputFrame.setSizePolicy(sizePolicy)
        self.fileInputFrame.setMinimumSize(QSize(191, 51))
        self.fileInputFrame.setMaximumSize(QSize(500, 40))
        self.fileInputFrame.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.fileInputFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.fileInputFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.fileInputFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.inputFileDisplay = QPlainTextEdit(self.fileInputFrame)
        self.inputFileDisplay.setObjectName(u"inputFileDisplay")
        self.inputFileDisplay.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.inputFileDisplay.sizePolicy().hasHeightForWidth())
        self.inputFileDisplay.setSizePolicy(sizePolicy1)
        self.inputFileDisplay.setMinimumSize(QSize(92, 31))
        self.inputFileDisplay.setMaximumSize(QSize(16777215, 31))
        self.inputFileDisplay.setStyleSheet(u"background-color: rgb(35, 35, 35);")
        self.inputFileDisplay.setReadOnly(True)
        self.inputFileDisplay.setCenterOnScroll(False)

        self.horizontalLayout.addWidget(self.inputFileDisplay)

        self.inputFileButton = QPushButton(self.fileInputFrame)
        self.inputFileButton.setObjectName(u"inputFileButton")
        self.inputFileButton.setMinimumSize(QSize(73, 24))
        self.inputFileButton.setMaximumSize(QSize(89, 24))

        self.horizontalLayout.addWidget(self.inputFileButton)


        self.verticalLayout.addWidget(self.fileInputFrame, 0, Qt.AlignmentFlag.AlignHCenter)

        self.InputPeekWidget = PlotWidget(self.inputFrame)
        self.InputPeekWidget.setObjectName(u"InputPeekWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.InputPeekWidget.sizePolicy().hasHeightForWidth())
        self.InputPeekWidget.setSizePolicy(sizePolicy2)
        self.InputPeekWidget.setMaximumSize(QSize(99999, 117))

        self.verticalLayout.addWidget(self.InputPeekWidget, 0, Qt.AlignmentFlag.AlignHCenter)

        self.inputPlaybackFrame = QFrame(self.inputFrame)
        self.inputPlaybackFrame.setObjectName(u"inputPlaybackFrame")
        self.inputPlaybackFrame.setMaximumSize(QSize(16777215, 40))
        self.inputPlaybackFrame.setAutoFillBackground(False)
        self.inputPlaybackFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.inputPlaybackFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.inputPlaybackFrame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButton_5 = QPushButton(self.inputPlaybackFrame)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setEnabled(True)
        self.pushButton_5.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaSkipBackward))
        self.pushButton_5.setIcon(icon)
        self.pushButton_5.setAutoRepeatDelay(300)

        self.horizontalLayout_4.addWidget(self.pushButton_5)

        self.pushButton_6 = QPushButton(self.inputPlaybackFrame)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setEnabled(True)
        self.pushButton_6.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStart))
        self.pushButton_6.setIcon(icon1)
        self.pushButton_6.setAutoRepeatDelay(300)

        self.horizontalLayout_4.addWidget(self.pushButton_6)

        self.pushButton_7 = QPushButton(self.inputPlaybackFrame)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setEnabled(True)
        self.pushButton_7.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackPause))
        self.pushButton_7.setIcon(icon2)
        self.pushButton_7.setAutoRepeatDelay(300)

        self.horizontalLayout_4.addWidget(self.pushButton_7)


        self.verticalLayout.addWidget(self.inputPlaybackFrame)

        self.IRFrame = QFrame(self.centralwidget)
        self.IRFrame.setObjectName(u"IRFrame")
        self.IRFrame.setGeometry(QRect(10, 310, 301, 291))
        self.IRFrame.setAutoFillBackground(False)
        self.IRFrame.setStyleSheet(u"")
        self.IRFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.IRFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.IRFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_5 = QLabel(self.IRFrame)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(16777215, 20))
        self.label_5.setFont(font)

        self.verticalLayout_2.addWidget(self.label_5, 0, Qt.AlignmentFlag.AlignHCenter)

        self.fileInputFrame_2 = QFrame(self.IRFrame)
        self.fileInputFrame_2.setObjectName(u"fileInputFrame_2")
        sizePolicy.setHeightForWidth(self.fileInputFrame_2.sizePolicy().hasHeightForWidth())
        self.fileInputFrame_2.setSizePolicy(sizePolicy)
        self.fileInputFrame_2.setMinimumSize(QSize(191, 51))
        self.fileInputFrame_2.setMaximumSize(QSize(500, 40))
        self.fileInputFrame_2.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.fileInputFrame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.fileInputFrame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.fileInputFrame_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.IRFileDisplay = QPlainTextEdit(self.fileInputFrame_2)
        self.IRFileDisplay.setObjectName(u"IRFileDisplay")
        self.IRFileDisplay.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.IRFileDisplay.sizePolicy().hasHeightForWidth())
        self.IRFileDisplay.setSizePolicy(sizePolicy1)
        self.IRFileDisplay.setMinimumSize(QSize(92, 31))
        self.IRFileDisplay.setMaximumSize(QSize(16777215, 31))
        self.IRFileDisplay.setStyleSheet(u"background-color: rgb(35, 35, 35);")
        self.IRFileDisplay.setReadOnly(True)
        self.IRFileDisplay.setCenterOnScroll(False)

        self.horizontalLayout_2.addWidget(self.IRFileDisplay)

        self.IRFileButton = QPushButton(self.fileInputFrame_2)
        self.IRFileButton.setObjectName(u"IRFileButton")
        self.IRFileButton.setMinimumSize(QSize(73, 24))
        self.IRFileButton.setMaximumSize(QSize(89, 24))
        self.IRFileButton.setToolTipDuration(-1)

        self.horizontalLayout_2.addWidget(self.IRFileButton)


        self.verticalLayout_2.addWidget(self.fileInputFrame_2, 0, Qt.AlignmentFlag.AlignHCenter)

        self.IRPeekWidget = PlotWidget(self.IRFrame)
        self.IRPeekWidget.setObjectName(u"IRPeekWidget")
        self.IRPeekWidget.setMaximumSize(QSize(16777215, 117))

        self.verticalLayout_2.addWidget(self.IRPeekWidget, 0, Qt.AlignmentFlag.AlignHCenter)

        self.IRPlaybackFrame = QFrame(self.IRFrame)
        self.IRPlaybackFrame.setObjectName(u"IRPlaybackFrame")
        self.IRPlaybackFrame.setMaximumSize(QSize(16777215, 40))
        self.IRPlaybackFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.IRPlaybackFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.IRPlaybackFrame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_4 = QPushButton(self.IRPlaybackFrame)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setEnabled(True)
        self.pushButton_4.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.pushButton_4.setIcon(icon)
        self.pushButton_4.setAutoRepeatDelay(300)

        self.horizontalLayout_3.addWidget(self.pushButton_4)

        self.pushButton_2 = QPushButton(self.IRPlaybackFrame)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setEnabled(True)
        self.pushButton_2.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setAutoRepeatDelay(300)

        self.horizontalLayout_3.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.IRPlaybackFrame)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setEnabled(True)
        self.pushButton_3.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.pushButton_3.setIcon(icon2)
        self.pushButton_3.setAutoRepeatDelay(300)

        self.horizontalLayout_3.addWidget(self.pushButton_3)


        self.verticalLayout_2.addWidget(self.IRPlaybackFrame)

        self.outputFrame = QFrame(self.centralwidget)
        self.outputFrame.setObjectName(u"outputFrame")
        self.outputFrame.setGeometry(QRect(330, 10, 531, 381))
        self.outputFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.outputFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.outputFrame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_7 = QLabel(self.outputFrame)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_7)

        self.graphicsView = PlotWidget(self.outputFrame)
        self.graphicsView.setObjectName(u"graphicsView")

        self.verticalLayout_3.addWidget(self.graphicsView)

        self.outputPlaybackFrame = QFrame(self.outputFrame)
        self.outputPlaybackFrame.setObjectName(u"outputPlaybackFrame")
        self.outputPlaybackFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.outputPlaybackFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.outputPlaybackFrame)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButton_8 = QPushButton(self.outputPlaybackFrame)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setEnabled(True)
        self.pushButton_8.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.pushButton_8.setIcon(icon)
        self.pushButton_8.setAutoRepeatDelay(300)

        self.horizontalLayout_5.addWidget(self.pushButton_8)

        self.pushButton_9 = QPushButton(self.outputPlaybackFrame)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setEnabled(True)
        self.pushButton_9.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.pushButton_9.setIcon(icon1)
        self.pushButton_9.setAutoRepeatDelay(300)

        self.horizontalLayout_5.addWidget(self.pushButton_9)

        self.pushButton_10 = QPushButton(self.outputPlaybackFrame)
        self.pushButton_10.setObjectName(u"pushButton_10")
        self.pushButton_10.setEnabled(True)
        self.pushButton_10.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.pushButton_10.setIcon(icon2)
        self.pushButton_10.setAutoRepeatDelay(300)

        self.horizontalLayout_5.addWidget(self.pushButton_10)


        self.verticalLayout_3.addWidget(self.outputPlaybackFrame)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(720, 590, 121, 51))
        self.pushButton_11 = QPushButton(self.centralwidget)
        self.pushButton_11.setObjectName(u"pushButton_11")
        self.pushButton_11.setGeometry(QRect(720, 530, 121, 51))
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(330, 420, 361, 221))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.inputGainFrame = QFrame(self.frame)
        self.inputGainFrame.setObjectName(u"inputGainFrame")
        self.inputGainFrame.setEnabled(True)
        sizePolicy.setHeightForWidth(self.inputGainFrame.sizePolicy().hasHeightForWidth())
        self.inputGainFrame.setSizePolicy(sizePolicy)
        self.inputGainFrame.setMinimumSize(QSize(0, 101))
        self.inputGainFrame.setMaximumSize(QSize(500, 200))
        font1 = QFont()
        font1.setPointSize(9)
        self.inputGainFrame.setFont(font1)
        self.inputGainFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.inputGainFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.inputGainFrame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.inputGainLabel = QLabel(self.inputGainFrame)
        self.inputGainLabel.setObjectName(u"inputGainLabel")
        font2 = QFont()
        font2.setPointSize(11)
        self.inputGainLabel.setFont(font2)
        self.inputGainLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.inputGainLabel)

        self.inputDial = QDial(self.inputGainFrame)
        self.inputDial.setObjectName(u"inputDial")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.inputDial.sizePolicy().hasHeightForWidth())
        self.inputDial.setSizePolicy(sizePolicy3)
        self.inputDial.setMinimumSize(QSize(80, 65))
        self.inputDial.setMaximumSize(QSize(92, 16777215))
        self.inputDial.setMinimum(-10)
        self.inputDial.setMaximum(10)
        self.inputDial.setValue(0)
        self.inputDial.setSliderPosition(0)
        self.inputDial.setTracking(False)
        self.inputDial.setWrapping(False)
        self.inputDial.setNotchesVisible(True)

        self.verticalLayout_4.addWidget(self.inputDial)

        self.inputSpinBox = QSpinBox(self.inputGainFrame)
        self.inputSpinBox.setObjectName(u"inputSpinBox")
        self.inputSpinBox.setMinimumSize(QSize(71, 31))
        self.inputSpinBox.setMaximumSize(QSize(71, 16777215))
        self.inputSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.inputSpinBox.setCorrectionMode(QAbstractSpinBox.CorrectionMode.CorrectToNearestValue)
        self.inputSpinBox.setProperty(u"showGroupSeparator", False)
        self.inputSpinBox.setMinimum(-10)
        self.inputSpinBox.setMaximum(10)

        self.verticalLayout_4.addWidget(self.inputSpinBox, 0, Qt.AlignmentFlag.AlignHCenter)


        self.horizontalLayout_6.addWidget(self.inputGainFrame)

        self.inputGainFrame_2 = QFrame(self.frame)
        self.inputGainFrame_2.setObjectName(u"inputGainFrame_2")
        self.inputGainFrame_2.setEnabled(True)
        sizePolicy.setHeightForWidth(self.inputGainFrame_2.sizePolicy().hasHeightForWidth())
        self.inputGainFrame_2.setSizePolicy(sizePolicy)
        self.inputGainFrame_2.setMinimumSize(QSize(0, 101))
        self.inputGainFrame_2.setMaximumSize(QSize(500, 200))
        self.inputGainFrame_2.setFont(font1)
        self.inputGainFrame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.inputGainFrame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.inputGainFrame_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.inputGainLabel_2 = QLabel(self.inputGainFrame_2)
        self.inputGainLabel_2.setObjectName(u"inputGainLabel_2")
        self.inputGainLabel_2.setFont(font2)
        self.inputGainLabel_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.inputGainLabel_2)

        self.inputDial_2 = QDial(self.inputGainFrame_2)
        self.inputDial_2.setObjectName(u"inputDial_2")
        sizePolicy3.setHeightForWidth(self.inputDial_2.sizePolicy().hasHeightForWidth())
        self.inputDial_2.setSizePolicy(sizePolicy3)
        self.inputDial_2.setMinimumSize(QSize(80, 95))
        self.inputDial_2.setMaximumSize(QSize(92, 16777215))
        self.inputDial_2.setMinimum(-10)
        self.inputDial_2.setMaximum(10)
        self.inputDial_2.setValue(0)
        self.inputDial_2.setSliderPosition(0)
        self.inputDial_2.setTracking(False)
        self.inputDial_2.setWrapping(False)
        self.inputDial_2.setNotchesVisible(True)

        self.verticalLayout_6.addWidget(self.inputDial_2, 0, Qt.AlignmentFlag.AlignHCenter)

        self.inputSpinBox_2 = QSpinBox(self.inputGainFrame_2)
        self.inputSpinBox_2.setObjectName(u"inputSpinBox_2")
        self.inputSpinBox_2.setMinimumSize(QSize(71, 31))
        self.inputSpinBox_2.setMaximumSize(QSize(71, 16777215))
        self.inputSpinBox_2.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.inputSpinBox_2.setCorrectionMode(QAbstractSpinBox.CorrectionMode.CorrectToNearestValue)
        self.inputSpinBox_2.setProperty(u"showGroupSeparator", False)
        self.inputSpinBox_2.setMinimum(-10)
        self.inputSpinBox_2.setMaximum(10)

        self.verticalLayout_6.addWidget(self.inputSpinBox_2, 0, Qt.AlignmentFlag.AlignHCenter)


        self.horizontalLayout_6.addWidget(self.inputGainFrame_2)

        self.IRGainFrame_2 = QFrame(self.frame)
        self.IRGainFrame_2.setObjectName(u"IRGainFrame_2")
        self.IRGainFrame_2.setEnabled(True)
        sizePolicy.setHeightForWidth(self.IRGainFrame_2.sizePolicy().hasHeightForWidth())
        self.IRGainFrame_2.setSizePolicy(sizePolicy)
        self.IRGainFrame_2.setMinimumSize(QSize(0, 101))
        self.IRGainFrame_2.setMaximumSize(QSize(112, 200))
        self.IRGainFrame_2.setFont(font1)
        self.IRGainFrame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.IRGainFrame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.IRGainFrame_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.irGainLabel_2 = QLabel(self.IRGainFrame_2)
        self.irGainLabel_2.setObjectName(u"irGainLabel_2")
        self.irGainLabel_2.setFont(font2)
        self.irGainLabel_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.irGainLabel_2)

        self.dial = QDial(self.IRGainFrame_2)
        self.dial.setObjectName(u"dial")
        self.dial.setMinimumSize(QSize(0, 95))
        self.dial.setMaximumSize(QSize(100, 16777215))
        self.dial.setMinimum(-10)
        self.dial.setMaximum(10)
        self.dial.setSliderPosition(0)
        self.dial.setTracking(False)
        self.dial.setInvertedAppearance(False)
        self.dial.setNotchesVisible(True)

        self.verticalLayout_5.addWidget(self.dial, 0, Qt.AlignmentFlag.AlignHCenter)

        self.IRSpinBox_2 = QSpinBox(self.IRGainFrame_2)
        self.IRSpinBox_2.setObjectName(u"IRSpinBox_2")
        self.IRSpinBox_2.setMinimumSize(QSize(71, 31))
        self.IRSpinBox_2.setMaximumSize(QSize(71, 31))
        self.IRSpinBox_2.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.IRSpinBox_2.setCorrectionMode(QAbstractSpinBox.CorrectionMode.CorrectToNearestValue)
        self.IRSpinBox_2.setProperty(u"showGroupSeparator", False)
        self.IRSpinBox_2.setMinimum(-10)
        self.IRSpinBox_2.setMaximum(10)

        self.verticalLayout_5.addWidget(self.IRSpinBox_2, 0, Qt.AlignmentFlag.AlignHCenter)


        self.horizontalLayout_6.addWidget(self.IRGainFrame_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.frame.raise_()
        self.inputFrame.raise_()
        self.IRFrame.raise_()
        self.outputFrame.raise_()
        self.pushButton.raise_()
        self.pushButton_11.raise_()
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.inputSpinBox.valueChanged.connect(self.inputDial.setValue)
        self.inputDial.valueChanged.connect(self.inputSpinBox.setValue)
        self.inputSpinBox_2.valueChanged.connect(self.inputDial_2.setValue)
        self.inputDial_2.valueChanged.connect(self.inputSpinBox_2.setValue)
        self.IRSpinBox_2.valueChanged.connect(self.dial.setValue)
        self.dial.valueChanged.connect(self.IRSpinBox_2.setValue)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Audio Convolver", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Input Audio", None))
        self.inputFileDisplay.setPlainText("")
        self.inputFileDisplay.setPlaceholderText(QCoreApplication.translate("MainWindow", u"filename...", None))
#if QT_CONFIG(tooltip)
        self.inputFileButton.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Accepted formats: </p><p>.mp3, .wav, .flac, .aiff, .au, .caf</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.inputFileButton.setText(QCoreApplication.translate("MainWindow", u"Select File...", None))
        self.pushButton_5.setText("")
        self.pushButton_6.setText("")
        self.pushButton_7.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Impulse Reponse", None))
        self.IRFileDisplay.setPlainText("")
        self.IRFileDisplay.setPlaceholderText(QCoreApplication.translate("MainWindow", u"filename...", None))
#if QT_CONFIG(tooltip)
        self.IRFileButton.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Accepted formats: </p><p>.mp3, .wav, .flac, .aiff, .au, .caf</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.IRFileButton.setText(QCoreApplication.translate("MainWindow", u"Select File...", None))
        self.pushButton_4.setText("")
        self.pushButton_2.setText("")
        self.pushButton_3.setText("")
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Output Audio", None))
        self.pushButton_8.setText("")
        self.pushButton_9.setText("")
        self.pushButton_10.setText("")
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Save As...", None))
        self.pushButton_11.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.inputGainLabel.setText(QCoreApplication.translate("MainWindow", u"Input Gain", None))
        self.inputSpinBox.setSuffix(QCoreApplication.translate("MainWindow", u" dB", None))
        self.inputGainLabel_2.setText(QCoreApplication.translate("MainWindow", u"IR Gain", None))
        self.inputSpinBox_2.setSuffix(QCoreApplication.translate("MainWindow", u" dB", None))
        self.irGainLabel_2.setText(QCoreApplication.translate("MainWindow", u"Output Gain", None))
        self.IRSpinBox_2.setSuffix(QCoreApplication.translate("MainWindow", u" dB", None))
    # retranslateUi

