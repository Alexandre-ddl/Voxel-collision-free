import numpy as np

def support(A, B, direction):
    point_A = A[np.argmax(np.dot(A, direction))]
    point_B = B[np.argmax(np.dot(B, -direction))]
    return point_A - point_B

