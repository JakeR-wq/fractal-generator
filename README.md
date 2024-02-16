# Fractal Generator

A Python script for generating fractal images.

## Fractal created with this script
![Julia Fractal](example_fractals/phonejulia.png)

## Setup

To set up the required Python libraries, run the `setup.sh` script:

This script detects your operating system and installs the necessary Python libraries (`numpy`, `joblib`, `matplotlib`) using the appropriate package manager (`apt` for Linux, `brew` for macOS).

If you're using Windows, please ensure that you have Python installed and install the required libraries (`numpy`, `joblib`, `matplotlib`) manually using pip.

## Parameters

You can adjust the following parameters in the `fractal.py` file to customize the fractal image:

- `c_real`: The real part of the complex constant defining the Julia set. See [coefficients.](#coefficients)
- `c_imag`: The imaginary part of the complex constant defining the Julia set. See [coefficients.](#coefficients)
- `colormap_name`: The name of the colormap used for coloring the fractal. You can change this to any valid colormap name available in Matplotlib. [color palettes](#color-palettes)
- `iterations`: The maximum number of iterations for determining if a point belongs to the fractal. NOTE: This does not seem to have any real effect on the output image from my tests, I typically keep it ~1000
- `size`: The size of the generated image in pixels. The image will be square with dimensions `size` x `size`. Depending on PC specs, anything over 2000 can take quite a while. I've found that 2000 seems to be the "sweet spot" of high resolution without taking forever.
- `contrast`: Set between 0 and 1. Adjusts the contrast of the colors in the fractal image.

Play with `c_real` and `c_imag` to change the shapes of your fractals 

## Color Palettes <a name ="color-palettes"></a>

The `colormap_name` parameter in the `fractal.py` file allows you to choose from various color palettes to colorize the generated fractal images. You can select from the following categories:

### Diverging
- Options: PiYG, PRGn, BrBG, PuOr, RdGy, RdBu, RdYlBu, RdYlGn, Spectral, coolwarm, bwr, seismic

### Perceptually Uniform Sequential
- Options: viridis, plasma, inferno, magma, cividis

### Sequential
- Options: Greys, Purples, Blues, Greens, Oranges, Reds, YlOrBr, YlOrRd, OrRd, PuRd, RdPu, BuPu, GnBu, PuBu, YlGnBu, PuBuGn, BuGn, YlGn

### Sequential (2)
- Options: binary, gist_yarg, gist_gray, gray, bone, pink, spring, summer, autumn, winter, cool, Wistia, hot, afmhot, gist_heat, copper

### [More info and visualizations from matplotlib](https://matplotlib.org/stable/users/explain/colors/colormaps.html)

## Coefficients <a name ="coefficients"></a>

The `c_real` and `c_imag` parameters in the `fractal.py` file define the real and imaginary parts of the complex constant (`c`) used to generate the Julia set. You can experiment with different coefficients to explore various Julia sets. Here are a few examples of coefficients:

- \( −0.70176 + 0.3842i \)
- \( −0.4 + 0.6i \)
- \( −0.8 + 0.156i \)
- \( 0.355 + 0.355i \)
- \( −0.835 − 0.2321i \)
- [More found here](https://en.wikipedia.org/wiki/Julia_set), [And here](https://paulbourke.net/fractals/juliaset/)

## Usage

1. Modify the parameters of the fractal in the `fractal.py` file according to your preferences. You can also adjust the Julia function under the `demJulia` method as follows:

    ```python
    def demJulia(p, dp, z, K, R, overflow):
        zk, dk = z, 1
    ```
    `zk` represents the julia function

2. Run the `fractal.py` script:

    ```bash
    python3 fractal.py
    ```

This will generate the fractal image based on the parameters you've set.

## Acknowledgements

The content of this repository is heavily inspired by the article ["Intro to Drawing Fractals with Python"](https://nseverkar.medium.com/intro-to-drawing-fractals-with-python-6ad53bbc8208) by Nisha Severkar. 

Please check out the original article for more detailed explanations and insights into fractal generation using Python.


