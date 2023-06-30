import rsa

alice = rsa.RSA(128)
bob = rsa.RSA(128)
not_alice = rsa.RSA(128)

alice.set_public_key(*bob.public_key)
bob.set_public_key(*alice.public_key)
not_alice.set_public_key(*bob.public_key)

m = 1234567890

c, s = alice.sign(m)

n_c, n_s = not_alice.sign(m)

d_c, d_s = bob.decrypt(c), bob.decrypt(s)

print(d_s)

print(bob.verify(d_c, d_s))