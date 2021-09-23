import matlab.engine

print("Starting engine!")
eng = matlab.engine.start_matlab()

print("Matlab engine running!")
print("Is 37 a prime?")
tf = eng.isprime(37)
print("Matlab says its ...")
print(tf)

print("Trying to call matlab script")
triangle_size = eng.triarea(1,2)
print(triangle_size)

print("Success")

eng.quit()
