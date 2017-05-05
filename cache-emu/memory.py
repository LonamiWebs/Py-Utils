#!/usr/bin/python3

try:
    import numpy as np
    import matplotlib.pyplot as plt
except:
    np = None
    plt = None


class Cache:
    def __init__(self, psize, partc, ways=1, policy=None):
        """psize = partition size (word count)
           partc = partition count
           ways  = 'partc/ways' blocks, with 'ways' blocks each
                 |= 1     : direct mapping
                 |= partc : fully associative
                 |= n     : partially associative (needs 'policy')

           policy = access policy
                  |= 'lfu'  : Least Frequently Used
                  |= 'lru'  : Least Recently Used
                  |= 'fifo' : First In, First Out
        """
        if ways != 1 and policy is None:
            raise ValueError('A policy is required unless using direct mapping')
        
        if policy not in [None, 'lfu', 'lru', 'fifo']:
            raise ValueError('Unknown policy given: '+policy)
        
        self.psize  = psize
        self.partc  = partc
        self.ways   = ways
        self.blockc = partc // ways
        self.valid  = [False] * partc
        self.tags   = [0] * partc
        self.policy = policy
        
        # Stats
        self.misses = 0
        self.hits = 0
        
        # Policy related
        self.usecount  = [0] * partc  # 'lfu'
        self.lasttime  = [0] * partc  # 'lru'
        self.firsttime = [0] * partc  # 'fifo'
    
    def access(self, ref, show=False):
        # Offset, tag and block index
        m, o = divmod(ref, self.psize)
        t, b = divmod(m, self.blockc)
        # Determine the tags and validity of the available ways
        # For the case of 1 way, we will be chosing always a single way
        # For the case of 'partc' ways, we will be choosing all of them
        # For any other case, we will only choose a part
        start = b   * self.ways  # Block index, each of 'ways' ways
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
            tag_at = wtags.index(t)
            wusecount[tag_at] += 1
            wlasttime[tag_at]  = 0
            #  wfirsttime is the same
            if show:
                print('Hit for {} at block {}[{}], offset {}'
                      .format(ref, b, tag_at, o))
        else:
            # Miss
            self.misses += 1
            if self.ways == 1:
                # Single way, no choice
                tag_at = 0
            
            elif self.policy == 'lfu':
                # Least Frequently Used, where wusecount is minimum
                tag_at = \
                    min(range(len(wusecount)), key=wusecount.__getitem__)
            
            elif self.policy == 'lru':
                # Least Recently Used, where wlasttime is maximum
                tag_at = \
                    max(range(len(wlasttime)), key=wlasttime.__getitem__)
            
            elif self.policy == 'fifo':
                # First In, First Out, where wfirsttime is maximum
                tag_at = \
                    max(range(len(wfirsttime)), key=wfirsttime.__getitem__)
            
            if show:
                print('Miss for {} at block {}, using way {}[{}]'
                      .format(ref, b, tag_at, o))
            wtags[tag_at] = t
            wvalid[tag_at] = True
            
            # Reset everything (first use, last and first time now)
            wusecount[tag_at]  = 1
            wlasttime[tag_at]  = 0
            wfirsttime[tag_at] = 0
        
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
        return '(Cache(partitions={}, size={}, ways={}, ' \
               'hits={}, misses={}, policy="{}"))' \
               .format(self.partc, self.psize, self.ways,
                       self.hits, self.misses, self.policy)

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
