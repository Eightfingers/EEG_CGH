import matlab.engine
eng = matlab.engine.start_matlab()
print("Matlab engine running!")
print("Is 37 a prime?")
tf = eng.isprime(37)
print("Matlab says its ...")
print(tf)
eng.quit()
