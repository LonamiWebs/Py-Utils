Simply used to emulate the access hits and misses to cache given a partition
size, partition count (so cache total size `= psize * partc`), possibly
dividing it into a number of ways (so there would be `psize // ways` blocks).

Access policies are:
* `lfu` for *Least Frequently Used*
* `lru` for *Least Recently Used*
* `fifo` for *First In, First Out*
