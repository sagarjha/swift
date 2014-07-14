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
    info = {}
    info['region']=None
    info['zone']=None
    info['encrypted']=False
    info['ssd'] = False
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

    info['device-properties'] = {}
    for pairs in config.items ('default'):
        if pairs[0] not in standard:
            if pairs[1] == 'true':
                info['device-properties'][pairs[0]] = True
            else:
                info['device-properties'][pairs[0]] = False

    for i in range (0, num_replica):
        info_copy = dict(info)
        info_copy['device-properties'] = dict(info['device-properties'])
        policy_info.append(info_copy)

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
            for pairs in config.items ('replica-' + str(section)):
                if pairs[0] not in standard:
                    if pairs[1] == 'true':
                        policy_info[section-1]['device-properties'][pairs[0]] = True
                    else:
                        policy_info[section-1]['device-properties'][pairs[0]] = False

    return policy_info


