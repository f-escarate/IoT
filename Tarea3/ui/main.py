from iot import Ui_Dialog
from PyQt5 import QtCore, QtGui, QtWidgets
import plot as pl

class Controller:
    
    def __init__(self, parent):
        self.ui = Ui_Dialog()
        self.parent = parent
        self.rt_plot1 = None
        self.rt_plot2 = None
        self.rt_plot3 = None

        self.PLOT_UNITS = {
            "Temperatura": {"x": "segundos", "y": "celcius"},
            "Humedad": {"x": "segundos", "y": "g/m^3"},
            "Acc_x": {"x": "segundos", "y": "m/s^2"},
            "Acc_y": {"x": "segundos", "y": "m/s^2"},
            "Acc_z": {"x": "segundos", "y": "m/s^2"},
            "RMS": {"x": "segundos", "y": "db"},
        }
        
    def init_plots(self):

        self.rt_plot1 = pl.RealTimePlot()
        self.rt_plot1.set_config(self.ui.plot1, "Temperatura", "segundos","celcius")

        self.rt_plot2 = pl.RealTimePlot() 
        self.rt_plot2.set_config(self.ui.plot2, "Temperatura", "segundos","celcius")

        self.rt_plot3 = pl.RealTimePlot() 
        self.rt_plot3.set_config(self.ui.plot3, "Temperatura", "segundos","celcius")

    def setSignals(self):
        self.ui.selec_10.currentIndexChanged.connect(self.leerModoOperacion)
        self.ui.selec_plot1.currentIndexChanged.connect(lambda x: self.updatePlot(self.ui.selec_plot1, self.rt_plot1))
        self.ui.selec_plot2.currentIndexChanged.connect(lambda x: self.updatePlot(self.ui.selec_plot2, self.rt_plot2))
        self.ui.selec_plot3.currentIndexChanged.connect(lambda x: self.updatePlot(self.ui.selec_plot3, self.rt_plot3))
        self.ui.boton_detener.clicked.connect(self.criticalError)
        self.ui.boton_configuracion.clicked.connect(self.leerConfiguracion)

    def updatePlot(self, plot, rt_plot):
        index = plot.currentIndex()
        value = plot.itemText(index)
        x = self.PLOT_UNITS[value]["x"]
        y = self.PLOT_UNITS[value]["y"]
        rt_plot.update_labels(value, x, y)

    def leerConfiguracion(self):
        conf = dict()
        conf['AccSamp'] = self.ui.text_acc_sampling.toPlainText()
        conf['AccSen'] = self.ui.text_acc_sensibity.toPlainText()
        print (conf)
        return conf

    def leerModoOperacion(self):
        index = self.ui.selec_10.currentIndex()
        texto = self.ui.selec_10.itemText(index)
        print(texto)
        return texto

    def criticalError(self):
        popup = QtWidgets.QMessageBox(parent= self.parent)
        popup.setWindowTitle('ERROR MASIVO')
        popup.setText('QUE HAS APRETADO, NOS HAS CONDENADO A TODOS')
        popup.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        popup.exec()
        return

    def stop(self):
        print('Mori')
        return

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    cont = Controller(parent=Dialog)
    ui = cont.ui
    ui.setupUi(Dialog)
    Dialog.show()

    cont.init_plots()
    cont.setSignals()
    
    sys.exit(app.exec_())

