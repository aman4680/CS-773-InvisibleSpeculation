CPU_TYPE=DerivO3CPU
BP_TYPE=LTAGE
SCHEME=UnsafeBaseline # Conventional, insecure baseline processor
# SCHEME=SpectreSafeFence # Insert a fence after every indirect/conditional branch
# SCHEME=FuturisticSafeFence # Insert a fence before every load instruction
# SCHEME=SpectreSafeInvisibleSpec # USL modifies only SB, and is made visible after all the preceding branches are resolved
# SCHEME=FuturisticSafeInvisibleSpec # USL modifies only SB, and is made visible when it is either non-speculative or spec non-squashable

L1I_SIZE=32kB
L1D_SIZE=32kB
L2_SIZE=256kB

L1I_ASSOC=2
L1D_ASSOC=2
L2_ASSOC=8

ALLOWSPECBUFFHIT=TRUE


build/X86/gem5.opt \
    configs/tutorial/run_spectre/two_level.py \
    --scheme=$SCHEME \
    --cpu-type=$CPU_TYPE \

build/X86/gem5.opt configs/tutorial/run_spectre/two_level.py --scheme="UnsafeBaseline"