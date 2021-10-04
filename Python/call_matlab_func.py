import matlab.engine

print("Starting engine!")
eng = matlab.engine.start_matlab()

print("Matlab engine running!")
print("Is 37 a prime?")
tf = eng.isprime(37)
print("Matlab says its ...")
print(tf)

print("Trying to call matlab script")
# triangle_size = eng.test(1,2)
# print(triangle_size)

a = eng.test(1,2)
print(a)
print("Success")

eng.quit()
