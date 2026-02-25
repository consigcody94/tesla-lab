#!/usr/bin/env python3
"""
══════════════════════════════════════════════════════════════════════════════
 EXPERIMENT 17 — EARTHQUAKE MACHINE SCALING
 Tesla's Mechanical Oscillator: From Lab Bench to Building Damage
══════════════════════════════════════════════════════════════════════════════

Tesla claimed that a small mechanical oscillator at 46 East Houston Street
(~1898) caused such vibrations that police came to investigate. He later
claimed he could "split the Earth in two" given enough time. This experiment
scales up Experiment 08 to test these claims against real structural
engineering data and modern vibration standards.

Models:
  (a) Forced vibration of different building types at resonance
  (b) Tesla's Houston Street story — 5-story masonry + 5 lb oscillator
  (c) Fatigue damage from sub-resonant cumulative forcing
  (d) Scaling laws: force, mass, Q-factor, time-to-damage
  (e) Comparison to DIN 4150-3 and BS 7385-2 vibration limits

References:
 - Tesla, N. "The New York World" interview, July 11, 1935
 - Seifer, M. "Wizard: Life and Times of Nikola Tesla" (1996)
 - DIN 4150-3:1999 "Structural vibration — Effects on structures"
 - BS 7385-2:1993 "Evaluation of vibration on structures"
 - Chopra, A.K. "Dynamics of Structures" (5th ed., Pearson, 2017)
 - Miner, M.A. "Cumulative Damage in Fatigue" J. Applied Mech. (1945)
══════════════════════════════════════════════════════════════════════════════
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

RESULTS = Path(__file__).parent.parent / "results"
RESULTS.mkdir(exist_ok=True)

def banner(text):
    w = 70
    print(f"\n{'═'*w}")
    print(f"  {text}")
    print(f"{'═'*w}")

def section(text):
    print(f"\n{'─'*60}")
    print(f"  § {text}")
    print(f"{'─'*60}")

g = 9.81  # m/s²

banner("EXPERIMENT 17: EARTHQUAKE MACHINE SCALING")
print("Tesla's Mechanical Oscillator — Structural Damage Analysis")

# ─────────────────────────────────────────────────────────────────────────
# Building Models
# ─────────────────────────────────────────────────────────────────────────

# Building types with structural properties
# Fundamental period T₁ ≈ 0.1N (N = number of stories) for rough estimate
buildings = {
    'Wood Frame (2-story)': {
        'mass': 30e3,        # kg (total mass)
        'stories': 2,
        'f_natural': 8.0,    # Hz (wood frames: 5-12 Hz)
        'Q': 10,             # Low Q (high damping)
        'v_damage': 20e-3,   # m/s PPV for cosmetic damage
        'v_struct': 50e-3,   # m/s PPV for structural damage
        'sigma_ult': 40e6,   # Pa (wood ultimate stress)
        'type': 'wood'
    },
    'Steel Frame (10-story)': {
        'mass': 2000e3,
        'stories': 10,
        'f_natural': 1.5,    # Hz
        'Q': 20,
        'v_damage': 40e-3,
        'v_struct': 100e-3,
        'sigma_ult': 400e6,
        'type': 'steel'
    },
    'Concrete (5-story)': {
        'mass': 500e3,
        'stories': 5,
        'f_natural': 3.0,    # Hz
        'Q': 15,
        'v_damage': 15e-3,
        'v_struct': 50e-3,
        'sigma_ult': 30e6,
        'type': 'concrete'
    },
    'Masonry (5-story)': {
        'mass': 400e3,
        'stories': 5,
        'f_natural': 4.0,    # Hz (masonry: 3-6 Hz)
        'Q': 8,              # Low Q — masonry is lossy
        'v_damage': 5e-3,    # Masonry is fragile!
        'v_struct': 15e-3,
        'sigma_ult': 5e6,    # Pa (masonry is weak in tension)
        'type': 'masonry'
    }
}

# ─────────────────────────────────────────────────────────────────────────
# Part A: Force Required for Structural Damage
# ─────────────────────────────────────────────────────────────────────────

section("A. Force Required for Structural Damage")

print(f"\n  Resonant response: x = F₀·Q / (m·ω²)")
print(f"  Velocity at resonance: v = F₀·Q / (m·ω) = F₀ / (m·ω/Q)")
print(f"  PPV for damage → required force: F = v_damage × m × ω / Q")

print(f"\n  {'Building Type':<28} {'Mass':>8} {'f₀':>6} {'Q':>4} {'F(cosmetic)':>12} {'F(structural)':>12}")
print(f"  {'─'*76}")

results_a = {}
for name, b in buildings.items():
    omega_n = 2 * np.pi * b['f_natural']
    F_cosmetic = b['v_damage'] * b['mass'] * omega_n / b['Q']
    F_structural = b['v_struct'] * b['mass'] * omega_n / b['Q']
    results_a[name] = (F_cosmetic, F_structural)
    print(f"  {name:<28} {b['mass']/1e3:>6.0f} t {b['f_natural']:>5.1f} {b['Q']:>4} "
          f"{F_cosmetic:>10.0f} N {F_structural:>10.0f} N")

print(f"\n  Tesla's oscillator force: estimated 5-50 N (from a ~5 lb device)")
print(f"  ⚠️  Even masonry requires ~{results_a['Masonry (5-story)'][0]:.0f} N for cosmetic damage")

# ─────────────────────────────────────────────────────────────────────────
# Part B: Tesla's Houston Street Story
# ─────────────────────────────────────────────────────────────────────────

section("B. Tesla's Houston Street Story (1898)")

print("""
  Claim: Tesla attached a small oscillator (~5 lbs, pocket-sized) to a
  steel beam in his Houston Street laboratory. After running for some
  time, vibrations became so severe that police arrived from neighboring
  buildings. Tesla claimed he could have destroyed the building.
  
  46 East Houston: ~5-story masonry building, built ~1880s
  Oscillator: steam-powered, ~2.3 kg (5 lbs), reciprocating
