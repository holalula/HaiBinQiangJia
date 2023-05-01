from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal
'''
    A label that can be clicked.
    Usage:
        thxfont = QFont("Microsoft YaHei",14,70)
        thxfont.setUnderline(True)
        self.thx = ClickQLabel("Sample Label")
        self.thx.setFont(thxfont)
        self.thx.setStyleSheet("color:rgb({},{},{},255)".format(0,154,214))
        self.thx.connect_customized_slot(self.Thx)
'''
class ClickQLabel(QLabel):
    # Custom signal, note that the signal must be a class attribute
    button_clicked_signal = pyqtSignal()
    def __init__(self, parent=None):
        super(ClickQLabel, self).__init__(parent)
    def mouseReleaseEvent(self, QMouseEvent):
        self.button_clicked_signal.emit()
    # Can be linked externally with slots
    def connect_customized_slot(self, func):
        self.button_clicked_signal.connect(func)