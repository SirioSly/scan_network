import eel
import threading
import os

#Esse código é um exemplo de aplicação cliente-servidor simples que utiliza a biblioteca Eel para criar uma interface gráfica em HTML/JS/CSS.
# O servidor é escrito em Python e é responsável por escanear uma rede local e retornar uma lista de endereços IP de dispositivos que responderam a um ping.
# O cliente é a interface gráfica criada com Eel, que chama a função do servidor para iniciar o escaneamento e exibe o resultado na tela.
# A classe adicionada é uma maneira de organizar o código e torná-lo mais legível e fácil de manter.

class Scanner:
    def __init__(self, network_to_scan):
        self.network_to_scan = network_to_scan
        self.my_ip = self.get_ip()
        self.network = network_to_scan[:network_to_scan.rfind(".")+1]
        self.clients = []
        self.threads = []
        self.lock = threading.Lock()

    def start_scan(self):
        for item in range(1, 255):
            test = self.network + str(item)

            if self.my_ip == test:
                continue

            t = threading.Thread(target=self.scanner, args=(test,))
            t.start()
            self.threads.append(t)

        for thread in self.threads:
            thread.join()

        return self.clients

    def get_ip(self):
        ip = os.popen("ipconfig")
        for line in ip.readlines():
            if "IPv4 Address" in line:
                start = line.find(":")
                end = -1
                output = line[start + 2:end]
                return output

    def scanner(self, ip_address):
        result = os.popen("ping {0} -n 1".format(ip_address)).read()

        if "TTL" in result:
            with self.lock:
                self.clients.append(ip_address)


eel.init('web')

@eel.expose
def start_scan(network_to_scan):
    scanner = Scanner(network_to_scan)
    clients = scanner.start_scan()
    return clients

try:
    eel.start('index.html', size=(1920,1080))
except (SystemExit, MemoryError, KeyboardInterrupt):
    print("Client")
