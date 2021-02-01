# MQTT YOLO
### Introduccion:
MQTT(Message Queuing Telemetry Transport) es un protocolo de comunicación ligero M2M(Machine2Machine). 

<p align="center">
  <img src="https://cdn.sparkfun.com/assets/learn_tutorials/8/2/7/mqtt-explanation2.png" width="350" title="hover text">
</p>

### PASOS
- 1. Install MQTT Server

	>sudo aptitude install mosquitto
	>sudo aptitude install mosquitto-clients
	
- 2. Usar el archivo ***config*** para cargar la configuración del servidor
	>mosquitto -c mosquitto.conf 


- 3. Instalar MQTT_MODULE en entorno de trabajo
	>pip install --user paho-mqtt




### ***Fuentes:***

- Theory + Practice: IoT con MQTT + Mosquitto + Python
https://www.youtube.com/watch?v=hEFSaysEIhs
- FAST Response search
https://pypi.org/project/paho-mqtt/#subscribe-unsubscribe
- Bytedata send modes
https://stackoverflow.com/questions/8634473/sending-json-request-with-python
- Official Paho-MQTT documentation
https://pypi.org/project/paho-mqtt/#subscribe-unsubscribe



