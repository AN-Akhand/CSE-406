import socket, sys
import rsa_1805089 as rsa
import AES_1805089 as aes
from BitVector import *
import random

#serialize an array of bitvectors
def serialize(bitvectorArray):
    serialized = ""
    for bitvector in bitvectorArray:
        serialized += bitvector.get_bitvector_in_hex()
    return serialized

def client():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 8889
    s.connect((host, port))

    alice = rsa.RSA(128)
    e, n = alice.public_key

    s.send(str(e).encode("ascii"))
    other_e = int(s.recv(1024).decode("ascii"))
    s.send(str(n).encode("ascii"))
    other_n = int(s.recv(1024).decode("ascii"))

    alice.set_public_key(other_e, other_n)

    print("Alice public key: ", alice.public_key)
    print("Alice private key: ", alice.private_key)
    print("Alice other key: ", alice.other_key)

    key = random.getrandbits(128)

    print(key)

    cipher = alice.encrypt(key)

    print(cipher)

    s.send(str(cipher).encode("ascii"))

    key = aes.handle_key(key)

    roundKeys = aes.createRoundKeys(key)

    message = input("Enter message: ")

    encryptedMessage = aes.encrypt_message(message, roundKeys)

    encryptedMessage = serialize(encryptedMessage)

    s.send(encryptedMessage.encode("ascii"))

    s.close()

client()