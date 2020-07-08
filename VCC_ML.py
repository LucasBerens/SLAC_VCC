from distgen import Generator
import numpy as np
import matplotlib.pyplot as plt
from pmd_beamphysics import plot

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