from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
import sys
from ExtremumFinder import ExtremumFinder
from graph import plot_function


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('extremum.ui', self)
        self.StartEngine.clicked.connect(self.calculate)
        self.exf = ExtremumFinder()
        
    def calculate(self):
        try:
            func = self.FuncInput.text()
            findmin = 1 if self.MinMaxInput.currentText() == "Поиск минимума" else 0
            a = float(self.LeftIntervalInput.text())
            b = float(self.RightIntervalInput.text())
            if a >= b:
                self.Result.setText("Левая граница интервала должна быть\nменьше правой!")
                return
            e = float(self.EpsilonInput.text())
            method = self.MethodInput.currentText()
            
            self.exf.SetFunc(func)
            
            if method == "Метод половинчатого деления":
                result, x, y = self.exf.BisectionMethod(a, b, e, findmin)
            if method == "Метод золотого сечения":
                result, x, y = self.exf.GoldenRatioMethod(a, b, e, findmin)
            if method == "Метод чисел Фиббоначи":
                result, x, y = self.exf.FibonacciNumberMethod(a, b, e, findmin)
            
            self.Result.setText(result)
            plot_function(self.exf.func, a, b, x, y)
            pixmap = QPixmap("pic.png")
            self.Graph.setPixmap(pixmap)
        except Exception:
            self.Result.setText("Заполните все поля!")
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    obj = MainWindow()
    obj.show()
    sys.exit(app.exec())
