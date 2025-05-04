# Building and Running the Optimized gem5 Simulator

This document outlines the steps to build and run the **optimized gem5 simulator** with custom debug flags and configurations.

---

## 🔧 Build Instructions

To build the optimized gem5 simulator, run the following command:

```bash
scons -j{no_of_cpus} build/X86/gem5.opt
Example: scons -j4 build/X86/gem5.opt
```


## Once built, you can run the program with the following command:

```bash
build/X86/gem5.opt configs/tutorial/run_spectre/two_level.py
```

## To run with different debug flags, use the --debug-flags option

```bash
build/X86/gem5.opt --debug-flags=Flag configs/tutorial/run_spectre/two_level.py
build/X86/gem5.opt --debug-flags=Cache configs/tutorial/run_spectre/two_level.py

```

## other useful flags
```bash
Cache, InvisiSpec, ROB, LSQ, LSQUnit, Commit
```

## To enable multiple debug flags, separate them with commas
```bash
build/X86/gem5.opt --debug-flags=Flag1,Flag2,etc configs/tutorial/run_spectre/two_level.py
Example: build/X86/gem5.opt --debug-flags=Cache,InvisiSpec,ROB configs/tutorial/run_spectre/two_level.py

