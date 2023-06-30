import socket, sys
import diffie_hellman_1805089 as dh
import AES_1805089 as aes
from BitVector import *

def deserialize(serialized):
    serialized = BitVector(hexstring = serialized)
    deserialized = []
    for i in range(0, len(serialized), 128):
        deserialized.append(serialized[i:i+128])
    return deserialized

def server():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 8889
    s.bind((host, port))
    s.listen()
    c, addr = s.accept()

    bob = dh.Diffie_Hellman(128, 64)
    bob.set_public_modulus(int(c.recv(1024).decode("ascii")))
    bob.set_public_base(int(c.recv(1024).decode("ascii")))
    bob.generate_private_key()
    bob.generate_public_key()
    c.send(str(bob.A).encode("ascii"))
    bob.set_public_key(int(c.recv(1024).decode("ascii")))
    bob.generate_shared_secret_key()

    key = bob.secret_key

    key = aes.handle_key(key)

    roundKeys = aes.createRoundKeys(key)

    encryptedMessage = deserialize(c.recv(1024).decode("ascii"))

    decryptedMessage = aes.decrypt_message(encryptedMessage, roundKeys)

    print(decryptedMessage.get_bitvector_in_ascii())

    c.close()

server()