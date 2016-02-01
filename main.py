#!/usr/bin/env python
import argparse
import AutoVivification as av
import pprint as pp


def merge_dict2(a, b, path=None):
    "merges b into a, with override"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_dict2(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                a[key] = b[key]
                #raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a



def get_args():
    """
    Get command line arguments
    """

    parser = argparse.ArgumentParser(description="""
Put description of application here
                   """)
    parser.add_argument('--test', action='store', dest='test',
                        help='Test name')

    parser.add_argument('--sim_type', action='store', dest='sim_type',
                        default='RTL',
                        help='Simulation type (RTL,SDF)')

    parser.add_argument('--version', action='version', version='%(prog)s 0.1')

    return parser.parse_args()

print "Hello !"
args = get_args()

cli_params= {
    'test_name' : args.test,
    'sim_type'  : args.sim_type,
}

default_cfg = av.AutoVivification()
current_cfg = av.AutoVivification()
override_cfg= av.AutoVivification()

default_cfg['class1'] = {'parameter1' :  "xxxx"}

execfile("./config/default.py", {}, {"cfg": default_cfg, "param": cli_params})
execfile("./test/test1/config.py", {}, {"cfg": current_cfg, "param": cli_params})
execfile("./config/override.py", {}, {"cfg": override_cfg, "param": cli_params})

pp.pprint(default_cfg)
pp.pprint(current_cfg)
pp.pprint(override_cfg)


merge_dict2(default_cfg, current_cfg)
merge_dict2(default_cfg, override_cfg)

pp.pprint(default_cfg)
