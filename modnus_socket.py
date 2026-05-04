import sys
import socket
import threading
from PyQt6.QtWidgets import(
    QApplication,
    QWidget,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)
from PyQt6.QtCore import QTimer
from pymodbus.client import ModbusTcp client