""")

# Model the Houston Street building
m_building = 400e3     # kg (5-story masonry)
f_building = 4.0       # Hz (masonry building fundamental)
Q_building = 8         # Low Q for masonry
omega_b = 2 * np.pi * f_building
k_building = m_building * omega_b**2
c_building = m_building * omega_b / Q_building

# Tesla's oscillator
m_osc = 2.3           # kg (5 lbs)
# Maximum force from a reciprocating oscillator:
# F = m_osc × ω² × stroke/2
# Assume stroke ~ 5 cm, frequency tunable
stroke = 0.05  # m
F_osc_at_resonance = m_osc * omega_b**2 * stroke / 2

print(f"  Building model:")
print(f"    Mass: {m_building/1e3:.0f} tonnes")
print(f"    Natural frequency: {f_building:.1f} Hz")
print(f"    Q factor: {Q_building}")
print(f"    Stiffness: k = {k_building/1e6:.1f} MN/m")
print(f"    Damping: c = {c_building:.0f} N·s/m")
print(f"\n  Oscillator model:")
print(f"    Mass: {m_osc:.1f} kg (5 lbs)")
print(f"    Stroke: {stroke*100:.0f} cm")
print(f"    Force at {f_building:.0f} Hz: F = {F_osc_at_resonance:.1f} N")

# Simulate forced response
def building_response(t, y, m, c_damp, k, F0, omega_d):
    x, v = y
    return [v, (-c_damp*v - k*x + F0*np.cos(omega_d*t)) / m]

# Sweep frequency to find resonance
freqs = np.linspace(0.5, 10, 200)
amplitudes_ss = np.zeros(len(freqs))
velocities_ss = np.zeros(len(freqs))

for i, f in enumerate(freqs):
    omega_d = 2 * np.pi * f
    # Steady-state analytical solution
    H = 1.0 / np.sqrt((k_building - m_building*omega_d**2)**2 + (c_building*omega_d)**2)
    amplitudes_ss[i] = F_osc_at_resonance * H
    velocities_ss[i] = amplitudes_ss[i] * omega_d

# Time-domain simulation at resonance
T_sim = 300  # seconds
sol = solve_ivp(building_response, [0, T_sim], [0, 0],
                args=(m_building, c_building, k_building, F_osc_at_resonance, omega_b),
                method='RK45', max_step=0.01, rtol=1e-8, atol=1e-10,
                t_eval=np.linspace(0, T_sim, 10000))

x_resp = sol.y[0]
v_resp = sol.y[1]
ppv = np.max(np.abs(v_resp))
max_disp = np.max(np.abs(x_resp))

print(f"\n  Resonant response (steady state):")
print(f"    Max displacement: {max_disp*1e6:.1f} µm ({max_disp*1e3:.4f} mm)")
print(f"    Peak velocity:    {ppv*1e3:.3f} mm/s")
print(f"    Peak acceleration: {ppv*omega_b*1e3:.3f} mm/s²")

# Compare to damage thresholds
v_threshold_masonry = 5e-3  # 5 mm/s PPV for masonry (DIN 4150)
print(f"\n  Damage threshold (masonry): PPV > {v_threshold_masonry*1e3:.0f} mm/s")
print(f"  Achieved PPV:               {ppv*1e3:.3f} mm/s")
ratio = ppv / v_threshold_masonry
print(f"  Ratio to threshold:         {ratio:.6f} ({ratio*100:.4f}%)")

# What force WOULD be needed?
F_needed = v_threshold_masonry * c_building  # At resonance, v_ss = F/(c)
print(f"\n  Force needed for damage:    {F_needed:.0f} N ({F_needed/g:.1f} kgf)")
print(f"  Tesla's oscillator force:   {F_osc_at_resonance:.1f} N")
print(f"  Shortfall:                  {F_needed/F_osc_at_resonance:.0f}x too weak")

# Could Tesla feel vibrations? Human perception threshold ~0.1 mm/s
v_human = 0.1e-3  # m/s
print(f"\n  Human perception threshold:  {v_human*1e3:.1f} mm/s")
print(f"  Achieved PPV:               {ppv*1e3:.3f} mm/s")
if ppv > v_human:
    print(f"  → Vibrations would be PERCEPTIBLE to humans ✓")
else:
    print(f"  → Vibrations BELOW human perception threshold ✗")

# ─────────────────────────────────────────────────────────────────────────
# Part C: Fatigue / Cumulative Damage Analysis
# ─────────────────────────────────────────────────────────────────────────

section("C. Fatigue Analysis — Cumulative Damage")

print("""
  Even sub-threshold vibrations cause fatigue damage over time.
  Using Miner's rule: D = Σ(nᵢ/Nᵢ), failure when D ≥ 1
  
  S-N curve for masonry: N = (σ_ref/σ)^m where m ≈ 5-8
