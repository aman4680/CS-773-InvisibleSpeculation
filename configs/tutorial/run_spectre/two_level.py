import argparse

# import the m5 (gem5) library created when gem5 is built
import m5

# import all of the SimObjects
from m5.objects import *

# Add the common scripts to our path
m5.util.addToPath("../../")

# import the caches which we made
from caches import *

# import the SimpleOpts module
from common import Options
from common import SimpleOpts
from common import CpuConfig
from common import Simulation
from common import ObjectList

# Default to running 'hello', use the compiled ISA to find the binary
# grab the specific path to the binary
thispath = os.path.dirname(os.path.realpath(__file__))
default_binary = os.path.join(
    thispath,
    "../../../",
    # "tests/test-progs/hello/bin/x86/linux/hello",
    "Spectre_variant_1/spectre_attack_binary",
)
# "tests/test-progs/hello/bin/x86/linux/hello"
# "Spectre_variant_1/spectre_attack_binary",

# Binary to execute
# SimpleOpts.add_option("binary", nargs="?", default=default_binary)
# SimpleOpts.add_option("--scheme", help=f"")
# Finalize the arguments and grab the args so we can pass it on to our objects
# options = SimpleOpts.parse_args()



parser = argparse.ArgumentParser()
parser.add_argument("binary", default=default_binary, nargs="?", type=str, help="Path to the binary to execute.")
# Options.addCommonOptions(parser)
# Options.addSEOptions(parser)
# print("Before")
options = parser.parse_args()
# print("After")

# create the system we are going to simulate
system = System()

# Set the clock frequency of the system (and all of its children)
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "2GHz"
system.clk_domain.voltage_domain = VoltageDomain()

# Set up the system
system.mem_mode = "timing"  # Use timing accesses
system.mem_ranges = [AddrRange("512MiB")]  # Create an address range

# Create a simple CPU
# print(ObjectList.cpu_list.get_names())  # Lists all available CPUs
system.cpu = DerivO3CPU(branchPred=LTAGE())

# ============== InvisiSpec starts ==============
# (CPUClass, test_mem_mode, FutureClass) = Simulation.setCPUClass(options)
# (CPUClass, test_mem_mode) = Simulation.getCPUClass("DerivO3CPU")
# CPUClass = system.cpu
# CPUClass.numThreads = 1
# print("CPUClass: ", CPUClass)
# ============== InvisiSpec ends ==============

# Create an L1 instruction and data cache
# system.cpu.icache = L1ICache(options)
# system.cpu.dcache = L1DCache(options)

system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()

# Connect the instruction and data caches to the CPU
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

# Create a memory bus, a coherent crossbar, in this case
system.l2bus = L2XBar()

# Hook the CPU ports up to the l2bus
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

# Create an L2 cache and connect it to the l2bus
# system.l2cache = L2Cache(options)
system.l2cache = L2Cache()
system.l2cache.connectCPUSideBus(system.l2bus)

# Create a memory bus
system.membus = SystemXBar()

# Connect the L2 cache to the membus
system.l2cache.connectMemSideBus(system.membus)

# create the interrupt controller for the CPU
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

# Connect the system up to the membus
system.system_port = system.membus.cpu_side_ports

# Create a DDR3 memory controller
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

system.workload = SEWorkload.init_compatible(options.binary)

# Create a process for a simple "Hello World" application
process = Process()
# Set the command
# cmd is a list which begins with the executable (like argv)
process.cmd = [options.binary]
# Set the cpu to use the process as its workload and create thread contexts
system.cpu.workload = process
system.cpu.createThreads()

print(f"CPU Type: {type(system.cpu)}")
# print(f"CPU Class: {type(CPUClass)}")

# print(issubclass(X86O3CPU, DerivO3CPU))  # Will print True if X86O3CPU is a subclass of DerivO3CPU
# print(X86O3CPU.__mro__)  # This shows the class hierarchy for X86O3CPU
# print(DerivO3CPU.__mro__)  # This shows the class hierarchy for DerivO3CPU


# [InvisiSpec] Configure simulation scheme
# if isinstance(CPUClass, DerivO3CPU):
#     print("Inside Equality, CPUClass == DerivO3CPU : ", CPUClass)
#     CpuConfig.config_scheme(type(CPUClass), system.cpu, options)


# set up the root SimObject and start the simulation
root = Root(full_system=False, system=system)
# instantiate all of the objects we've created above
m5.instantiate()

print(f"Beginning simulation!")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")