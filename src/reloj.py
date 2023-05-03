import datetime
class reloj:

    def __init__(self) -> None:
        self.hora = datetime.datetime.now().strftime("%H:%M:%S")
        self.id = input("Introduce el id del sensor: ")
    
    def actualizar_hora(self):
        self.hora = datetime.datetime.now().strftime("%H:%M:%S")
    
    def publish(self):
        pass
