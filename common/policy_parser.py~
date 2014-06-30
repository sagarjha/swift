import ConfigParser
import random
from collections import defaultdict


def policy_parser (policy_file, numRegions, maxZones):
    config=ConfigParser.RawConfigParser()
    config.read(policy_file)

    num_replica = config.getint('default', 'replica')

    policy_info = []

    # initialize policy_info
    for i in range (0, num_replica):
        info = {}
        if config.has_option('default', 'region'):
            region_info=config.get('default', 'region')
            region_num=int (region_info[1:])
            info['region']=set([region_num])
        else:
            info['region']=set(range(1,numRegions+1))
        if config.has_option('default', 'zone'):
            zone_info=config.get('default', 'zone')
            zone_num=int (zone_info[1:])
            info['zone']=set([zone_num])
        else:
            info['zone']=set(range(1,maxZones+1))
        info['region-inclusion']=set()
        info['zone-inclusion']=set()
        info['region-exclusion']=set()
        info['zone-exclusion']=set()
        policy_info.append(info)

    for section in range(1,num_replica+1):
        if config.has_section('replica-' + str(section)):
            if config.has_option('replica-'+ str(section), 'region'):
                region_info = config.get('replica-' + str(section) , 'region')
                if 'replica' in region_info:
                    replica_num=int(region_info.split(':')[0].split('-')[1])
                    if ('not' in region_info):
                        policy_info[section-1]['region']=set(range(1,numRegions+1))-policy_info[replica_num-1]['region']
                        policy_info[section-1]['region-exclusion'].add(replica_num)
                        policy_info[replica_num-1]['region-exclusion'].add(section)
                    else:
                        policy_info[section-1]['region']=policy_info[replica_num-1]['region']
                        policy_info[section-1]['region-inclusion'].add(replica_num)
                        policy_info[replica_num-1]['region-inclusion'].add(section)
                else:
                    if ('not' in region_info):
                        region_num=int (region_info[5:])
                        policy_info[section-1]['region']=set(range(1,maxRegions+1))-set([region_num])
                    else:
                        region_num=int (region_info[1:])
                        policy_info[section-1]['region']=set([region_num])
            if config.has_option('replica-'+ str(section), 'zone'):
                zone_info = config.get('replica-' + str(section) , 'zone')
                if 'replica' in region_info:
                    zone_num=int(zone_info.split(':')[0].split('-')[1])
                    if ('not' in zone_info):
                        policy_info[section-1]['zone']=set(range(1,maxZones+1))-policy_info[replica_num-1]['zone']
                        policy_info[section-1]['zone-exclusion'].add(replica_num)
                        policy_info[replica_num-1]['zone-exclusion'].add(section)
                    else:
                        policy_info[section-1]['zone']=policy_info[replica_num-1]['zone']
                        policy_info[section-1]['zone-inclusion'].add(replica_num)
                        policy_info[replica_num-1]['zone-inclusion'].add(section)
                else:
                    if ('not' in zone_info):
                        zone_num=int (zone_info[5:])
                        policy_info[section-1]['zone']=set(range(1,maxZones+1))-set([zone_num])
                    else:
                        zone_num=int (zone_info[1:])
                        policy_info[section-1]['zone']=set([zone_num])
    return policy_info
