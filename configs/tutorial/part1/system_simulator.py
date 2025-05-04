import m5
from m5.objects import *
from m5.util import addToPath
from caches import *
from m5.objects import X86ISA

# Create system
system = System()

system.mem_mode = 'timing'

# Clock domain (4GHz base)
system.clk_domain = SrcClockDomain(clock='4GHz', voltage_domain=VoltageDomain())

# 4 cores with hyperthreading (8 logical CPUs)
system.cpu = [X86O3CPU() for _ in range(4)]  # Remove clock parameter here
for i, cpu in enumerate(system.cpu):
    cpu.clk_domain = SrcClockDomain(clock='4GHz', voltage_domain=system.clk_domain.voltage_domain)
    cpu.socket_id = 0  # Single socket
    # cpu.numThreads = 2  # Hyperthreading

# Private L1 caches (32kB per core)
for i, cpu in enumerate(system.cpu):
    # Instruction cache
    cpu.icache = L1ICache(size='32kB', assoc=8, tag_latency=2, data_latency=2, response_latency=2, mshrs=16, tgts_per_mshr=20)
    cpu.icache.connectCPU(cpu)
    
    # Data cache
    cpu.dcache = L1DCache(size='32kB', assoc=8, tag_latency=2, data_latency=2, response_latency=2, mshrs=16, tgts_per_mshr=20)
    cpu.dcache.connectCPU(cpu)
    
    # Connect to L2 via private bus
    cpu.l2bus = L2XBar()
    cpu.icache.connectBus(cpu.l2bus)
    cpu.dcache.connectBus(cpu.l2bus)
    # cpu.icache.mem_side = cpu.l2bus.cpu_side_ports
    # cpu.dcache.mem_side = cpu.l2bus.cpu_side_ports

# Private L2 caches (1MB total, 256KB per core)
for i, cpu in enumerate(system.cpu):
    cpu.l2cache = L2Cache(size='256kB', assoc=8)
    cpu.l2cache.connectCPUSideBus(cpu.l2bus)
    # cpu.l2cache.cpu_side = cpu.l2bus.mem_side_ports

# Shared L3 BUS
system.l3bus = SystemXBar()

# Connect L2 caches to L3 BUS
for cpu in system.cpu:
    cpu.l2cache.connectMemSideBus(system.l3bus)
    # cpu.l2cache.mem_side = system.l3bus.mem_side_ports

# Shared L3 cache (8MB)
system.l3cache = L3Cache(size='8MB', assoc=16)
system.l3cache.connectCPUSideBus(system.l3bus)
# system.l3cache.cpu_side = system.l3bus.cpu_side_ports

# Memory system (8GB DDR3-1600)
system.membus = SystemXBar()
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = AddrRange('8GB')
system.mem_ctrl.port = system.membus.mem_side_ports
# system.l3cache.mem_side = system.membus.cpu_side_ports
system.l3cache.connectMemSideBus(system.membus)

# Interrupts and system ports
for cpu in system.cpu:
    cpu.createInterruptController()
    cpu.interrupts[0].pio = system.membus.mem_side_ports
    cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
    cpu.interrupts[0].int_responder = system.membus.mem_side_ports
system.system_port = system.membus.cpu_side_ports

# # Process setup (for Spectre PoC)
# process = Process()
# # process.cmd = ['tests/test-progs/hello/bin/x86/linux/spectre_variant_1']
# process.cmd = ['tests/test-progs/hello/bin/x86/linux/bubblesort']
# system.workload = SEWorkload.init_compatible(process.cmd[0])

# binary = 'tests/test-progs/hello/bin/x86/linux/spectre_POC'
binary = 'tests/test-progs/hello/bin/x86/linux/bubblesort'

process = Process()
process.cmd = [binary]
system.workload = SEWorkload.init_compatible(binary)

# Assign workloads to threads - FIXED VERSION
for cpu in system.cpu:
    cpu.createThreads()
    cpu.workload = process  # Assign process directly


# Configure CPU features to match i7-4790K
for cpu in system.cpu:
    # Set ISA (one per thread)
    cpu.isa = [X86ISA()]
    
    # Branch predictor (Haswell-style)
    cpu.branchPred = TournamentBP()
    
    # ROB and IQ sizes
    cpu.numROBEntries = 192
    cpu.numIQEntries = 56

# Start simulation
root = Root(full_system=False, system=system)
m5.instantiate()

print(f"Beginning simulation of i7-4790K-like system")
print(f"Configuration:")
print(f"- 4 cores, 8 threads with O3CPU model")
print(f"- Cache hierarchy: 128KB L1i/d per core, 256KB L2 per core, 8MB shared L3")
print(f"- 8GB DDR3-1600 memory")

exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")