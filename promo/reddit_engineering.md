# Title: Open-source replication blueprint for Tesla's Colorado Springs magnifying transmitter — $2,005 in parts, 20 computational experiments validating the design

## Body

We computationally reconstructed Tesla's 1899 Colorado Springs magnifying transmitter and published the full design parameters, simulation code, and a bill of materials for a scaled replication.

**What you can build for ~$2,005:**

A three-coil coupled resonator system matching Tesla's architecture:
- **Primary:** 70 μH inductance, 45 nF capacitance, driven by spark gap oscillator
- **Secondary:** 20 mH helical resonator, 25 pF distributed capacitance
- **Extra coil:** 80 mH, 22 pF, with elevated capacitive terminal
- **Ground system:** 12 radials, ~30 m each
- **Coupling coefficients:** k₁₂ = 0.6, k₂₃ = 0.3

The system achieves 124× voltage magnification from primary to terminal. With a 40 kV transformer input, that's 5 MV at the top — consistent with Tesla's reported 30+ meter discharges.

**The interesting engineering finding:** The spark gap modulation at ~400 breaks/sec naturally produces ELF subharmonics that land on Schumann resonance frequencies (7.83, 14.3, 20.8 Hz). This wasn't designed in — it's an emergent property of the coupled resonator dynamics. The vertical monopole geometry then preferentially launches TM₀ surface waves into the Earth-ionosphere waveguide.

We modeled the complete system: coupled differential equations for the three-coil resonator, ELF spectral analysis of the spark gap output, field propagation in the Earth-ionosphere waveguide, and mode conversion at conductivity boundaries. 20 experiments, 47 plots, all Python, all open source.

The repo includes the full paper with derivations, all simulation code, and the parameter tables you'd need for a physical build. If anyone's interested in actually constructing a scaled version, the design space is well-characterized.

**Repo:** https://github.com/consigcody94/tesla-lab

*Cody Churchwell, Sentinel Owl Technologies*
