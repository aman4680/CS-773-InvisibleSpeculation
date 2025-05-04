# from m5.objects import Cache

# class L1Cache(Cache):
#     """Base L1 cache class"""
#     assoc = 2
#     tag_latency = 2
#     data_latency = 2
#     response_latency = 2
#     mshrs = 4
#     tgts_per_mshr = 20

#     def __init__(self, options=None):
#         super(L1Cache, self).__init__()
#         pass

#     def connectCPU(self, cpu):
#         raise NotImplementedError

#     def connectBus(self, bus):
#         self.mem_side = bus.cpu_side_ports

# class L1ICache(L1Cache):
#     """L1 instruction cache"""
#     size = '16kB'
    
#     def __init__(self, options=None):
#         super(L1ICache, self).__init__(options)
#         if options and hasattr(options, 'l1i_size') and options.l1i_size:
#             self.size = options.l1i_size

#     def connectCPU(self, cpu):
#         self.cpu_side = cpu.icache_port

# class L1DCache(L1Cache):
#     """L1 data cache"""
#     size = '64kB'
    
#     def __init__(self, options=None):
#         super(L1DCache, self).__init__(options)
#         if options and hasattr(options, 'l1d_size') and options.l1d_size:
#             self.size = options.l1d_size

#     def connectCPU(self, cpu):
#         self.cpu_side = cpu.dcache_port

# class L2Cache(Cache):
#     """Unified L2 cache"""
#     size = '256kB'
#     assoc = 8
#     tag_latency = 20
#     data_latency = 20
#     response_latency = 20
#     mshrs = 20
#     tgts_per_mshr = 12

#     def __init__(self, options=None):
#         super(L2Cache, self).__init__()
#         if options and hasattr(options, 'l2_size') and options.l2_size:
#             self.size = options.l2_size

#     def connectCPUSideBus(self, bus):
#         self.cpu_side = bus.mem_side_ports

#     def connectMemSideBus(self, bus):
#         self.mem_side = bus.cpu_side_ports

# class L3Cache(Cache):
#     """Shared L3 cache"""
#     size = '8MB'
#     assoc = 16
#     tag_latency = 30
#     data_latency = 30
#     response_latency = 30
#     mshrs = 32
#     tgts_per_mshr = 16

#     def __init__(self, options=None):
#         super(L3Cache, self).__init__()
#         if options and hasattr(options, 'l3_size') and options.l3_size:
#             self.size = options.l3_size

#     def connectCPUSideBus(self, bus):
#         self.cpu_side = bus.mem_side_ports

#     def connectMemSideBus(self, bus):
#         self.mem_side = bus.cpu_side_ports






from m5.objects import Cache

class L1Cache(Cache):
    """Base L1 cache class"""
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20

    def __init__(self, **kwargs):
        super(L1Cache, self).__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def connectCPU(self, cpu):
        raise NotImplementedError

    def connectBus(self, bus):
        self.mem_side = bus.cpu_side_ports

class L1ICache(L1Cache):
    """L1 instruction cache"""
    size = '16kB'
    
    def __init__(self, **kwargs):
        super(L1ICache, self).__init__(**kwargs)

    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port

class L1DCache(L1Cache):
    """L1 data cache"""
    size = '64kB'
    
    def __init__(self, **kwargs):
        super(L1DCache, self).__init__(**kwargs)

    def connectCPU(self, cpu):
        self.cpu_side = cpu.dcache_port

class L2Cache(Cache):
    """Unified L2 cache"""
    size = '256kB'
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12

    def __init__(self, **kwargs):
        super(L2Cache, self).__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports

    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports

class L3Cache(Cache):
    """Shared L3 cache"""
    size = '8MB'
    assoc = 16
    tag_latency = 30
    data_latency = 30
    response_latency = 30
    mshrs = 32
    tgts_per_mshr = 16

    def __init__(self, **kwargs):
        super(L3Cache, self).__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports

    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports