
class interruptor:
    def __init__(self) -> None:
        self.state = False
        self.id = input("Introduce el id del sensor: ")
    
    def encender(self):
        self.state = True

    def apagar(self):
        self.state = False
    
    def estado(self):
        return "ON" if self.state else "OFF"

    def suscribre(self):
        pass
    def publish(self):
        pass