""")

# Stress from vibration: σ = E × ε ≈ E × v/(c_wave)
E_masonry = 5e9      # Young's modulus for brick masonry (Pa)
c_wave_masonry = np.sqrt(E_masonry / 2000)  # Wave speed in masonry
sigma_from_v = E_masonry * ppv / c_wave_masonry  # Stress from vibration

# S-N curve for masonry (fatigue)
sigma_ref = 2e6   # Reference fatigue stress (Pa) — masonry endurance limit
m_fatigue = 6     # S-N exponent for masonry
sigma_ult_masonry = 5e6  # Ultimate compressive, but tension ~0.5 MPa

print(f"  Vibration stress: σ = E × v/c = {sigma_from_v:.2f} Pa")
print(f"  Masonry endurance limit: σ_ref = {sigma_ref/1e6:.1f} MPa")
print(f"  Ratio σ/σ_ref = {sigma_from_v/sigma_ref:.2e}")

if sigma_from_v < sigma_ref * 0.01:
    # Below endurance limit — essentially infinite life
    N_cycles = float('inf')
    print(f"  Cycles to failure: INFINITE (below endurance limit)")
    print(f"  ⚠️  Stress is {sigma_from_v/sigma_ref*100:.4f}% of endurance limit")
else:
    N_cycles = (sigma_ref / sigma_from_v)**m_fatigue
    print(f"  Cycles to failure: N = {N_cycles:.2e}")
    time_to_fail = N_cycles / f_building / 3600
    print(f"  Time to failure: {time_to_fail:.1f} hours at {f_building:.0f} Hz")

# What if we scale up the oscillator?
print(f"\n  Scaling analysis — time to fatigue failure vs oscillator force:")
print(f"  {'Force (N)':>12} {'PPV (mm/s)':>12} {'Stress (Pa)':>12} {'N_cycles':>12} {'Time':>15}")
print(f"  {'─'*67}")

forces = [F_osc_at_resonance, 10, 50, 100, 500, 1000, F_needed]
for F in forces:
    v = F / c_building  # Resonant velocity
    sigma = E_masonry * v / c_wave_masonry
    if sigma > sigma_ref * 0.01:
        N = (sigma_ref / sigma)**m_fatigue
        t_hrs = N / f_building / 3600
        if t_hrs > 1e6:
            t_str = f"{t_hrs/8760:.0f} years"
        elif t_hrs > 24:
            t_str = f"{t_hrs/24:.1f} days"
        else:
            t_str = f"{t_hrs:.1f} hours"
    else:
        N = float('inf')
        t_str = "∞"
    print(f"  {F:>12.1f} {v*1e3:>12.4f} {sigma:>12.2f} {N:>12.2e} {t_str:>15}")

# ─────────────────────────────────────────────────────────────────────────
# Part D: Scaling Laws
# ─────────────────────────────────────────────────────────────────────────

section("D. Scaling Laws: Force × Q × Time")

print("""
  At resonance, the key relationships are:
    • Displacement: x = F₀·Q / (m·ω²)  →  x ∝ F·Q/m
    • Velocity:     v = F₀ / (m·ω/Q)    →  v ∝ F·Q/(m·ω)
    • Build-up time: τ = 2Q/ω            →  τ ∝ Q
    • Time to damage: t_d ∝ (m·ω/(F·Q))^m_fatigue / f
    
  The "earthquake machine" requires: F·Q >> m·ω·v_damage
