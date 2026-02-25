# YouTube Video Script: Tesla's Hidden Frequency
**Target length: 5 minutes**

---

## HOOK (0:00–0:30)

"Every physics textbook tells you Marconi's signal crossed the Atlantic by bouncing off the ionosphere. What if that's wrong? We ran 20 computational experiments on Tesla's most controversial apparatus — and found a propagation mechanism that's been hiding in the electromagnetic equations for over a century."

*Visual: Side-by-side of Tesla's Colorado Springs lab photo + modern simulation plots*

---

## SETUP (0:30–1:30)

"In 1899, Tesla built a magnifying transmitter in Colorado Springs. He claimed he could send signals around the world using the Earth itself. The physics community said: impossible. The frequencies are wrong, the attenuation is too high, the Earth is too lossy."

"But that dismissal assumed Tesla was only using one propagation mechanism. Our computational reconstruction shows he was using two — simultaneously."

*Visual: Diagram of Earth-ionosphere waveguide. Show TE modes (Schumann) vs TM₀ mode.*

---

## FINDING 1: The Hidden Mode (1:30–2:15)

"The Earth-ionosphere cavity supports a TM₀ mode with zero cutoff frequency. It propagates at every frequency. It's well-known in waveguide theory — but almost completely absent from the Schumann resonance literature. Why? Because it doesn't produce spectral peaks. It's invisible to the usual measurements."

"Tesla's vertical monopole antenna is exactly the geometry that excites this mode."

*Visual: Show `results/12_tm_mode_dispersion.png` and `results/12_complete_mode_map.png`*

---

## FINDING 2: The Spark Gap Coincidence (2:15–3:00)

"Here's where it gets interesting. Tesla's spark gap fired at about 400 times per second. The subharmonics of that rate — 400 divided by 51, 28, 19 — land almost exactly on Schumann resonance frequencies. 7.84 Hz versus 7.83 Hz for the fundamental."

"Whether Tesla tuned this deliberately or stumbled into it, his apparatus was naturally pumping energy into the Earth's resonant frequencies."

*Visual: Show `results/13_elf_spectrum.png` with Schumann frequencies highlighted*

---

## FINDING 3: Surface Wave Fills the Cavity (3:00–3:45)

"At these extremely low frequencies, something remarkable happens. The surface wave doesn't stay near the ground — it extends upward 80 to 100 kilometers, all the way to the ionosphere. It fills the entire cavity."

"That means the TM₀ surface wave and the TE Schumann resonances occupy the same physical space. They can exchange energy directly."

"And at coastlines — where ground conductivity jumps by a factor of 4,000 — one to ten percent of the surface wave converts into cavity modes that propagate globally."

*Visual: Show `results/11_surface_wave_elf.png` and `results/11_signal_vs_distance.png`*

---

## FINDING 4: Nighttime Enhancement (3:45–4:15)

"Tesla reported his signals were stronger at night. Our model shows exactly why: the ionosphere rises at night, from about 70 to 90 kilometers, reducing TM₀ attenuation by 30 to 80 percent. The day/night asymmetry in the data matches Tesla's observations perfectly."

*Visual: Show `results/12_daynight_asymmetry.png`*

---

## THE BALANCE (4:15–4:45)

"So what did Tesla get right? Earth resonance detection — 53 years before Schumann. Nighttime enhancement. Continental-distance signaling. The importance of ground coupling."

"What did he get wrong? Power efficiency. His apparatus produced detectable signals at 1000 kilometers — 774 microvolts per meter — but not usable power. The 99.97% efficiency claim doesn't survive the physics."

"The truth is more interesting than either the legend or the dismissal."

---

## CALL TO ACTION (4:45–5:00)

"The full paper, all 20 experiments, 47 plots, and complete source code are open source on GitHub. Link in the description. If you're a physicist, engineer, or just curious — check the math. That's the point of open science."

*Visual: GitHub repo link, paper title, author credit — Cody Churchwell, Sentinel Owl Technologies*
