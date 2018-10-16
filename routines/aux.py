_repeat_=100
def __add_parent__():
    import os
    import sys
    sys.path.append(os.path.abspath('../'))
    sys.path.append(os.path.abspath('./'))


def load_model(architecture_file, mtype='base'):
    import models
    from tensorflow import GPUOptions, ConfigProto, Session
    checkdir = '/'.join(architecture_file.split('/')[:-1]) + '/'
    
    print('\n'*2, '-'*_repeat_, '\n:: Open Session\n', '-'*_repeat_, '\n')
    gpu_options = GPUOptions(per_process_gpu_memory_fraction=0.5)
    config=ConfigProto(allow_soft_placement=True, gpu_options=gpu_options)
    sess = Session(config=config)
    print('\n', '-'*_repeat_)
    
    model = models.__dict__[mtype].__MODEL__()
    pkg= {'model':model, 
          'architecture': architecture_file,
          'dir':checkdir}  
    models.base.__MODEL__.load_architecture(pkg)
    model.set_session(sess)
    model.build(training=False)
    model.load(pkg)
    return model

def __tensorboard_script__(fname='/tmp/tensorboard_script.sh', logidr='/tmp/'):
    with open(fname, 'w') as out:
        out.write('#!/usr/bin/env bash\n')
        out.write('tensorboard --logdir=\'{}\' --port=6006\n'.format(logidr))

def __seed__():
    from tensorflow import set_random_seed
    from numpy.random import seed
    _seed = 53
    seed(_seed)
    set_random_seed(_seed)

def __git_version__():
    import inspect, os
    try:
        with open('./.git/refs/heads/master') as f:
            committag = f.readline()
        file_ = inspect.getfile(inspect.currentframe())  # script filename (usually with path)
        dir_ = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

        return {'commit': committag, 'script': file_, 'project': dir_}
    except:
        raise Exception('Not possible to reach project commit versioning!')


def update_metric(model, mflag, _set, answer):
    for key, item in answer.items():
        if key in _set.__dict__:
            _set.__dict__[key].update(item)
            try:
                model.set_summary(tag='{}/{}/metric/{}'.format(model.namespace, mflag, key), 
                                  value=item)
            except:
                pass

def get_basic_model(value):
    import models
    return {'classifier': models.classifier,
            'regressor': models.regressor,
            'generator': models.generators,
            'discriminator': models.discriminators}[value]