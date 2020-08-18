from distgen import Generator
import numpy as np
import matplotlib.pyplot as plt
from pmd_beamphysics import plot
import yaml
import pprint
from lcls_tools import image_processing as imp
import lcls_tools
import scipy
from scipy import ndimage, misc

def create_beam(file, parameters_dict=None):
    """Create a beam object from importing a yaml file.

    Arguments:
    file -- yaml file from which the beam is being generated
    parameters_dict -- dictionary of parameters that are being applied to the yaml file (default=None) 
    """
    gen = Generator(file, verbose=0)

    if parameters_dict:

        for i,param in enumerate(parameters_dict):
                value = parameters_dict[param]

                if 'n_particle' in param:
                    gen.input['n_particle'] = value

                elif 'file' in param:
                    gen.input['output']['file'] = value

                elif all(x in param for x in ('output','type')):
                    gen.input['output']['type'] = value

                elif all(x in param for x in ('sigma_xy','units')):
                    gen.input['r_dist']['sigma_xy']['units'] = value

                elif all(x in param for x in ('sigma_xy','value')):
                    gen.input['r_dist']['sigma_xy']['value'] = value

                elif all(x in param for x in ('r_dist','type')):
                    gen.input['r_dist']['type'] = value

                elif ('random_type') in param:
                    gen.input['random_type'] = value

                elif all(x in param for x in ('MTE','units')):
                    gen.input['start']['MTE']['units'] = value

                elif all(x in param for x in ('MTE','value')):
                    gen.input['start']['MTE']['value'] = value

                elif all(x in param for x in ('start','type')):
                    gen.input['start']['type'] = value

                elif all(x in param for x in ('max_t','units')):
                    gen.input['t_dist']['max_t']['units'] = value

                elif all(x in param for x in ('max_t','value')):
                    gen.input['t_dist']['max_t']['value'] = value

                elif all(x in param for x in ('min_t','units')):
                    gen.input['t_dist']['min_t']['units'] = value

                elif all(x in param for x in ('min_t','value')):
                    gen.input['t_dist']['min_t']['value'] = value

                elif all(x in param for x in ('t_dist','type')):
                    gen.input['t_dist']['type'] = value

                elif all(x in param for x in ('total_charge','units')):
                    gen.input['total_charge']['units'] = value

                elif all(x in param for x in ('total_charge','value')):
                    gen.input['total_charge']['value'] = value
                
                else:
                    print('ERROR: One or more parameter names was invalid, please check spelling')
                    return
    else:
        print ('No parameters changed')

    gen.verbose=False
    gen.run()
    return gen
    
def gen_xyhistogram(gen, bins):
    """Returns a 2d histogram from a generated beam.
    
    Arguments:
    gen -- beam generated from create_beam()
    bins -- int or array_like or [int, int] or [array, array]. If only int is given, int=bin_x=bin_y
    """
    x = gen.particles.x
    y = gen.particles.y
    return np.histogram2d(x,y,bins)

