### spec_util.py: a package to process color images of simple lab spectra
### Authors: Emily Ramey, Eden McEwen
### Date: 5/11/21

# Imports
import numpy as np

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
    c_spec = split_colors(spec_img)
    
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