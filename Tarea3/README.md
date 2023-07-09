Para esta tarea decidimos usar pygattlib por el lado de la Raspberry porque con pygatt no nos pudimos conectar bien. Al comienzo solo logramos tener una conexión utilizando la máquina de estado, pero para lograrla tuvimos que dejar el código corriendo por 3 horas aproximadamente (aproximadamente unos 1000 intentos de conexión).

Buscando en internet, encontramos la otra librería y encontramos que pygatt es un wrapper de gatttool que fue deprecado en 2017, en cambio, pygattlib está hecho de otra forma.


https://github.com/peplin/pygatt
https://github.com/oscaracena/pygattlib
https://raspberrypi.stackexchange.com/questions/120448/linux-python-bluez-bluetooth-libraries-uuids-and-handles

Como con pygattlib las conexiones se lograban al primer intento, no consideramos necesario utilizar la máquina de estados.
