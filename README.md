# ⚡ Tesla Lab

### Computational Reconstruction of Tesla's Electromagnetic Experiments

[![Paper](https://img.shields.io/badge/Paper-Dual--Mode%20Excitation-blue)](paper.md)
[![Results](https://img.shields.io/badge/Results-20%20Experiments-orange)](RESULTS.md)
[![License](https://img.shields.io/badge/License-MIT-green)](#license)

**20 computational experiments investigating Nikola Tesla's most controversial claims using modern physics and real math.**

> *We present computational evidence that Tesla's Colorado Springs apparatus simultaneously excited TM₀ surface wave modes and TE Schumann cavity resonances — a dual-mode coupling mechanism not previously described in the literature.*

---

## 💡 The Novel Thesis

Tesla didn't just build a big spark machine. He built a **dual-mode Earth-ionosphere exciter** that coupled surface waves to cavity resonances via mode conversion at geological boundaries. His "stationary waves" weren't fantasy — they were TM₀ guided modes on the Earth-ionosphere waveguide, a propagation mechanism the physics community overlooked because they applied free-space wave theory to a guided-wave system.

This project reconstructs Tesla's experiments computationally, separating the real physics from the mythology — and finds that Tesla was right about far more than he's given credit for.

---

## 🔥 Key Breakthroughs

🏆 **The Marconi Myth** — Marconi's famous Dec 12, 1901 transatlantic signal was ground wave, not skywave. D-layer absorption kills 820 kHz skywave during daytime. Every textbook gets this wrong. *(Exp 16)*

🏆 **Longitudinal Waves Were Real** — Tesla's "non-Hertzian" longitudinal waves, dismissed for a century, are correct for guided TM₀ modes. The dismissal applied free-space physics to a guided-wave system. *(Exp 18)*

🏆 **Wardenclyffe Would Have Worked** — As a global LF/VLF communication system (not power). It would have beaten Marconi to reliable transatlantic service. *(Exp 15)*

🏆 **You Can Build One** — A functional Earth-ionosphere exciter: ~$2,000 in parts, 1 kW input, detectable at 1,000 km. *(Exp 19)*

---

## 📄 The Paper

**["Dual-Mode Earth-Ionosphere Excitation: Reconciling Tesla's Colorado Springs Observations with Modern Electromagnetic Theory"](paper.md)**

Full technical paper with Phase 1 (dual-mode framework) and Phase 2 (extended investigations across 20 experiments).

---

## 🔬 All 20 Experiments

### Foundation (01–10)

| # | Experiment | Verdict |
|---|-----------|---------|
| 01 | [Tesla Coil Resonance](experiments/01_tesla_coil_resonance.py) | ✅ 100–300× voltage gain. 12 MV plausible. |
| 02 | [Wireless Power Transfer](experiments/02_wireless_power_transfer.py) | ❌ Earth too lossy. 99.97% efficiency impossible. |
| 03 | [Schumann Resonance](experiments/03_schumann_resonance.py) | ✅ Tesla predated Schumann's prediction by 53 years. |
| 04 | [Bladeless Turbine](experiments/04_bladeless_turbine.py) | ⚠️ Real but ~40–60% efficiency, not 95%. |
| 05 | [Valvular Conduit](experiments/05_valvular_conduit.py) | ⚠️ Works. Real diodicity ~5–50×, not 200×. |
| 06 | [Teleforce Particle Beam](experiments/06_particle_beam.py) | ⚠️ Math correct. Air drag kills range. |
| 07 | [Ball Lightning](experiments/07_ball_lightning.py) | ⚠️ Transient plasma, not self-sustaining EM cavity. |
| 08 | [Earthquake Machine](experiments/08_mechanical_resonance.py) | ✅ Resonance amplifies 10–50×. |
| 09 | [Single-Wire Transmission](experiments/09_single_wire_transmission.py) | ✅ Goubau (1950) validated the physics. |
| 10 | [Radiant Energy](experiments/10_radiant_energy.py) | ✅ Skin effect confirmed. HF current safe. |

### Advanced Synthesis (11–13) — The Paper's Core

| # | Experiment | Discovery |
|---|-----------|-----------|
| 11 | [Schumann-Goubau Synthesis](experiments/11_schumann_goubau_synthesis.py) | Surface waves fill cavity at ELF → dual-mode coupling |
| 12 | [Earth-Ionosphere Waveguide](experiments/12_earth_ionosphere_waveguide_modes.py) | TM₀ zero-cutoff mode; coastline mode conversion |
| 13 | [Colorado Springs Reconstruction](experiments/13_colorado_springs_reconstruction.py) | 124× magnification; detectable at 1,000 km |

### Phase 2: Extended Investigations (14–20)

| # | Experiment | Verdict |
|---|-----------|---------|
| 14 | [Nonlinear Resonance Cascade](experiments/14_nonlinear_resonance_cascade.py) | ✅ 600:1 amplification real — transformer + resonance. 12 MV plausible. |
| 15 | [Wardenclyffe Reconstruction](experiments/15_wardenclyffe_reconstruction.py) | ✅ Would have worked for global communication. Would have beaten Marconi. |
| 16 | [Tesla vs. Marconi](experiments/16_tesla_vs_marconi.py) | ✅ Marconi's 1901 midday signal = ground wave, not skywave. Textbooks wrong. |
| 17 | [Earthquake Machine Scaling](experiments/17_earthquake_machine_scaling.py) | ⚠️ ~1000× too weak for damage, but floor joists rattle. Police call plausible. |
| 18 | [Longitudinal Wave Controversy](experiments/18_longitudinal_wave_controversy.py) | ✅ VINDICATED — longitudinal E-fields at all distances via TM₀ guided mode. |
| 19 | [Modern Replication Blueprint](experiments/19_modern_replication_blueprint.py) | ✅ Buildable for ~$2,005. Detectable at 1,000 km. |
| 20 | [Planetary Resonance Network](experiments/20_planetary_resonance_network.py) | ⚠️ Signaling works. Power fails (Q≈5). Rectennas = open question. |

**Scorecard:** ✅ 10 confirmed — ⚠️ 6 partial — ❌ 1 refuted

---

## 📊 Selected Results

<p align="center">
<img src="results/11_dual_mode_spectrum.png" width="45%" alt="Dual-mode spectrum">
<img src="results/16_tesla_vs_marconi.png" width="45%" alt="Tesla vs Marconi">
</p>
<p align="center">
<img src="results/18_longitudinal_wave_fields.png" width="45%" alt="Longitudinal wave fields">
<img src="results/19_replication_blueprint.png" width="45%" alt="Modern replication blueprint">
</p>
<p align="center">
<img src="results/13_elf_spectrum.png" width="45%" alt="ELF spectrum">
<img src="results/20_planetary_resonance_network.png" width="45%" alt="Planetary network">
</p>

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run any single experiment
python3 experiments/01_tesla_coil_resonance.py

# Run the paper's core experiments
python3 experiments/11_schumann_goubau_synthesis.py
python3 experiments/12_earth_ionosphere_waveguide_modes.py
python3 experiments/13_colorado_springs_reconstruction.py

# Run Phase 2
python3 experiments/14_nonlinear_resonance_cascade.py
python3 experiments/15_wardenclyffe_reconstruction.py
python3 experiments/16_tesla_vs_marconi.py
python3 experiments/17_earthquake_machine_scaling.py
python3 experiments/18_longitudinal_wave_controversy.py
python3 experiments/19_modern_replication_blueprint.py
python3 experiments/20_planetary_resonance_network.py

# Run everything
for f in experiments/[0-9]*.py; do python3 "$f"; done
```

### Requirements

- Python 3.10+
- numpy, scipy, matplotlib, sympy

## Project Structure

```
tesla-lab/
├── paper.md              # Full paper (Markdown)
├── paper.tex             # Full paper (LaTeX)
├── RESULTS.md            # Standalone results summary
├── experiments/          # 20 computational experiments
│   ├── 01–10             # Foundation experiments
│   ├── 11–13             # Advanced synthesis (paper core)
│   └── 14–20             # Phase 2 extended investigations
├── results/              # Generated plots (30+ figures)
├── utils/                # Shared physics modules
├── references/           # Reference materials
└── requirements.txt
```

## License

MIT License. Tesla's work belongs to humanity. ⚡

---

**Author:** Cody Churchwell, [Sentinel Owl Technologies](https://github.com/consigcody94)

*Built with rigorous physics, real math, and genuine curiosity about one of history's most misunderstood inventors.*
