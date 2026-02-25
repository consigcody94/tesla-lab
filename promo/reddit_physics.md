# Title: Computational evidence for a zero-cutoff TM₀ mode in the Earth-ionosphere waveguide and its coupling to Schumann resonances — implications for Tesla's 1899 apparatus

## Body

I've been working on a computational study of electromagnetic mode propagation in the Earth-ionosphere waveguide, focusing on a mechanism that seems to have been overlooked in the Schumann resonance literature: the role of the TM₀ mode.

**The gap in the literature:** The Earth-ionosphere cavity supports both TE and TM modes. Schumann resonance research focuses almost exclusively on TE modes (which produce the characteristic spectral peaks at 7.83, 14.3, 20.8 Hz, etc.). But the TM₀ mode has *zero cutoff frequency* — it propagates at all frequencies from DC up. Any vertical current source (including lightning) excites it, yet it's absent from most Schumann analyses because it's non-resonant and produces no spectral peaks.

**Why it matters:** At ELF frequencies, the Goubau surface wave radial extent is:

δ_sw ≈ (c/f) / (2π) · √(2ωε₀/σ_E) ≈ 80–100 km at 7.83 Hz

This means the surface wave fills the entire cavity, creating volumetric overlap with TE Schumann modes. Mode conversion at geological conductivity boundaries (e.g., coastlines, where σ jumps from 10⁻³ to 4 S/m) converts TM₀ → TE with ~1–10% efficiency per crossing.

**Application to Tesla:** When we digitally reconstructed Tesla's Colorado Springs transmitter (three-coil coupled resonator, 300 kW, 400 sparks/sec), we found that spark gap subharmonics land almost exactly on Schumann frequencies (400/51 = 7.84 Hz). The vertical monopole geometry preferentially excites TM₀. Combined with the mode conversion mechanism, this gives a physical basis for Tesla's reported detection of "stationary waves" — without invoking anything exotic.

Day/night ionospheric asymmetry yields α_day/α_night ≈ 1.3–1.8 for TM₀, consistent with Tesla's observation of enhanced nighttime reception.

**This is computational, not experimental.** The model uses standard Wait/Galejs formulations for the waveguide, Sommerfeld-Goubau theory for surface waves, and Corum & Corum's analysis for the apparatus parameters. All code is open source with 47 plots across 20 experiments.

I'd appreciate feedback from anyone working on Schumann resonances, ELF propagation, or waveguide theory. Is the TM₀ oversight a known issue in the community? Are there experimental measurements that could test the dual-mode coupling prediction?

**Paper + code:** https://github.com/consigcody94/tesla-lab

*Cody Churchwell, Sentinel Owl Technologies*