""")

# Parametric sweep: F vs Q for masonry building
F_sweep = np.logspace(-1, 4, 100)  # 0.1 N to 10 kN
Q_sweep = np.array([2, 5, 8, 15, 30, 50])

print(f"\n  Force needed for PPV = 5 mm/s (masonry damage threshold):")
for Q in Q_sweep:
    c_q = m_building * omega_b / Q
    F_need = v_threshold_masonry * c_q
    print(f"    Q = {Q:>3}: F = {F_need:>8.0f} N ({F_need/g:.1f} kgf, {F_need*0.2248:.0f} lbf)")

# Build-up time
print(f"\n  Time to reach 90% steady-state (ring-up time):")
for Q in Q_sweep:
    tau = 2 * Q / omega_b
    t_90 = 2.3 * tau  # 90% of steady state
    print(f"    Q = {Q:>3}: τ = {tau:.1f} s, t₉₀ = {t_90:.1f} s")

# ─────────────────────────────────────────────────────────────────────────
# Part E: Modern Vibration Standards Comparison
# ─────────────────────────────────────────────────────────────────────────

section("E. Modern Vibration Standards (DIN 4150-3, BS 7385-2)")

# DIN 4150-3 PPV limits for structural damage prevention
din_4150 = {
    'Commercial/Industrial': {
        '<10 Hz': 20, '10-50 Hz': 20, '50-100 Hz': 40  # mm/s
    },
    'Residential': {
        '<10 Hz': 5, '10-50 Hz': 5, '50-100 Hz': 15
    },
    'Heritage/Sensitive': {
        '<10 Hz': 3, '10-50 Hz': 3, '50-100 Hz': 8
    }
}

# BS 7385-2 limits
bs_7385 = {
    'Reinforced concrete': {'4 Hz': 50, '15 Hz': 50, '40 Hz': 50},
    'Unreinforced masonry': {'4 Hz': 15, '15 Hz': 20, '40 Hz': 50},
    'Light timber': {'4 Hz': 10, '15 Hz': 15, '40 Hz': 25},
}

print(f"\n  DIN 4150-3: Peak Particle Velocity limits (mm/s):")
print(f"  {'Building Type':<28} {'<10 Hz':>8} {'10-50 Hz':>10} {'50-100 Hz':>10}")
print(f"  {'─'*58}")
for btype, limits in din_4150.items():
    vals = list(limits.values())
    print(f"  {btype:<28} {vals[0]:>8} {vals[1]:>10} {vals[2]:>10}")

print(f"\n  BS 7385-2: Transient vibration limits (mm/s PPV):")
print(f"  {'Structure':<24} {'4 Hz':>8} {'15 Hz':>8} {'40 Hz':>8}")
print(f"  {'─'*50}")
for stype, limits in bs_7385.items():
    vals = list(limits.values())
    print(f"  {stype:<24} {vals[0]:>8} {vals[1]:>8} {vals[2]:>8}")

# Could Tesla's device exceed these limits?
print(f"\n  Tesla's oscillator at Houston Street:")
print(f"    Achieved PPV: {ppv*1e3:.4f} mm/s")
print(f"    DIN 4150 limit (heritage): 3 mm/s")
print(f"    Ratio to DIN limit: {ppv*1e3/3:.6f}")
print(f"    → {ppv*1e3/3*100:.4f}% of modern safety threshold")

# What oscillator COULD exceed standards?
print(f"\n  To exceed DIN 4150 (heritage, 3 mm/s) for masonry at 4 Hz:")
c_b = m_building * omega_b / Q_building
F_din = 3e-3 * c_b
print(f"    Required force: {F_din:.0f} N ({F_din/g:.0f} kgf)")
print(f"    This requires an oscillator mass of: {F_din/(omega_b**2 * stroke/2):.0f} kg")
print(f"    Tesla's device: {m_osc:.1f} kg → {m_osc/(F_din/(omega_b**2 * stroke/2))*100:.2f}% of required")

# ─────────────────────────────────────────────────────────────────────────
# Part F: What COULD have happened at Houston Street?
# ─────────────────────────────────────────────────────────────────────────

section("F. Alternative Explanations for Houston Street")

print("""
  If Tesla's 5 lb oscillator couldn't damage the building, what happened?
  
  1. LOCAL RESONANCE (most likely):
     Individual structural elements (floor joists, wall panels) have
     MUCH lower mass and MUCH higher natural frequencies than the
     whole building. A 2.3 kg oscillator could excite:
     • Floor joists (10-20 Hz, mass ~50-200 kg): PPV up to 50 mm/s ✓
     • Window panes (20-50 Hz, mass ~5 kg): easily shattered ✓
     • Loose objects on shelves: rattling at very low forces ✓
