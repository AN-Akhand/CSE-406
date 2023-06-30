import diffie_hellman as dh
import time

pTime = {128:0, 192:0, 256:0, 512:0}
gTime = {128:0, 192:0, 256:0, 512:0}
aTime = {128:0, 192:0, 256:0, 512:0}
Atime = {128:0, 192:0, 256:0, 512:0}
kTime = {128:0, 192:0, 256:0, 512:0} 

keySizes = [128, 192, 256]

noTrials = 20

for size in keySizes:
    for _ in range(noTrials):
        test = dh.Diffie_Hellman(size, 64)
        start = time.time_ns()
        test.generate_public_modulus()
        pTime[size] += time.time_ns() - start
        start = time.time_ns()
        test.generate_public_base()
        gTime[size] += time.time_ns() - start
        start = time.time_ns()
        test.generate_private_key()
        aTime[size] += time.time_ns() - start
        start = time.time_ns()
        test.generate_public_key()
        Atime[size] += time.time_ns() - start


        test2 = dh.Diffie_Hellman(size, 64)
        test2.set_public_modulus(test.p)
        test2.set_public_base(test.g)
        test2.generate_private_key()
        test2.generate_public_key()
        test.set_public_key(test2.A)

        test2.set_public_key(test.A)

        start = time.time_ns()
        test.generate_shared_secret_key()
        kTime[size] += time.time_ns() - start

        test2.generate_shared_secret_key()

        if test.secret_key != test2.secret_key:
            print("Error")

    print("pTime: " + str((pTime[size]/noTrials) / 1000000))
    print("gTime: " + str((gTime[size]/noTrials) / 1000000))
    print("aTime: " + str((aTime[size]/noTrials) / 1000000))
    print("Atime: " + str((Atime[size]/noTrials) / 1000000))
    print("kTime: " + str((kTime[size]/noTrials) / 1000000))
    print()

