import socket, sys
import rsa_1805089 as rsa
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

    bob = rsa.RSA(128)
    e, n = bob.public_key

    other_e = int(c.recv(1024).decode("ascii"))
    c.send(str(e).encode("ascii"))
    other_n = int(c.recv(1024).decode("ascii"))
    c.send(str(n).encode("ascii"))

    bob.set_public_key(other_e, other_n)

    print("Bob public key: ", bob.public_key)
    print("Bob private key: ", bob.private_key)
    print("Bob other key: ", bob.other_key)

    cipher = int(c.recv(1024).decode("ascii"))

    key = bob.decrypt(cipher)

    print(key)
    print(cipher)

    key = aes.handle_key(key)

    roundKeys = aes.createRoundKeys(key)

    encryptedMessage = deserialize(c.recv(1024).decode("ascii"))

    decryptedMessage = aes.decrypt_message(encryptedMessage, roundKeys)

    print(decryptedMessage.get_bitvector_in_ascii())

    c.close()

server()