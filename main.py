#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('fn_event_log', 
    help='Path to input log file')
parser.add_argument('fnout_org_model', 
    help='Path to output model file')

args = parser.parse_args()

fn_event_log = args.fn_event_log
fnout_org_model = args.fnout_org_model

if __name__ == '__main__':
    # read event log as input
    from orgminer.IO.reader import read_xes
    with open(fn_event_log, 'r', encoding='utf-8') as f:
        el = read_xes(f)

    from orgminer.ExecutionModeMiner import direct_groupby
    exec_mode_miner = direct_groupby.ATonlyMiner(el)
    rl = exec_mode_miner.derive_resource_log(el)

    # Discover organizational groups
    print('Input a number to choose a solution:')
    print('\t1. MJA: Metric based on Joint Activities (Song & van der Aalst, 2008)')
    print('\t2. GMM: Gaussian Mixture Model')
    print('\t3. MOC: Model based Overlapping Clustering')
    #print('\t4. "Commu": Overlapping Community Detection (Appice, 2018)')
    mining_option = int(input())

    if mining_option == 1:
        print('Input the desired number of groups:', end=' ')
        num_groups = int(input())
        num_groups = list(range(num_groups, num_groups + 1))

        # build profiles
        from orgminer.ResourceProfiler.raw_profiler import \
            count_execution_frequency
        profiles = count_execution_frequency(rl, scale='log')
        from orgminer.OrganizationalModelMiner.community.graph_partitioning\
            import mja
        print('Input a number to choose a metric:')
        metrics = ['euclidean', 'correlation']
        print('\t0. Distance (Euclidean)')
        print('\t1. PCC')
        print('Option: ', end='')
        metric_option = int(input())
        ogs = mja(profiles, num_groups, 
            metric=metrics[metric_option])

    elif mining_option == 2:
        print('Input the desired number of groups:', end=' ')
        num_groups = int(input())
        num_groups = list(range(num_groups, num_groups + 1))

        # build profiles
        from orgminer.ResourceProfiler.raw_profiler import\
            count_execution_frequency
        profiles = count_execution_frequency(rl, scale='log')

        print('Input a threshold value [0, 1), in order to determine the ' +
            'resource membership:', end=' ')
        user_selected_threshold = input()
        user_selected_threshold = (float(user_selected_threshold)
            if user_selected_threshold != '' else None)

        from orgminer.OrganizationalModelMiner.clustering.overlap\
            import gmm
        ogs = gmm(profiles, num_groups, 
            threshold=user_selected_threshold,
            init='kmeans')

    elif mining_option == 3:
        print('Input the desired number of groups:', end=' ')
        num_groups = int(input())
        num_groups = list(range(num_groups, num_groups + 1))

        # build profiles
        from orgminer.ResourceProfiler.raw_profiler import\
            count_execution_frequency
        profiles = count_execution_frequency(rl, scale='log')

        from orgminer.OrganizationalModelMiner.clustering.overlap import moc
        ogs = moc(profiles, num_groups,
            init='kmeans')

    elif mining_option == 4:
        # NOTE: disable Commu option for now 
        # due to unresolved dependencies of OrgMiner on Windows platform
        raise NotImplementedError
        print('Input the desired number of groups:', end=' ')
        num_groups = int(input())

        # build profiles
        from orgminer.ResourceProfiler.raw_profiler import\
            count_execution_frequency
        profiles = count_execution_frequency(rl, scale='log')

        from orgminer.OrganizationalModelMiner.community import overlap
        ogs = overlap.link_partitioning(profiles, num_groups, 
            metric='correlation')


    else:
        raise ValueError('Failed to recognize input option!')
    
    # analyze discovery result: show resources as members of multiple groups
    from collections import defaultdict
    resource_membership = defaultdict(lambda: list())
    for group_id, group in enumerate(ogs):
        for resource in group:
            resource_membership[resource].append(group_id)

    overlapped_resource = list()
    for resource in sorted(resource_membership.keys()):
        if len(resource_membership[resource]) > 1:
            overlapped_resource.append(resource)
        else:
            pass
    
    is_result_overlapped = len(overlapped_resource) > 0
    if is_result_overlapped is False:
        print('No resources were identified as ' + 
            'having multiple group membership.')
    else:
        print('Resources identified as having multiple group membership:')
        for resource in overlapped_resource:
            print('\tResource "{}" belongs to groups {}'.format(
                resource, resource_membership[resource]))

    # output discovery result
    with open(fnout_org_model, 'w', encoding='utf-8') as fout:
        header = 'group,members'
        fout.write(header)
        fout.write('\n')
        for group_id, group in enumerate(ogs):
            line = str(group_id) + ',' + ';'.join(str(r) for r in group)
            fout.write(line)
            fout.write('\n')

    print('\n[Organizational model of {} resources in {} groups exported to "{}"]'
        .format(len(resource_membership), len(ogs), fnout_org_model))

