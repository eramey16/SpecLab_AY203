### spec_util.py: a package to process color images of simple lab spectra
### Authors: Emily Ramey, Eden McEwen
### Date: 5/11/21

# Imports
import numpy as np
import matplotlib.pyplot as plt

#############################
##### Isolate Spectrum ######
#############################
def plot_lines(ax, *args, vert=False, **kwargs):
    """ 
    Plots horizontal lines 1 and 2 to give a 
    sense of the vertical height of the spectrum
    """
    if vert: # Plot vertical lines
        y0, y1 = ax.get_ylim()
        for line in args:
            ax.plot([line, line], [y0, y1], **kwargs)
    else: # Plot horizontal lines
        x0, x1 = ax.get_xlim()
        for line in args:
            ax.plot([x0,x1], [line,line], **kwargs)

def clip_spec(spec_img, bounds):
    """ Vertically filters the spectrum for data between y=line1 and y=line2 """
    r = np.arange(bounds[0], bounds[1])
    
    new_spec = spec_img[r, :, :]
    return new_spec

#############################
##### Color management ######
#############################

def split_colors(spec_img):
    """ Averages spectrum image (spec) and returns average color arrays """
    # Take mean along vertical axis
    c_spec = np.mean(spec_img, axis=0)
    # Separate colors
    redspec, greenspec, bluespec = [c_spec[:,i].copy() for i in range(3)]
    return redspec, greenspec, bluespec

def combine_colors(spec_img, red_stop=2350, blue_stop=4450):
    """ 
    Combines overlapping color filters for a raw spectrum
    spec_img: raw image of the spectrum
    red_stop: array index at which to split red & green filters
    blue_stop: array index at which to split red & blue filters
    """
    # Split spectrum into colors
    redspec, greenspec, bluespec = split_colors(spec_img)
    
    # Get ranges for RGB filters
    red_range = np.arange(0, red_stop)
    green_range = np.arange(red_stop, blue_stop)
    blue_range = np.arange(blue_stop, len(bluespec))
    
    # Zero filters outside their given range
    redspec[green_range] = 0; redspec[blue_range] = 0
    greenspec[red_range] = 0; greenspec[blue_range] = 0
    bluespec[red_range] = 0; bluespec[green_range] = 0
    
    # Return combined intensity
    return redspec+greenspec+bluespec

#########################
####### Plotting ########
#########################

def spec_labels(ax, y=True):
    """ Flips x and labels the x and (optionally) y axes of a graphed spectrum """
    # Flip so wavelength increases
    ax.invert_xaxis()
    
    # Take off tick labels
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Label wavelength and intensity
    ax.set_xlabel("Wavelength $\longrightarrow$", fontsize=14)
    if y:
        ax.set_ylabel("Intensity $\longrightarrow$", fontsize=14)

def test_bounds(spec_img, bounds):
    N,M = spec_img.shape[:2]
    fig, axes = plt.subplots(1,2, figsize=(15,5))
    axes[0].imshow(spec_img)
    axes[0].set_title("Image Spectrum", fontsize=16)

    plot_lines(axes[0], bounds[0], bounds[1], c='w')

    new_img = clip_spec(spec_img, bounds)
    axes[1].imshow(new_img)
    axes[1].set_title("Clipped Spectrum", fontsize=16)

    axes[0].set_xlim([0,M])
    spec_labels(axes[0], y=False)
    spec_labels(axes[1], y=False)
    
    return fig, axes

def test_filters(spec_img, rg, gb):
    fig, axes = plt.subplots(1,2, figsize=[15,5])
    
    redspec, greenspec, bluespec = split_colors(spec_img)
    
    # Color plots
    axes[0].plot(redspec, 'r', label='red')
    axes[0].plot(greenspec, 'g', label='green')
    axes[0].plot(bluespec, 'b', label='blue')
    axes[0].legend()
    axes[0].set_title("Color Response", fontsize=16)
    plot_lines(axes[0], rg, gb, vert=True, 
                      c='k', ls='--')
    spec_labels(axes[0])

    # Combine colors
    spec = combine_colors(spec_img, rg, gb)

    # Combined plot
    axes[1].plot(spec)
    axes[1].set_title("Combined Intensity", fontsize=16)
    spec_labels(axes[1])
    
    return fig, axes