""")

# Floor joist model
m_joist = 100     # kg (single floor joist + tributary floor)
f_joist = 15      # Hz
Q_joist = 12
omega_j = 2 * np.pi * f_joist
c_joist = m_joist * omega_j / Q_joist
F_osc_joist = m_osc * omega_j**2 * stroke / 2

v_joist = F_osc_joist / c_joist
print(f"  Floor joist response:")
print(f"    Joist mass: {m_joist} kg, f₀ = {f_joist} Hz, Q = {Q_joist}")
print(f"    Oscillator force at {f_joist} Hz: {F_osc_joist:.1f} N")
print(f"    PPV at resonance: {v_joist*1e3:.1f} mm/s")
print(f"    DIN limit: 5 mm/s → {'EXCEEDS LIMIT ✓' if v_joist*1e3 > 5 else 'below limit'}")

print(f"""
  2. SYMPATHETIC RESONANCE OF PIPES/CONDUITS:
     Building infrastructure (water pipes, gas lines, heating ducts)
     can resonate and amplify vibrations. A vibrating pipe sounds
     much louder than it measures.

  3. EXAGGERATION:
     Tesla told this story 37 years later (1935 interview). The tale
     grew in the telling — "police investigated" may be embellished.

  4. SAND HEAP RESONANCE:
     Tesla's oscillator was mounted on a steel beam connected to
     building structure. At certain frequencies, loose mortar and
     fill between floors would shift, creating audible noise
     disproportionate to actual structural vibration.
