import os
import cmath
import numpy as np
from math import log2
from functools import reduce
from joblib import Parallel, delayed
from matplotlib.colors import Normalize
import matplotlib.cm as cm
from cv2 import imwrite

# evaluates the polynomial p at point z
def horner(p, z):
    result = 0
    for coeff in reversed(p):
        result = result * z + coeff
    return result

def drawImage(filename, rgbfun, n):
    colormat = np.zeros((n, n, 3), dtype=float)
    for i in range(n):
        for j in range(n):
            rgb01 = rgbfun(i, j) # rgb(a) values in [0,1]
            for k in range(3): 
                colormat[i,j,k] = int(255 * rgb01[2-k])
    imwrite(filename, colormat)

def mapToComplexPlaneCenter(n, c, r, i, j):
    return c + r * complex(2 * j / n - 1, 2 * i / n - 1)

def radiusJulia(poly, L=1.0000001):
    n = len(poly) - 1
    an = abs(poly[0])
    C = sum(map(abs, poly)) - an
    return max(1, 2 * C / 2, pow(2 * L / an, 1 / (n-1)))

# derivative of the given polynomial
def differentiate(poly):
    n, an = len(poly) - 1, poly[0]
    return [(n - i) * an for (i, an) in enumerate(poly[:-1])]

def demJulia(p, dp, z, K, R, overflow):
    zk, dk = np.exp(z), 1
    for _ in range(K):
        if max(
            abs(zk.real), abs(zk.imag),
            abs(dk.real), abs(dk.imag)
        ) > overflow:
            break
        dk = horner(dp, zk) * dk
        zk = horner(p, zk)
    abszk = abs(zk)
    if abszk < R:
        return 0
    else:
        absdk = abs(dk)
        if absdk == 0:
            return np.nan
        estimate = log2(abszk) * abszk / absdk
        return -log2(estimate)

def compute_dem_pixel(i, j, n, p, dp, K, r, overflow):
    z = mapToComplexPlaneCenter(n, 0, r, i, j)
    return demJulia(p, dp, z, K, r, overflow)

def drawDemJulia(n, p, colormap, K, pow_, overflow, filename):
    dp = differentiate(p)
    r = radiusJulia(p)

    results = Parallel(n_jobs=-1)(
        delayed(compute_dem_pixel)(i, j, n, p, dp, K, r, overflow)
        for i in range(n) for j in range(n)
    )

    arr = np.array(results).reshape((n, n))

    m, M = arr.min(), arr.max()
    arr[arr == 0] = M
    arr[np.isnan(arr)] = M
    normalized = Normalize(m, M)(arr)
    adjusted = pow(normalized, pow_) 
    colortable = colormap(adjusted)
            
    def rgbfun(i, j):
        if arr[i, j] == M:
            return (0, 0, 0)
        else:
            return colortable[i, j]

    drawImage(filename, rgbfun, n)

def format_coefficients(c_real, c_imag):
    return f"{c_real:.4f}{c_imag:+.4f}j"

if __name__ == '__main__':
    
    c_real = -.7269
    c_imag = .1889
    colormap_name = "Purples"  # Change this to the desired colormap name
    iterations = 10000
    size = 4000
    contrast = .7
    coefficients = [1, 0, c_real + c_imag * 1j]
    
    # Create folder if it doesn't exist
    folder_name = "fractal_images"
    if not os.path.exists(folder_name):
        try:
            os.makedirs(folder_name)
            print(f"Created folder: {folder_name}")
        except OSError as e:
            print(f"Error creating folder: {folder_name} - {e}")
    
    # Generate filename based on coefficients and colormap
    filename = f"{format_coefficients(c_real, c_imag)}_{colormap_name}_{contrast}_julia.png"
    filepath = os.path.join(folder_name, filename)
    iterations = 900
    drawDemJulia(
        size, coefficients,
        getattr(cm, colormap_name),
        iterations, contrast, 10**20, filepath
    )
    
    # Check if the file exists after saving
    if os.path.exists(filepath):
        print(f"Image saved successfully: {filepath}")
    else:
        print(f"Error: Image not saved at {filepath}")
