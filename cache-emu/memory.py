#!/usr/bin/python3

import time


try:
    import numpy as np
    import matplotlib.pyplot as plt
except ImportError:
    np = None
    plt = None

try:
    import colorama
except ImportError:
    colorama = None


class ListView:
    """Similar to memoryview(bytes_buffer), but for any list"""
    def __init__(self, lst, start=None, end=None):
        self.lst = lst
        self.move(start, end)
    
    def move(self, start, end):
        self.start = 0 if start is None else max(start, 0)
        self.end = len(self.lst) if end is None else min(end, len(self.lst))
    
    def __iter__(self):
        for i in range(self.start, self.end):
            yield self.lst[i]
    
    def __len__(self):
        return self.end - self.start
    
    def __contains__(self, x):
        for i in range(self.start, self.end):
            if self.lst[i] == x:
                return True
        return False
    
    def _getindex(self, key):
        i = self.end + key if key < 0 else self.start + key
        if self.start <= i < self.end:
            return i
        
        raise IndexError('list index out of range')
    
    def __getitem__(self, key):
        return self.lst[self._getindex(key)]
    
    def __setitem__(self, key, value):
        self.lst[self._getindex(key)] = value
    
    def __str__(self):
        return str(self.lst[self.start:self.end])
    
    def __repr__(self):
        return repr(self.lst[self.start:self.end])
    
    def index(self, value):
        for i in range(self.start, self.end):
            if self.lst[i] == value:
                return i - self.start
        
        raise ValueError('{} is not in list'.format(value))
    
    def original(self, index):
        return self.start + index


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
        self.policy = policy
        self.reset()
    
    def access(self, ref, show=False, draw=False,
               delay=0, delay_hit=None, delay_miss=None):
        """Accesses a single reference on the main memory"""
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
        wtags = ListView(self.tags, start, end)
        wvalid = ListView(self.valid, start, end)
        wusecount = ListView(self.usecount, start, end)
        wlasttime = ListView(self.lasttime, start, end)
        wfirsttime = ListView(self.firsttime, start, end)
        
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
            #
            # Hit, at position (original index)
            self.last_access = True, wtags.original(t)
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
            # Miss, at position (original index)
            self.last_access = False, wtags.original(way)
        
        if draw:
            self.draw()
            print(' -> Accessed word', ref, '-',
                  self.hits, 'hits and', self.misses, 'misses')
        
        hit, _ = self.last_access
        if hit and delay_hit:
            time.sleep(delay_hit)
        elif not hit and delay_miss:
            time.sleep(delay_miss)
        elif delay:
            time.sleep(delay)
    
    def access_all(self, refs, show=False, draw=False,
                   delay=0, delay_hit=None, delay_miss=None):
        """Accesses all the references (either a list, or a
           string, comma, semicolon, or space separated values)
        """
        if isinstance(refs, str):
            if ',' in refs:
                refs = [int(s.strip()) for s in refs.split(',')]
            elif ';' in refs:
                refs = [int(s.strip()) for s in refs.split(';')]
            else:
                refs = [int(s) for s in refs.split()]
        
        for r in refs:
            self.access(r, show=show, draw=draw, delay=delay,
                        delay_hit=delay_hit, delay_miss=delay_miss)
    
    def reset(self):
        """Resets the status of the cache"""
        self.valid = [False] * self.partitions
        self.tags = [0] * self.partitions
        
        # Stats
        self.misses = 0
        self.hits = 0
        
        # Was hit? At which partition? (tuple)
        self.last_access = None, None
        
        # Policy related
        self.usecount  = [0] * self.partitions  # 'lfu'
        self.lasttime  = [0] * self.partitions  # 'lru'
        self.firsttime = [0] * self.partitions  # 'fifo'
    
    def __str__(self):
        return '(Cache(partitions={}, size={}, sets={}, ways={}, ' \
               'hits={}, misses={}, policy="{}"))' \
               .format(self.partitions, self.partition_size, self.sets,
                       self.ways, self.hits, self.misses, self.policy)
    
    def content_of(self, partition):
        """Returns the contents of a given partition index"""
        if self.valid[partition]:
            set_ = partition // self.ways
            tag  = self.tags[partition]
            
            memory_block = (tag << set_.bit_length()) | set_
            start = memory_block * self.partition_size
            
            return '{}-{}'.format(start, start + self.partition_size - 1)
        return ''

    def draw(self, show_partition=True, show_content=True, show_way=True):
        partition_padding = len(str(self.partitions - 1))
        ways_padding = len(str(self.ways - 1))
        content_padding = max(
            # len(largest) + len('-') + len(largest)
            1 + 2*len(str(self.partitions * self.partition_size)),
            len('Content')
        )
        
        # Resulting items will be spread accross many lines
        lines = []
        
        # All the partitions in the cache
        for i in range(self.partitions):
            items = []
            if show_partition:
                items.append(str(i).rjust(partition_padding))
            
            if show_content:
                content = self.content_of(i).center(content_padding)
                hit, at = self.last_access
                if colorama and i == at:
                    if hit:
                        items.append(colorama.Back.GREEN +
                                     content +
                                     colorama.Style.RESET_ALL)
                    else:
                        items.append(colorama.Back.RED +
                                     content +
                                     colorama.Style.RESET_ALL)
                else:
                    items.append(content)
            
            if show_way:
                items.append(str(i % self.ways).ljust(partition_padding))
            
            lines.append(items)
        
        # Then the column headers
        items = []
        if show_partition:
            items.append('P'.rjust(partition_padding))
        
        if show_content:
            items.append('Content'.center(content_padding))
        
        if show_way:
            items.append('W'.ljust(partition_padding))
        lines.append(items)
        
        # Header
        result = []
        line = ['┌']
        for item in lines[-1]:  # -1 will never be colored (OK size)
            line.append('─' * len(item))
            line.append('┬')
        line[-1] = '┐';
        result.append(''.join(line))
        
        # Items
        for items in reversed(lines):
            line = ['│']
            for item in items:
                line.append(item)
                line.append('│')
            result.append(''.join(line))
        
        # Footer
        line = ['└']
        for item in lines[-1]:
            line.append('─' * len(item))
            line.append('┴')
        line[-1] = '┘';
        result.append(''.join(line))
        print('\n'.join(result))


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


def draw_example():
    c = Cache(4, 8, 2, 'lru')
    for i in range(3):
     for j in range(32):
      c.access(j, draw=True, delay_hit=0.05, delay_miss=0.2)
     for j in range(32+4, 32+8):
      c.access(j, draw=True, delay_hit=0.05, delay_miss=0.2)

    print(c)


if __name__ == '__main__':
    draw_example()
    #plot_psize()
    #plot_ways()
