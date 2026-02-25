# Twitter Thread: Tesla Lab

## Tweet 1 (Hook)
We ran 20 computational experiments on Tesla's most controversial claims. Here's what we found 🧵

## Tweet 2
Every textbook says Marconi's 1901 transatlantic signal bounced off the ionosphere (skywave).

Our modeling suggests it was actually ground wave — a TM₀ mode with zero cutoff frequency that propagates along the Earth-ionosphere waveguide.

Tesla was arguing for ground propagation. He may have been right.

## Tweet 3
We digitally reconstructed Tesla's Colorado Springs magnifying transmitter from his original notes.

Three coupled resonator coils. 300 kW input. 124× voltage magnification. 5+ megavolts at the terminal.

📎 *Attach: results/13_frequency_response.png*

## Tweet 4
The key finding: Tesla's apparatus was a dual-mode Earth-ionosphere exciter.

It simultaneously launched:
• TM₀ surface waves (via vertical monopole)
• TE Schumann cavity resonances (via ELF from spark gap)

This coupling mechanism hasn't been described in the literature before.

📎 *Attach: results/11_dual_mode_spectrum.png*

## Tweet 5
Here's the wild part: his spark gap at 400 breaks/sec produces subharmonics that land almost exactly on Schumann resonance frequencies.

400/51 = 7.84 Hz
Schumann fundamental = 7.83 Hz

Coincidence? Or empirical optimization by Tesla?

📎 *Attach: results/13_elf_spectrum.png*

## Tweet 6
At ELF frequencies, the surface wave extends from ground to ionosphere (~80 km). It literally fills the entire Earth-ionosphere cavity.

This means TM₀ surface waves and TE Schumann modes occupy the same physical space — enabling direct energy coupling.

📎 *Attach: results/11_surface_wave_elf.png*

## Tweet 7
But how does a signal get out of landlocked Colorado Springs?

Mode conversion at coastlines. When TM₀ waves hit the conductivity boundary between land (10⁻³ S/m) and ocean (4 S/m), 1–10% converts to TE cavity modes that propagate globally.

📎 *Attach: results/11_signal_vs_distance.png*

## Tweet 8
Tesla reported his signals were stronger at night. Our model explains why:

The ionosphere rises from ~70 km (day) to ~90 km (night), reducing TM₀ attenuation by 30–80%.

The physics matches his observation perfectly.

📎 *Attach: results/12_daynight_asymmetry.png*

## Tweet 9
Predicted field strength at 1000 km: 774 μV/m.

That's well above modern detection thresholds. Tesla's apparatus contributed ~6.7% of local Schumann background power.

Detectable signal? Yes. Usable power? No. His efficiency claims don't hold up.

## Tweet 10
The TM₀ mode has been hiding in plain sight. It has zero cutoff frequency — propagates at all frequencies. Well-known in waveguide theory.

But it's almost completely absent from the Schumann resonance literature. Why? It's non-resonant, so it produces no spectral peaks.

📎 *Attach: results/12_tm_mode_dispersion.png*

## Tweet 11
Tesla detected Schumann resonances in 1899.

Schumann predicted them in 1952.

Balser and Wagner measured them in 1960.

Tesla was 53 years early and nobody believed him.

## Tweet 12
What Tesla got right:
✅ Earth resonance detection
✅ Nighttime enhancement
✅ Continental-distance signaling
✅ Importance of ground coupling

What he got wrong:
❌ Wireless power efficiency
❌ "99.97%" claims

The truth is more interesting than either the myth or the dismissal.

## Tweet 13
Full paper, 20 experiments, 47 plots, all source code — open source.

Built by @consigcody94 / Sentinel Owl Technologies

https://github.com/consigcody94/tesla-lab
