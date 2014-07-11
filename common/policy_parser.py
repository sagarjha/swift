import ConfigParser
import random
from collections import defaultdict
from boolean_expression_parser import parse, Formula, Connective, tokenize, evaluate, change_literal_to_formula, print_formula

def policy_parser (policy_file):
    config=ConfigParser.RawConfigParser()
    config.read(policy_file)

    num_replica = config.getint('default', 'replica')

    policy_info = []

    # anything else will be taken as a device property
    standard = ['region', 'zone', 'encrypted', 'replica']

    # initialize policy_info
    for i in range (0, num_replica):
        info = {}
        info['region']=None
        info['zone']=None
        info['encrypted']=False
        if config.has_option('default', 'region'):
            region_info=config.get('default', 'region')
            info['region'] = parse(tokenize (region_info, True))
        if config.has_option('default', 'zone'):
            zone_info=config.get('default', 'zone')
            info['zone'] = parse(tokenize (zone_info, False))
        if config.has_option('default', 'encrypted'):
            encrypted_info=config.get('default', 'encrypted')
            if encrypted_info == 'true':
                info['encrypted']=True
        policy_info.append(info)

    for section in range(1,num_replica+1):
        if config.has_section('replica-' + str(section)):
            if config.has_option('replica-'+ str(section), 'region'):
                region_info = config.get('replica-' + str(section) , 'region')
                policy_info[section-1]['region']=parse(tokenize (region_info, True))
            if config.has_option('replica-'+ str(section), 'zone'):
                zone_info = config.get('replica-' + str(section) , 'zone')
                policy_info[section-1]['zone']=parse(tokenize (zone_info, False))
            if config.has_option('replica-'+ str(section), 'encrypted'):
                encrypted_info = config.get('replica-' + str(section) , 'encrypted')
                if encrypted_info == 'true':
                    policy_info[section-1]['encrypted']=True
                else:
                    policy_info[section-1]['encrypted']=False

    return policy_info

