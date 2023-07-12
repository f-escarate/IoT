from iot import Ui_Dialog
from PyQt5 import QtCore, QtGui, QtWidgets
import plot as pl
from RaspberryServer.TCPRaspServer import connect
import mysql.connector

class Controller:
    
    def __init__(self, parent):
        self.ui = Ui_Dialog()
        self.parent = parent
        self.rt_plot1 = None
        self.rt_plot2 = None
        self.rt_plot3 = None
        self.config= {}
        self.thread = QtCore.QThread()

        self.PLOT_UNITS = {
            "Temperatura": {"x": "segundos", "y": "celcius","dataX" : [], "dataY" : []},
            "Humedad": {"x": "segundos", "y": "g/m^3","dataX" : [], "dataY" : []},
            "Acc_x": {"x": "segundos", "y": "m/s^2","dataX" : [], "dataY" : []},
            "Acc_y": {"x": "segundos", "y": "m/s^2","dataX" : [], "dataY" : []},
            "Acc_z": {"x": "segundos", "y": "m/s^2","dataX" : [], "dataY" : []},
            "RMS": {"x": "segundos", "y": "db","dataX" : [], "dataY" : []},
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
        self.ui.boton_inicio.clicked.connect(self.start)
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
        rt_plot.set_data(self.PLOT_UNITS[value]["dataX"],self.PLOT_UNITS[value]["dataY"])

    def leerConfiguracion(self):
        conf = dict()
        conf['AccSamp'] = self.ui.text_acc_sampling.toPlainText()
        conf['AccSen'] = self.ui.text_acc_sensibity.toPlainText()
        conf['GyroSen'] = self.ui.text_gyro_sensibility.toPlainText()
        conf['BME688Samp'] = self.ui.textEdit_18.toPlainText()
        conf['DiscTime'] = self.ui.text_disc_time.toPlainText()
        conf['TCPPort'] = self.ui.text_tcp_port.toPlainText()
        conf['UDPPort'] = self.ui.text_udp_port.toPlainText()
        conf['HostIp'] = self.ui.text_host_ip.toPlainText()
        conf['SSID'] = self.ui.text_ssid.toPlainText()
        conf['Pass'] = self.ui.text_pass.toPlainText()
        print (conf)
        self.config = conf


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
        #popup.exec()
        return

    def stop(self):
        print('Mori')
        return
        
    def add_value(self,dicti):
        if dicti["protocol"] == 0:
            pass
            
        elif dicti["protocol"] == 1:
            self.PLOT_UNITS["Temperatura"]["dataX"].append(dicti["Timestamp"])
            self.PLOT_UNITS["Temperatura"]["dataY"].append(dicti["Temp"])
            #self.PLOT_UNITS[""]["dataY"] = dicti["Pres"]
            self.PLOT_UNITS["Humedad"]["dataX"].append(dicti["Timestamp"])
            self.PLOT_UNITS["Humedad"]["dataY"].append(dicti["Hum"])
            #self.PLOT_UNITS[""]["dataY"] = dicti["CO"]
        
        self.updatePlot(self.ui.selec_plot1,self.rt_plot1)
        self.updatePlot(self.ui.selec_plot2,self.rt_plot2)
        self.updatePlot(self.ui.selec_plot3,self.rt_plot3)
        
    def start(self):
        
        
        self.worker = Worker(self.config)
        self.worker.add.connect(self.add_value)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.thread.start()

        
        
        
class Worker(QtCore.QObject):
    add = QtCore.pyqtSignal(object)
    
    def __init__(self,conf):
        super().__init__()
        self.config = conf
        
    
    def run(self):
        connect(self,self.config)
       
        
    @QtCore.pyqtSlot(object)
    def do_work(self,dicti):
        
        self.add.emit(dicti)
        

    
    

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


