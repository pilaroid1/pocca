import subprocess
import base64
from Crypto.Cipher import AES

class Secrets():
    def __init__(self):
        self.secret = self.generateSecret()
        self.cipher = AES.new(self.secret, AES.MODE_ECB)

    def decode(self, encoded):
        try:
            decoded = self.cipher.decrypt(base64.b64decode(encoded))
            return decoded.decode().strip()
        except:
            return False

    def encode(self, decoded):
        decoded = decoded.rjust(32).encode()
        encoded = base64.b64encode(self.cipher.encrypt(decoded))
        return encoded.decode()

    def generateSecret(self):
      child = subprocess.Popen(['cat','/proc/cpuinfo'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      serial = child.stdout.read().decode()
      serial2 = serial.split("Serial\t\t:")[1].split("Model")
      return(serial2[0].strip())
