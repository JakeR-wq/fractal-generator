import matplotlib.cm as cm
import numpy as np
from PIL import Image
from tqdm import tqdm
from mandelbrot import MandelbrotSet
from viewport import Viewport
import os

def denormalize(colormap):
    return [
        tuple(int(channel * 255) for channel in color[:3]) for color in colormap
    ]

def adjust_contrast(colormap, exponent):
    norm = cm.colors.Normalize(vmin=0, vmax=1)
    return cm.ScalarMappable(norm=norm, cmap=colormap).to_rgba(np.linspace(0, 1, 256) ** exponent)

def paint_pixel(pixel, mandelbrot_set, colormap, smooth):
    stability = mandelbrot_set.stability(complex(pixel), smooth)
    index = int(min(stability * colormap.shape[0], colormap.shape[0] - 1))
    pixel.color = tuple(int(255 * channel) for channel in colormap[index])

def paint(mandelbrot_set, viewport, colormap, smooth):
    with tqdm(total=viewport.width * viewport.height, desc="Painting Mandelbrot Set", ncols=80) as pbar:
        for pixel in viewport:
            paint_pixel(pixel, mandelbrot_set, colormap, smooth)
            pbar.update(1)

if __name__ == "__main__":
    testval = 512
    testres = testval, testval
    phone = 828, 1792
    normit = 1000
    normres = 1920, 1080
    # color_r reverses the color map
    colormapname = "plasma_r"
    # + on real shifts up + on imag shifts right
    center = -.7 + .2702j
    width = .002
    # phone bg ~ 828 x 1792
    # testval, testval
    size = testres
    iterations = testval
    contrast = .8
    
    colormap = cm.get_cmap(colormapname)
    # Adjust contrast by applying a power function to the colormap's luminance values
    adjusted_colormap = adjust_contrast(colormap, contrast)  # You can adjust the exponent for desired contrast

    palette = denormalize(adjusted_colormap)
    mandelbrot_set = MandelbrotSet(max_iterations=iterations, escape_radius=1000)
    image = Image.new(mode="RGB", size=size)
    viewport = Viewport(image, center=center, width=width)
    paint(mandelbrot_set, viewport, adjusted_colormap, smooth=True)
    
    # Create directory if it doesn't exist
    directory = "fractal_images"
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

    # Generate filename based on center and size
    center_str = str(center.real) + "+" + str(center.imag) + "j"
    size_str = str(width)
    filename = f"{center}_size_{size}_zoom{width}_clr_{colormapname}_cont_{contrast}.png"

    # Save the image with the generated filename in the 'fractal_images' directory
    filepath = os.path.join(directory, filename)
    image.save(filepath)

    print(f"Image saved as '{filepath}'.")
