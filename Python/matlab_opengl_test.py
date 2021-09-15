import matlab.engine
import moderngl
import numpy as np

# import OpenGL
# import OpenGL.GL
# import OpenGL.GLUT
# import OpenGL.GLU

eng = matlab.engine.start_matlab()
print("Calling matlab function...")
eng.triarea(nargout=0)
print("Finished!")
