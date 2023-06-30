import AES as aes
from BitVector import *
import time

key = input("Enter key: ")
message = input("Enter message: ")
print()

state = BitVector(textstring = message)

print('Plain Text: ')
print("In ASCII: ", message)
print("In Hex: ", state.get_bitvector_in_hex())

print()

print('Key: ')
print("In ASCII: ", key)
print("In Hex: ", BitVector(textstring = key).get_bitvector_in_hex())

print()

key = aes.handle_key(key)

start = time.time()

roundKeys = aes.createRoundKeys(key)

keySchedulingTime = (time.time() - start)

start = time.time()

cipherText = aes.encrypt_message(state, roundKeys)

encryptionTime = (time.time() - start)

print('Cipher Text: ')
print("In Hex: ", aes.get_cipher_in_hex(cipherText))
print("In ASCII: ", aes.get_cipher_in_ascii(cipherText))

print()

start = time.time()

decipheredText = aes.decrypt_message(cipherText, roundKeys)

decryptionTime = (time.time() - start)

print('Deciphered Text: ')
print("In Hex: ", decipheredText.get_bitvector_in_hex())
print("In ASCII: ", decipheredText.get_bitvector_in_ascii())

print()

print("Execution time details:")
print("Key Scheduling Time: ", keySchedulingTime, "seconds")
print("Encryption Time: ", encryptionTime, "seconds")
print("Decryption Time: ", decryptionTime, "seconds")

