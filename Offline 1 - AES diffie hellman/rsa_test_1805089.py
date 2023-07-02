import rsa_1805089 as rsa

t = False

key_size = 128 

alice = rsa.RSA(key_size)
bob = rsa.RSA(key_size)
not_alice = rsa.RSA(key_size)

alice.set_public_key(*bob.public_key)
bob.set_public_key(*alice.public_key)
not_alice.set_public_key(*bob.public_key)

m = 1234567890

c, s = alice.sign(m)

n_c, n_s = not_alice.sign(m)

if t == True:
    d_c, d_s = bob.decrypt(n_c), bob.decrypt(n_s)
else:
    d_c, d_s = bob.decrypt(c), bob.decrypt(s)

print(d_c)

print(bob.verify(d_c, d_s))