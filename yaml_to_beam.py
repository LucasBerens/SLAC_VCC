"""Create a beam object from importing a yaml file.

Arguments:
file -- yaml file from which the beam is being generated
parameters_dict -- dictionary of parameters that are being applied to the yaml file (default=None) 
"""
from distgen import Generator

def create_beam(file, parameters_dict=None):
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
    gen.particles
    print (gen.particles)
    print ('\n' + str(gen))