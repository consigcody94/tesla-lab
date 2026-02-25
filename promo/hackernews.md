# Show HN: Computational reconstruction of Tesla's 1899 transmitter reveals dual-mode Earth-ionosphere coupling

**Link:** https://github.com/consigcody94/tesla-lab

Every electromagnetics textbook credits Marconi's 1901 transatlantic transmission to skywave propagation via ionospheric reflection. We ran 20 computational experiments and found evidence that the signal was more likely ground wave (TM₀ mode), and that Tesla's Colorado Springs apparatus was substantially better suited for Earth-ionosphere coupling than previously recognized.

The core finding: Tesla's magnifying transmitter simultaneously excited TM₀ surface waves and TE Schumann cavity resonances — a dual-mode coupling mechanism not previously described in the literature. The TM₀ mode has zero cutoff frequency (well-known in waveguide theory, largely ignored in the Schumann resonance literature). At ELF frequencies, Goubau surface waves extend to ionospheric heights (~80 km), sharing physical volume with Schumann modes and enabling direct energy transfer between them.

The spark gap modulation naturally produced ELF components at Schumann frequencies. The subharmonic alignment is striking: 400/51 = 7.84 Hz vs. the 7.83 Hz fundamental. Mode conversion at coastlines (1–10% per crossing) provides the mechanism for global propagation from landlocked Colorado Springs.

What Tesla got right: Earth resonance detection (53 years before Schumann), nighttime signal enhancement (explained by day/night ionospheric asymmetry), continental-distance signaling (774 μV/m at 1000 km). What he got wrong: wireless power efficiency claims.

The repo includes the full paper, all 20 experiments with source code, and 47 plots. Apparatus parameters reconstructed from Tesla's Colorado Springs Notes. Everything is open source.

Built by Cody Churchwell / Sentinel Owl Technologies.
