import AES as aes
import random

message = open('test.png', 'rb').read()

key = random.getrandbits(128)

roundKeys = aes.createRoundKeys(aes.handle_key(key))

cipher = aes.encrypt_message(message, roundKeys)

aes.printAll(cipher)

decrypted = aes.decrypt_message(cipher, roundKeys)

open('test_decrypted.png', 'wb').write(aes.to_byte_array(decrypted))
