import socket, sys
import diffie_hellman_1805089 as dh
import AES_1805089 as aes
from BitVector import *
from math import log2

#serialize an array of bitvectors
def serialize(bitvectorArray):
    serialized = ""
    for bitvector in bitvectorArray:
        serialized += bitvector.get_bitvector_in_hex()
    return serialized

def deserialize(serialized):
    serialized = BitVector(hexstring = serialized)
    deserialized = []
    for i in range(0, len(serialized), 128):
        deserialized.append(serialized[i:i+128])
    return deserialized

def client():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 8889
    s.connect((host, port))

    alice = dh.Diffie_Hellman(128, 64)
    alice.generate_public_modulus()
    alice.generate_public_base()
    alice.generate_private_key()
    alice.generate_public_key()
    s.send(str(alice.p).encode("ascii"))
    s.send(str(alice.g).encode("ascii"))
    alice.set_public_key(int(s.recv(1024).decode("ascii")))
    s.send(str(alice.A).encode("ascii"))
    alice.generate_shared_secret_key()

    key = alice.secret_key

    key = aes.handle_key(key)

    roundKeys = aes.createRoundKeys(key)

    message = input("Enter message: ")

    encryptedMessage = aes.encrypt_message(message, roundKeys)

    encryptedMessage = serialize(encryptedMessage)

    s.send(encryptedMessage.encode("ascii"))

    s.close()

client()