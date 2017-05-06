#!/usr/bin/python3

try:
    import numpy as np
    import matplotlib.pyplot as plt
except:
    np = None
    plt = None


class Cache:
    def __init__(self, partition_size, partitions, ways=1, policy=None):
        """partition_size = partition size in words
           partitions     = number of partitions
           ways.          = number of way (associativity degree)
               |            There are 'partitions/ways' sets
               |= 1     : direct mapping
               |= n     : partially associative (needs 'policy')
               |= else  : fully associative

           policy = access policy when 'ways' ≠ 1, 'partitions'
                  |= 'lfu'  : Least Frequently Used
                  |= 'lru'  : Least Recently Used
                  |= 'fifo' : First In, First Out
        """
        if ways != 1 and policy is None:
            raise ValueError('A policy is required unless using direct mapping')
        
        if policy not in [None, 'lfu', 'lru', 'fifo']:
            raise ValueError('Unknown policy given: '+policy)
        
        self.partition_size = partition_size
        self.partitions = partitions
        self.ways = ways
        self.sets = partitions // ways
        self.valid = [False] * partitions
        self.tags = [0] * partitions
        self.policy = policy
        
        # Stats
        self.misses = 0
        self.hits = 0
        
        # Policy related
        self.usecount  = [0] * partitions  # 'lfu'
        self.lasttime  = [0] * partitions  # 'lru'
        self.firsttime = [0] * partitions  # 'fifo'
    
    def access(self, ref, show=False):
        # Offset, tag and set indexs
        m, o = divmod(ref, self.partition_size)
        t, s = divmod(m, self.sets)
        # Determine the tags and validity of the available ways
        # For the case of 1 way, we will be choosing always a single way
        #     Also known as 'partitions' sets
        #
        # For the case of 'partitions' ways, we will be choosing all of them
        #     Also known as 1 single set
        #
        # For any other case, we will only choose a specific set
        start = s   * self.ways  # Set index, each of 'ways' ways
        end = start + self.ways  # Next way end
        
        # Slice everything to work on a local copy
        # TODO There has to be a better way to work on local copies
        wtags = self.tags[start:end]
        wvalid = self.valid[start:end]
        wusecount = self.usecount[start:end]
        wlasttime = self.lasttime[start:end]
        wfirsttime = self.firsttime[start:end]
        
        # Everything in the cache just got older
        for i in range(self.ways):
            wlasttime[i]  += 1
            wfirsttime[i] += 1
        
        if t in wtags and wvalid[wtags.index(t)]:
            # Hit
            self.hits += 1
            way = wtags.index(t)
            wusecount[way] += 1
            wlasttime[way]  = 0
            #  wfirsttime is the same
            if show:
                if self.ways == 1:
                    print('Hit for {} at partition {}, word offset {}'
                          .format(ref, s, o))
                elif self.ways == self.partitions:
                    print('Hit for {} at way {}, word offset {}'
                          .format(ref, s, o))
                else:
                    print('Hit for {} on set {} at way {}, word offset {}'
                          .format(ref, s, way, o))
        else:
            # Miss
            self.misses += 1
            if self.ways == 1:
                # Single way, no choice
                reason = None
                way = 0
            
            elif self.policy == 'lfu':
                # Least Frequently Used, where wusecount is minimum
                way = min(range(len(wusecount)), key=wusecount.__getitem__)
                reason = 'it was only used {} times'.format(wusecount[way])
            
            elif self.policy == 'lru':
                # Least Recently Used, where wlasttime is maximum
                way = max(range(len(wlasttime)), key=wlasttime.__getitem__)
                reason = 'it was last used {}t ago'.format(wlasttime[way])
            
            elif self.policy == 'fifo':
                # First In, First Out, where wfirsttime is maximum
                way = max(range(len(wfirsttime)), key=wfirsttime.__getitem__)
                reason = 'it was first added at {}t'.format(wfirsttime[way])
            
            if show:
                if self.ways == 1:
                    print('Miss for {}, using partition {}, word offset {}'
                          .format(ref, s, o))
                elif self.ways == self.partitions:
                    print('Miss for {}, using way {} because {}, word offset {}'
                          .format(ref, way, reason, o))
                else:
                    print('Miss for {} on set {} using way {} because {}, '
                          'word offset {}'.format(ref, s, way, reason, o))
            wtags[way] = t
            wvalid[way] = True
            
            # Reset everything (first use, last and first time now)
            wusecount[way]  = 1
            wlasttime[way]  = 0
            wfirsttime[way] = 0
        
        self.tags[start:end] = wtags
        self.valid[start:end] = wvalid
        self.usecount[start:end] = wusecount
        self.lasttime[start:end] = wlasttime
        self.firsttime[start:end] = wfirsttime
    
    def access_all(self, refs, show=False):
        if isinstance(refs, str):
            if ',' in refs:
                refs = [int(s.strip()) for s in refs.split(',')]
            elif ';' in refs:
                refs = [int(s.strip()) for s in refs.split(';')]
            else:
                refs = [int(s) for s in refs.split()]
        
        for r in refs:
            self.access(r, show=show)
    
    def __str__(self):
        return '(Cache(partitions={}, size={}, sets={}, ways={}, ' \
               'hits={}, misses={}, policy="{}"))' \
               .format(self.partitions, self.partition_size, self.sets,
                       self.ways, self.hits, self.misses, self.policy)

def plot_ways(policy='lru'):
    if np is None or plt is None:
        print('numpy and matplotlib are required for plotting')
        return
    
    fig, ax = plt.subplots()
    refs = '1 65 129 193 1 129 1 65 129 1 1 65 129 129'
    psize = 4
    partc = 16
    
    ways = []
    hits = []
    miss = []
    
    wayc = 1 
    while wayc <= partc:
        c = Cache(psize, partc, wayc, policy)
        c.access_all(refs)
        ways.append(wayc)
        hits.append(c.hits)
        miss.append(c.misses)
        wayc *= 2
        print(c)
    
    ax.plot(ways, hits, 'go-', label='hits', linewidth=1)
    ax.plot(ways, miss, 'ro-', label='misses', linewidth=1)
    
    ax.set_ylabel('Count (using '+policy.upper()+')')
    ax.set_xlabel('Number of ways')
    ax.legend()
    
    ax.set_xscale('log', basex=2)
    plt.show()

def plot_psize():
    if np is None or plt is None:
        print('numpy and matplotlib are required for plotting')
        return
    
    fig, ax = plt.subplots()
    refs = '1 4 8 5 20 17 19 56 9 11 4 43 5 6 9 17 181'
    psize = 1
    partc = 16
    
    xaxe = []
    hits = []
    miss = []
    
    while partc >= 1:
        c = Cache(psize, partc)
        c.access_all(refs)
        xaxe.append(psize)
        hits.append(c.hits)
        miss.append(c.misses)
        psize *= 2
        partc //= 2
        print(c)
    
    ax.plot(xaxe, hits, 'go-', label='hits', linewidth=1)
    ax.plot(xaxe, miss, 'ro-', label='misses', linewidth=1)
    
    ax.set_ylabel('Count')
    ax.set_xlabel('Partition size (total size constant)')
    ax.legend()
    
    ax.set_xscale('log', basex=2)
    plt.show()


if __name__ == '__main__':
    plot_psize()
    plot_ways()