""")

# ─────────────────────────────────────────────────────────────────────────
# Plotting
# ─────────────────────────────────────────────────────────────────────────

fig, axes = plt.subplots(2, 2, figsize=(14, 11))
fig.suptitle("Experiment 17: Earthquake Machine Scaling\nTesla's Mechanical Oscillator",
             fontsize=14, fontweight='bold')

# A: Frequency response of Houston St building
ax = axes[0, 0]
ax.semilogy(freqs, velocities_ss * 1e3, 'b-', linewidth=2)
ax.axhline(y=5, color='r', linestyle='--', linewidth=1.5, label='DIN 4150 masonry (5 mm/s)')
ax.axhline(y=0.1, color='g', linestyle=':', linewidth=1.5, label='Human perception (0.1 mm/s)')
ax.axvline(x=f_building, color='orange', linestyle=':', alpha=0.7, label=f'f₀ = {f_building} Hz')
ax.set_xlabel('Forcing Frequency (Hz)')
ax.set_ylabel('Peak Velocity (mm/s)')
ax.set_title(f'A. Houston St Building Response\n(F = {F_osc_at_resonance:.1f} N oscillator)')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# B: Time-domain buildup
ax = axes[1, 0]
t_plot = sol.t
envelope = np.abs(v_resp) * 1e3
ax.plot(t_plot, v_resp * 1e3, 'b-', alpha=0.3, linewidth=0.5)
# Smooth envelope
from scipy.signal import hilbert
analytic = np.abs(hilbert(v_resp)) * 1e3
ax.plot(t_plot, analytic, 'r-', linewidth=1.5, label='Envelope')
ax.axhline(y=5, color='r', linestyle='--', alpha=0.5, label='Damage threshold')
ax.axhline(y=0.1, color='g', linestyle=':', alpha=0.5, label='Perception threshold')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Velocity (mm/s)')
ax.set_title('B. Resonant Build-up at Houston St')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# C: Force required vs building type
ax = axes[0, 1]
names = list(buildings.keys())
short_names = ['Wood\n2-story', 'Steel\n10-story', 'Concrete\n5-story', 'Masonry\n5-story']
F_cos = [results_a[n][0] for n in names]
F_str = [results_a[n][1] for n in names]
x_pos = np.arange(len(names))
w = 0.35
ax.bar(x_pos - w/2, F_cos, w, label='Cosmetic damage', color='orange', edgecolor='black')
ax.bar(x_pos + w/2, F_str, w, label='Structural damage', color='red', edgecolor='black')
ax.axhline(y=F_osc_at_resonance, color='blue', linestyle='--', linewidth=2,
           label=f'Tesla oscillator ({F_osc_at_resonance:.0f} N)')
ax.set_xticks(x_pos)
ax.set_xticklabels(short_names, fontsize=8)
ax.set_ylabel('Force Required at Resonance (N)')
ax.set_title('C. Force for Building Damage')
ax.set_yscale('log')
ax.legend(fontsize=7)
ax.grid(True, alpha=0.3, axis='y')

# D: Scaling — oscillator mass vs PPV for different Q
ax = axes[1, 1]
m_osc_range = np.logspace(-1, 4, 100)  # 0.1 kg to 10 tonnes
for Q in [5, 8, 15, 30]:
    c_q = m_building * omega_b / Q
    F_range = m_osc_range * omega_b**2 * stroke / 2
    v_range = F_range / c_q * 1e3  # mm/s
    ax.loglog(m_osc_range, v_range, linewidth=2, label=f'Q={Q}')
ax.axhline(y=5, color='r', linestyle='--', alpha=0.7, label='DIN 4150 masonry')
ax.axhline(y=0.1, color='g', linestyle=':', alpha=0.7, label='Human perception')
ax.axvline(x=2.3, color='blue', linestyle=':', alpha=0.7, label='Tesla (2.3 kg)')
ax.set_xlabel('Oscillator Mass (kg)')
ax.set_ylabel('PPV at Building Resonance (mm/s)')
ax.set_title('D. Scaling: Mass vs Vibration (5-story masonry)')
ax.legend(fontsize=7, ncol=2)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(RESULTS / "17_earthquake_machine_scaling.png", dpi=150, bbox_inches='tight')
print(f"\n  📊 Plot saved: {RESULTS}/17_earthquake_machine_scaling.png")

# ─────────────────────────────────────────────────────────────────────────
# Verdict
# ─────────────────────────────────────────────────────────────────────────

banner("VERDICT")
print(f"""
  Tesla's Earthquake Machine — Scaling Analysis:

  1. WHOLE-BUILDING DAMAGE: A 5 lb (2.3 kg) oscillator produces
     ~{F_osc_at_resonance:.0f} N of force at building resonance (~4 Hz).
     To damage a 5-story masonry building requires ~{F_needed:.0f} N.
     Tesla's device was {F_needed/F_osc_at_resonance:.0f}× too weak.
     VERDICT: Cannot damage whole building structure. ✗

  2. LOCAL ELEMENT DAMAGE: Individual components (floor joists,
     windows, pipes) have much lower mass. Tesla's oscillator could
     produce {v_joist*1e3:.0f} mm/s PPV in floor joists — enough to exceed
     modern vibration standards and cause perceptible shaking.
     VERDICT: Could cause local vibration + noise. ✓

  3. FATIGUE: Even at resonance, stresses from a 5 lb oscillator
     are far below masonry endurance limits. Cumulative fatigue
     damage would take effectively infinite time.
     VERDICT: Fatigue damage not viable at this force level. ✗

  4. SCALING LAW: To match DIN 4150 limits for masonry:
     Need ~{F_din:.0f} N → oscillator mass ~{F_din/(omega_b**2*stroke/2):.0f} kg
     That's a {F_din/(omega_b**2*stroke/2)/m_osc:.0f}× heavier device than Tesla described.

  5. WHAT PROBABLY HAPPENED:
     ✓ Tesla's oscillator excited local structural elements
     ✓ Floor joists, pipes, and loose objects vibrated audibly
     ✓ The effect was startling but not structurally dangerous
     ✗ The story grew significantly in 37 years of retelling
     ✗ "Split the Earth" is pure hyperbole

  ⚡ KEY INSIGHT: Resonance is real and powerful, but conservation
     of energy applies. A 5 lb oscillator contains limited energy
     per cycle. No amount of resonance creates energy from nothing —
     it only concentrates what's already there.

  🏷️  Could Tesla's device have exceeded modern vibration standards?
     For a whole building: NO (needs {F_needed/F_osc_at_resonance:.0f}× more force)
     For local elements: YES (floor joists, windows at risk)
     Police investigation: PLAUSIBLE (rattling + noise = complaints)

  References:
  - DIN 4150-3:1999, BS 7385-2:1993
  - Chopra, "Dynamics of Structures" (Pearson, 2017)
  - Miner, "Cumulative Damage in Fatigue" (1945)
  - Seifer, "Wizard: Life and Times of Nikola Tesla" (1996)
""")
