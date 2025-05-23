import m5
import argparse
from m5.objects import *
from caches import *

parser = argparse.ArgumentParser(description='A simple system with 2-level cache.')
parser.add_argument("binary", default="", nargs="?", type=str, help="Path to the binary to execute.")
parser.add_argument("--l1i_size", help=f"L1 instruction cache size. Default: 16kB.")
parser.add_argument("--l1d_size", help=f"L1 data cache size. Default: Default: 64kB.")
parser.add_argument("--l2_size", help=f"L2 cache size. Default: 256kB.")
options = parser.parse_args()

system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '4GHz'
system.clk_domain.voltage_domain = VoltageDomain()

system.cpu = X86AtomicSimpleCPU()

system.cpu.icache = L1ICache(options)
system.cpu.dcache = L1DCache(options)

system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

system.l2bus = L2XBar()

system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

system.l2cache = L2Cache(options)
system.l2cache.connectCPUSideBus(system.l2bus)

system.membus = SystemXBar()
system.l2cache.connectMemSideBus(system.membus)

# system.mem_mode = 'timing'
system.mem_mode = 'atomic'
system.mem_ranges = [AddrRange('4GB')]

system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports
system.system_port = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# binary = 'tests/test-progs/hello/bin/x86/linux/hello'

process = Process()
process.cmd = [options.binary]

system.workload = SEWorkload.init_compatible(options.binary)

system.cpu.workload = process
system.cpu.createThreads()
# for cpu in system.cpu:
#     cpu.workload = process  # You could also assign separate processes
#     cpu.createThreads()  # Must be called for each CPU

root = Root(full_system = False, system = system)
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()

print('Exiting @ tick {} because {}'.format(m5.curTick(), exit_event.getCause()))

