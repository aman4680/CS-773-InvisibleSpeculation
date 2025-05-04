import m5
from m5.objects import *

# print(dir())
# num_cores = 4  # Change this to however many cores you want


system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '2GHz'
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

system.cpu = X86TimingSimpleCPU()

system.membus = SystemXBar()

# Create CPU cores
# system.cpu = [X86TimingSimpleCPU(cpu_id=i) for i in range(num_cores)]

# Connect each CPU core
# for cpu in system.cpu:
#     cpu.icache_port = system.membus.cpu_side_ports
#     cpu.dcache_port = system.membus.cpu_side_ports
#     cpu.createInterruptController()
#     cpu.interrupts[0].pio = system.membus.mem_side_ports
#     cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
#     cpu.interrupts[0].int_responder = system.membus.mem_side_ports
#     # cpu.createThreads()

system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports

system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports
system.system_port = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR4_2400_16x4()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

binary = 'tests/test-progs/hello/bin/x86/linux/hello'

process = Process()
process.cmd = [binary]

system.workload = SEWorkload.init_compatible(binary)

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