def show_histogram(gen, bins, figsize=None, dpi=None, title=None, x_label=None, y_label=None):
    """Displays an image of a single 2d histogram.
    
    Arguments:
    gen -- beam generated from create_beam()
    bins -- Int or array_like or [int, int] or [array, array]. If only int is given, int=bin_x=bin_y
    figsize -- int/float array, figure size in inches, if histogram is a square, ratio is locked to square and 
               largest of the two values is used
    dpi -- int/float, figure resolution in pixels per inch
    title -- string
    x/y_label -- string, axes labels
    """
    H, xedges, yedges = gen_xyhistogram(gen, bins) # H -- 2d array of data values, x/yedges -- bin edge locations
    fig = plt.figure(figsize=figsize, dpi=dpi) # size of plot = fig.get_size_inches()*fig.dpi
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    fig.autofmt_xdate() # rotate x-axis labels so that they don't overlap
    plt.imshow(H, interpolation='nearest', origin='low',
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
    
def use_marginal_plot(gen, key1='y', key2='energy', bins=None):
    """Uses capabilities from marginal_plot in pmd_beamphysics to plot a histogram with axes other than x,y
    
    Arguments:
    gen -- beam generated from create_beam()
    key1 & key2 -- parameters of the beam that are being plotted against each other
                   parameters include: 'x', 'y', 'p' (momentum), 'energy', 't' (transverse time)
    bins -- int or array_like or [int, int] or [array, array]. If only int is given, int=bin_x=bin_y
    """
    particle_group = gen.particles
    plot.marginal_plot(particle_group, key1, key2, bins)
    
def change_yaml(input_file, output_file, parameters_dict=None, verbose=False):
    """Takes an input yaml file, applies parameters changes, and outputs another yaml file to a specifies location. Returns modified dict
    
    Arguments:
    input_file -- input yaml file with beam parameters
    parameters_dict -- dictionary of parameters that are being applied to the yaml file (default=None)
    verbose -- if set to True, will print input and output files formatted with pretty print (pprint)
    """
    with open(input_file) as file:
        doc = yaml.load(file, Loader=yaml.FullLoader)
        
        if verbose:
            print ('INPUT FILE PARAMETERS')
            pprint.pprint (doc)
        
    if parameters_dict:

        for i,param in enumerate(parameters_dict):
            value = parameters_dict[param]

            if 'n_particle' in param:
                doc['n_particle'] = value
                    
            elif 'file' in param:
                doc['output']['file'] = value

            elif all(x in param for x in ('output','type')):
                doc['output']['type'] = value

            elif all(x in param for x in ('sigma_xy','units')):
                doc['r_dist']['sigma_xy']['units'] = value

            elif all(x in param for x in ('sigma_xy','value')):
                doc['r_dist']['sigma_xy']['value'] = value

            elif all(x in param for x in ('r_dist','type')):
                doc['r_dist']['type'] = value

            elif ('random_type') in param:
                doc['random_type'] = value

            elif all(x in param for x in ('MTE','units')):
                doc['start']['MTE']['units'] = value

            elif all(x in param for x in ('MTE','value')):
                doc['start']['MTE']['value'] = value

            elif all(x in param for x in ('start','type')):
                doc['start']['type'] = value

            elif all(x in param for x in ('max_t','units')):
                doc['t_dist']['max_t']['units'] = value

            elif all(x in param for x in ('max_t','value')):
                doc['t_dist']['max_t']['value'] = value

            elif all(x in param for x in ('min_t','units')):
                doc['t_dist']['min_t']['units'] = value

            elif all(x in param for x in ('min_t','value')):
                doc['t_dist']['min_t']['value'] = value

            elif all(x in param for x in ('t_dist','type')):
                doc['t_dist']['type'] = value

            elif all(x in param for x in ('total_charge','units')):
                doc['total_charge']['units'] = value

            elif all(x in param for x in ('total_charge','value')):
                doc['total_charge']['value'] = value

            else:
                print('ERROR: One or more parameter names was invalid, please check spelling')
                return
            
        if verbose:
            print ('\nOUTPUT FILE PARAMETERS')
            pprint.pprint  (doc)
            
        with open(output_file, 'w') as outfile:
            yaml.dump(doc, outfile, default_flow_style=False)
            
        return (doc)

def reduce_2dArray(file, buffer, shape, verbose=False):
    # Loading image file
    image = imp.mat_image.MatImage()
    image.load_mat_image(file) # image object loaded with file
    
    # Get initial dimensions
    array = image.image
    
    r_index, c_index = scipy.ndimage.center_of_mass(array)
    splice1 = int(r_index - buffer)
    removed_top_rows = np.delete(array, np.s_[:splice1], axis=0)
    
    r_index, c_index = scipy.ndimage.center_of_mass(removed_top_rows)
    splice2 = int(r_index + buffer*(len(array)-splice1)/len(array))
    removed_bottom_rows = np.delete(removed_top_rows, np.s_[splice2:], axis=0)
    
    r_index, c_index = scipy.ndimage.center_of_mass(removed_bottom_rows)
    splice3 = int(c_index - buffer)
    removed_left_cols = np.delete(removed_bottom_rows, np.s_[:splice3], axis=1)
    
    r_index, c_index = scipy.ndimage.center_of_mass(removed_left_cols)
    splice4 = int(c_index + buffer*(len(removed_bottom_rows[0])-splice3)/len(removed_bottom_rows[0]) + buffer/5)
    reduced = np.delete(removed_left_cols, np.s_[splice4:], axis=1)
    
    # Square shaping below this line, not using SquareShape function so we can pass the dimension variables more easily
    old_xsize, old_ysize = np.shape(array) # Get dimensions of original mat image
    xsize, ysize = np.shape(reduced) # Get dimensions of reduced mat image

    if ysize > xsize:
        square = np.delete(reduced, np.s_[:(ysize-xsize)], axis=1) # Delete rows until equal with columns
    elif ysize < xsize:
        square = np.delete(reduced, np.s_[:(xsize-ysize)], axis=0) # Delete columns until equal with rows
    else:
        print ('Array is already square')

    X,Y = np.shape(square) # check to make sure they're square
    
    if X == Y:
        scale = shape/X # scale factor to make array ShapexShape
    else:
        print ('Something terrible has happened, the dimensions still are not square')
        return ()
    
    # Getting dimensions of final image
    xdim,ydim,resolution = get_dimensions(image, verbose=True)
    #x_reduction_factor = X/old_xsize
    #y_reduction_factor = X/old_ysize
    #new_xdim = xdim*x_reduction_factor
    #new_ydim = ydim*y_reduction_factor
    new_xdim = X*resolution
    new_ydim = Y*resolution
    dimensions = [new_xdim,new_ydim]
    
    if verbose:
        print ('Dimensions of reduced image: ' + str(new_xdim) + ' x ' + str(new_ydim)  + ' microns')
        print ('                           : ' + str(new_xdim*0.001) + ' x ' + str(new_ydim*0.001)  + ' mm\n')

    # Square image and return it along with others made during the process
    squared = ndimage.zoom(square, scale)
    return(array, reduced, squared, dimensions)

def SquareShape(file, shape):
    original = file
    xsize, ysize = np.shape(original)

    if ysize > xsize:
        square = np.delete(original, np.s_[:(ysize-xsize)], axis=1)
    elif ysize < xsize:
        square = np.delete(original, np.s_[:(xsize-ysize)], axis=0)
    else:
        print ('Array is already square')

    X,Y = np.shape(square) # check to make sure they're square
    
    if X == Y:
        scale = shape/X # scale factor to make array ShapexShape
    else:
        print ('Something terrible has happened, the dimensions still are not square')
        return ()
    
    result = ndimage.zoom(square, scale)
    return(result)

def get_dimensions(image_object, verbose=False):
    resolution = image_object.resolution
    cols = image_object.columns
    rows = image_object.rows
    xdim = cols*resolution
    ydim = rows*resolution
    
    if verbose:
        print (cols, rows, resolution)
        print (str(resolution) + " microns/pixel")
        print ('rows x cols: ' + str(cols) + ' x ' + str(rows))
        print ('Real life dimensions: ' + str(xdim) + ' x ' + str(ydim)  + ' microns')
        print ('                    : ' + str(xdim*0.001) + ' x ' + str(ydim*0.001)  + ' mm\n')
    
    return(xdim,ydim,resolution)