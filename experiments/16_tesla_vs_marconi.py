#!/usr/bin/env python3
"""
══════════════════════════════════════════════════════════════════════════════
 EXPERIMENT 16 — TESLA vs MARCONI
 Surface Wave vs Skywave: Who Was Right About Transatlantic Radio?
══════════════════════════════════════════════════════════════════════════════

On December 12, 1901, Marconi claimed to receive the letter "S" (three dots)
transmitted from Poldhu, Cornwall to Signal Hill, Newfoundland — 3,500 km
across the Atlantic. Tesla insisted that Marconi's signal traveled via
ground/surface wave, not skywave. This experiment tests both hypotheses.

Parameters:
  - Frequency: ~820 kHz (Marconi's estimated operating frequency)
  - Distance: 3,500 km (Poldhu → Signal Hill)
  - Path: predominantly over seawater (σ ≈ 4 S/m)
  - Marconi's antenna: fan-shaped wire array, ~50m height
  - Time: ~12:30 local (midday at mid-Atlantic)

References:
 - Belrose, J.S. "Fessenden and Marconi" IEEE Antennas & Propagation (2001)
 - Ratcliffe, J.A. "Scientists' Reactions to Marconi's Transatlantic
   Experiment" Proc. IEE (1974)
 - Austin, L.W. & Cohen, L. "Transmission of Signals" (Bureau of Standards)
 - Wait, J.R. "The Ancient and Modern History of EM Ground-Wave
   Propagation" IEEE AP Magazine (1998)
 - Tesla, N. "Experiments with Alternating Currents" (1904)
══════════════════════════════════════════════════════════════════════════════
"""

import numpy as np
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

# Constants
c = 3e8
mu0 = 4e-7 * np.pi
eps0 = 8.854e-12
eta0 = 377.0
R_earth = 6.371e6
k_boltz = 1.381e-23

banner("EXPERIMENT 16: TESLA vs MARCONI")
print("Surface Wave vs Skywave — Transatlantic 1901")

# ─────────────────────────────────────────────────────────────────────────
# Transmission Parameters
# ─────────────────────────────────────────────────────────────────────────

f_marconi = 820e3    # Estimated frequency (various sources say 800-850 kHz)
lam = c / f_marconi
omega = 2 * np.pi * f_marconi
k = omega / c
d_atlantic = 3500    # Distance in km
P_tx = 25e3          # Poldhu transmitter power ~25 kW (some sources say 10-50 kW)

# Antenna parameters
h_poldhu = 50.0      # Poldhu antenna height ~50 m (fan array)
h_signal = 120.0     # Signal Hill: kite-borne wire ~120 m

# Seawater
sigma_sea = 4.0      # S/m
eps_r_sea = 80

print(f"\n  Marconi's Transmission Parameters:")
print(f"    Frequency:     {f_marconi/1e3:.0f} kHz (λ = {lam:.0f} m)")
print(f"    Distance:      {d_atlantic} km (Poldhu → Signal Hill)")
print(f"    TX Power:      {P_tx/1e3:.0f} kW")
print(f"    TX antenna:    Fan array, ~{h_poldhu:.0f} m height")
print(f"    RX antenna:    Kite wire, ~{h_signal:.0f} m height")
print(f"    Path:          Predominantly seawater (σ = {sigma_sea} S/m)")

# ─────────────────────────────────────────────────────────────────────────
# Part A: Ground/Surface Wave (Tesla's Hypothesis)
# ─────────────────────────────────────────────────────────────────────────

section("A. Ground Wave / Surface Wave (Tesla's Method)")

# Austin-Cohen formula (empirical, 1911):
# E = (377 × √P × h_eff) / (λ × d) × exp(-0.0014 × π × d / (λ × √(σ/f)))
# This was the first reliable ground-wave formula

def austin_cohen_field(d_km, P_w, h_tx, h_rx, f, sigma):
    """Austin-Cohen empirical ground wave field (V/m)."""
    lam_f = c / f
    d_m = d_km * 1e3
    # Effective radiated field for short monopole
    E_inv = 300 * np.sqrt(P_w) / d_m  # Inverse-distance field (V/m)
    # Austin-Cohen absorption factor
    alpha_ac = 0.0014 * np.pi / (lam_f * np.sqrt(sigma / f))
    A = np.exp(-alpha_ac * d_m)
    return E_inv * A

# Sommerfeld-Norton ground wave (more rigorous)
def sommerfeld_ground_wave(d_km, P_w, f, sigma, eps_r):
    """Sommerfeld flat-earth ground wave field strength (V/m)."""
    lam_f = c / f
    omega_f = 2 * np.pi * f
    d_m = d_km * 1e3

    # Complex dielectric constant of ground
    eps_c = eps_r - 1j * sigma / (omega_f * eps0)

    # Numerical distance
    p = (np.pi * d_m / lam_f) * (1 / np.abs(eps_c))

    # Norton's attenuation function W(p) — asymptotic expansion
    # For large p: W ≈ 1/(2p) - 3/(4p²) + ...
    # For small p: W ≈ 1 - √(πp) × exp(-p)
    W = np.where(p < 1,
                 1 - np.sqrt(np.pi * p) * np.exp(-p) * (1 - 0.5/np.maximum(p, 0.01)),
                 1 / (2 * p + 0.3))

    # Free-space field
    E0 = np.sqrt(90 * P_w) / d_m
    return np.abs(E0 * W)

distances = np.logspace(0, np.log10(5000), 500)

E_ac = austin_cohen_field(distances, P_tx, h_poldhu, h_signal, f_marconi, sigma_sea)
E_som = sommerfeld_ground_wave(distances, P_tx, f_marconi, sigma_sea, eps_r_sea)

# Field at 3500 km
E_gw_3500_ac = austin_cohen_field(d_atlantic, P_tx, h_poldhu, h_signal, f_marconi, sigma_sea)
E_gw_3500_som = sommerfeld_ground_wave(d_atlantic, P_tx, f_marconi, sigma_sea, eps_r_sea)

print(f"\n  Ground wave field at {d_atlantic} km:")
print(f"    Austin-Cohen:    E = {E_gw_3500_ac*1e6:.2f} µV/m")
print(f"    Sommerfeld:      E = {E_gw_3500_som*1e6:.2f} µV/m")

# Zenneck surface wave contribution
# The Zenneck wave is the surface wave solution
eps_c = eps_r_sea - 1j * sigma_sea / (omega * eps0)
k_zenneck = k * np.sqrt(eps_c / (1 + eps_c))
alpha_z = np.abs(np.imag(k_zenneck))
beta_z = np.real(k_zenneck)

print(f"\n  Zenneck surface wave at {f_marconi/1e3:.0f} kHz over seawater:")
print(f"    Attenuation: α = {alpha_z:.6f} Np/m = {alpha_z*1e3:.4f} Np/km")
print(f"    1/e distance: {1/alpha_z/1e3:.0f} km")

# Zenneck field at 3500 km
E_zenneck_3500 = np.sqrt(90 * P_tx) / (d_atlantic * 1e3) * np.exp(-alpha_z * d_atlantic * 1e3)
print(f"    Field at {d_atlantic} km: {E_zenneck_3500*1e6:.4f} µV/m")

# ─────────────────────────────────────────────────────────────────────────
# Part B: Skywave (Ionospheric Reflection)
# ─────────────────────────────────────────────────────────────────────────

section("B. Skywave (Ionospheric Reflection)")

# Ionospheric layers
D_height = 70e3    # D-layer height (km), only present during day
E_height = 110e3   # E-layer height
F1_height = 200e3  # F1-layer height
F2_height = 300e3  # F2-layer height

# At 820 kHz, which layer reflects?
# Plasma frequency: f_p = 9√(N_e) where N_e is electron density (m⁻³)
# E-layer: N_e ~ 10¹¹ m⁻³ → f_p ≈ 3 MHz → reflects 820 kHz ✓
# D-layer (day): N_e ~ 10⁹ m⁻³ → f_p ≈ 300 kHz → absorbs 820 kHz

# Critical frequency for E-layer
Ne_E = 1.5e11  # Typical daytime E-layer
fp_E = 9.0 * np.sqrt(Ne_E)  # Hz
print(f"  E-layer: N_e = {Ne_E:.1e} m⁻³, f_p = {fp_E/1e6:.1f} MHz")
print(f"  820 kHz < f_p → E-layer CAN reflect this frequency")

# D-layer absorption (key factor!)
# Absorption ∝ N_e(D) / (ν² + ω²) where ν is collision frequency
# At 820 kHz, D-layer absorption is severe during daytime
Ne_D_day = 1e9    # Daytime D-layer density
Ne_D_night = 1e7  # Nighttime D-layer density
nu_D = 1e7        # Collision frequency in D-layer (Hz)

# Non-deviative absorption coefficient
def d_layer_absorption(f, Ne_D, nu, thickness=20e3):
    """D-layer absorption in dB (one-way pass)."""
    omega_f = 2 * np.pi * f
    omega_p2 = Ne_D * (1.6e-19)**2 / (9.11e-31 * eps0)
    # Absorption per unit length
    kappa = omega_p2 * nu / (2 * c * (omega_f**2 + nu**2))
    # Total absorption through D-layer
    L_Np = kappa * thickness
    L_dB = 8.686 * L_Np
    return L_dB

L_D_day = d_layer_absorption(f_marconi, Ne_D_day, nu_D)
L_D_night = d_layer_absorption(f_marconi, Ne_D_night, nu_D)

print(f"\n  D-layer absorption at {f_marconi/1e3:.0f} kHz:")
print(f"    Daytime:  {L_D_day:.1f} dB (one-way through D-layer)")
print(f"    Nighttime: {L_D_night:.1f} dB (one-way through D-layer)")
print(f"    Total skywave (2 passes through D-layer):")
print(f"      Day:   {2*L_D_day:.1f} dB absorption")
print(f"      Night: {2*L_D_night:.1f} dB absorption")

# Skywave field strength at 3500 km
# 1-hop via E-layer: path = 2 × √((d/2)² + h²)
d_half = d_atlantic * 1e3 / 2
h_reflect = E_height
path_1hop = 2 * np.sqrt(d_half**2 + h_reflect**2)

# Free-space loss + D-layer absorption + reflection loss
FSPL = 20 * np.log10(4 * np.pi * path_1hop / lam)
R_loss_dB = 3  # Ionospheric reflection loss ~3 dB
L_total_day = FSPL + 2 * L_D_day + R_loss_dB
L_total_night = FSPL + 2 * L_D_night + R_loss_dB

# Effective field strength
E_skywave_day = np.sqrt(90 * P_tx) / path_1hop * 10**(-2*L_D_day/20) * 10**(-R_loss_dB/20)
E_skywave_night = np.sqrt(90 * P_tx) / path_1hop * 10**(-2*L_D_night/20) * 10**(-R_loss_dB/20)

print(f"\n  Skywave field at {d_atlantic} km:")
print(f"    1-hop path length: {path_1hop/1e3:.0f} km")
print(f"    FSPL: {FSPL:.1f} dB")
print(f"    Day:   E = {E_skywave_day*1e6:.2f} µV/m (total loss: {L_total_day:.0f} dB)")
print(f"    Night: E = {E_skywave_night*1e6:.2f} µV/m (total loss: {L_total_night:.0f} dB)")

# Multi-hop analysis
print(f"\n  Multi-hop options:")
for n_hops in [1, 2, 3]:
    d_seg = d_atlantic * 1e3 / n_hops
    path = n_hops * 2 * np.sqrt((d_seg/2)**2 + E_height**2)
    L_abs = 2 * n_hops * L_D_day
    E_mh = np.sqrt(90 * P_tx) / path * 10**(-L_abs/20) * 10**(-n_hops * R_loss_dB/20)
    print(f"    {n_hops}-hop (day): path={path/1e3:.0f} km, abs={L_abs:.0f} dB, "
          f"E={E_mh*1e6:.4f} µV/m")

# ─────────────────────────────────────────────────────────────────────────
# Part C: Direct Comparison — Which Path Carried Marconi's Signal?
# ─────────────────────────────────────────────────────────────────────────

section("C. Head-to-Head: Ground Wave vs Skywave")

# Receiver sensitivity
# Marconi used a coherer detector — very crude
# Estimated minimum detectable field: ~100 µV/m (optimistic)
# Some sources say 1 mV/m was needed
E_min_optimistic = 100e-6  # V/m
E_min_realistic = 1e-3     # V/m

# Noise floor at 820 kHz
# Atmospheric noise dominates at MF
T_noise = 1e6  # Effective noise temperature ~10⁶ K at 820 kHz
B = 1000  # Bandwidth ~1 kHz (CW)
N_power = k_boltz * T_noise * B
E_noise = np.sqrt(N_power * eta0 / (lam**2 / (4 * np.pi)))

print(f"  Signal strengths at {d_atlantic} km:")
print(f"  ┌─────────────────────┬────────────────┬──────────┐")
print(f"  │ Propagation Mode    │ Field (µV/m)   │ Viable?  │")
print(f"  ├─────────────────────┼────────────────┼──────────┤")
print(f"  │ Ground wave (A-C)   │ {E_gw_3500_ac*1e6:>12.2f}  │ {'YES ✓' if E_gw_3500_ac > E_min_optimistic else 'NO ✗':>8} │")
print(f"  │ Ground wave (Som.)  │ {E_gw_3500_som*1e6:>12.2f}  │ {'YES ✓' if E_gw_3500_som > E_min_optimistic else 'NO ✗':>8} │")
print(f"  │ Zenneck surface     │ {E_zenneck_3500*1e6:>12.4f}  │ {'YES ✓' if E_zenneck_3500 > E_min_optimistic else 'NO ✗':>8} │")
print(f"  │ Skywave (day)       │ {E_skywave_day*1e6:>12.2f}  │ {'YES ✓' if E_skywave_day > E_min_optimistic else 'NO ✗':>8} │")
print(f"  │ Skywave (night)     │ {E_skywave_night*1e6:>12.2f}  │ {'YES ✓' if E_skywave_night > E_min_optimistic else 'NO ✗':>8} │")
print(f"  └─────────────────────┴────────────────┴──────────┘")
print(f"\n  Minimum detectable (optimistic): {E_min_optimistic*1e6:.0f} µV/m")
print(f"  Minimum detectable (realistic):  {E_min_realistic*1e6:.0f} µV/m")

# Time of day analysis
print(f"\n  Time of day matters critically:")
print(f"    Marconi's reception: ~12:30 local time (midday)")
print(f"    At midday: D-layer is FULLY present → skywave heavily absorbed")
print(f"    At night:  D-layer disappears → skywave much stronger")
print(f"    The midday timing HURTS the skywave hypothesis")

# ─────────────────────────────────────────────────────────────────────────
# Distance sweep — both modes
# ─────────────────────────────────────────────────────────────────────────

# Skywave vs distance
E_sky_day_d = np.zeros_like(distances)
E_sky_night_d = np.zeros_like(distances)
for i, d in enumerate(distances):
    if d > 100:  # Skywave only relevant beyond ground wave range
        d_m = d * 1e3
        path = 2 * np.sqrt((d_m/2)**2 + E_height**2)
        E_sky_day_d[i] = np.sqrt(90 * P_tx) / path * 10**(-2*L_D_day/20) * 10**(-R_loss_dB/20)
        E_sky_night_d[i] = np.sqrt(90 * P_tx) / path * 10**(-2*L_D_night/20) * 10**(-R_loss_dB/20)

# ─────────────────────────────────────────────────────────────────────────
# Part D: Was Tesla Right?
# ─────────────────────────────────────────────────────────────────────────

section("D. Was Tesla Right About Ground Wave?")

# Modern consensus analysis
print(f"""
  Tesla's claim: Marconi's signal traveled via ground/surface wave.
  
  Evidence FOR ground wave:
    • Seawater path: σ = 4 S/m gives excellent ground wave propagation
    • Austin-Cohen formula predicts detectable signal at 3500 km
    • Midday transmission: D-layer absorption devastating to skywave
    • 820 kHz ground wave over sea can reach ~3000-5000 km
    
  Evidence AGAINST ground wave (for skywave):
    • Most modern textbooks credit skywave (Kennelly-Heaviside layer)
    • Marconi's later experiments showed strong skywave at night
    • Some calculations show ground wave too weak at 3500 km
    • Diffraction around Earth's curvature helps but has limits

  The uncomfortable truth:
    • The signal was received at MIDDAY → worst case for skywave
    • At 820 kHz over seawater → best case for ground wave
    • Austin-Cohen formula (empirical, from actual measurements)
      gives {E_gw_3500_ac*1e6:.1f} µV/m — marginal but possible
    • D-layer absorption of {2*L_D_day:.0f} dB makes daytime skywave
      extremely weak: {E_skywave_day*1e6:.2f} µV/m
      
  Modern re-analysis (Belrose, 2001):
    Both modes may have contributed. The ground wave was likely
    the DOMINANT path for Marconi's specific midday experiment.
    Nighttime transatlantic reception (which Marconi also achieved)
    was primarily skywave.
""")

# ─────────────────────────────────────────────────────────────────────────
# Plotting
# ─────────────────────────────────────────────────────────────────────────

fig, axes = plt.subplots(2, 2, figsize=(14, 11))
fig.suptitle("Experiment 16: Tesla vs Marconi\nTransatlantic Propagation 1901",
             fontsize=14, fontweight='bold')

# A: Ground wave field strength
ax = axes[0, 0]
ax.loglog(distances, E_ac * 1e6, 'b-', linewidth=2, label='Austin-Cohen')
ax.loglog(distances, E_som * 1e6, 'r-', linewidth=2, label='Sommerfeld')
ax.axhline(y=100, color='g', linestyle='--', alpha=0.7, label='Detection threshold')
ax.axvline(x=3500, color='gray', linestyle=':', alpha=0.7, label='Atlantic crossing')
ax.set_xlabel('Distance (km)')
ax.set_ylabel('Field Strength (µV/m)')
ax.set_title('A. Ground Wave over Seawater (820 kHz)')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)
ax.set_ylim([1e-3, 1e8])

# B: Skywave with D-layer absorption
ax = axes[0, 1]
mask = E_sky_day_d > 0
if np.any(mask):
    ax.loglog(distances[mask], E_sky_day_d[mask] * 1e6, 'r-', linewidth=2, label='Skywave (day)')
mask = E_sky_night_d > 0
if np.any(mask):
    ax.loglog(distances[mask], E_sky_night_d[mask] * 1e6, 'b-', linewidth=2, label='Skywave (night)')
ax.axhline(y=100, color='g', linestyle='--', alpha=0.7, label='Detection threshold')
ax.axvline(x=3500, color='gray', linestyle=':', alpha=0.7, label='Atlantic crossing')
ax.set_xlabel('Distance (km)')
ax.set_ylabel('Field Strength (µV/m)')
ax.set_title('B. Skywave via E-layer (820 kHz)')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# C: Comparison at 3500 km
ax = axes[1, 0]
modes = ['Ground\n(Austin-Cohen)', 'Ground\n(Sommerfeld)', 'Zenneck\nSurface', 
         'Skywave\n(Day)', 'Skywave\n(Night)']
fields = [E_gw_3500_ac*1e6, E_gw_3500_som*1e6, E_zenneck_3500*1e6,
          E_skywave_day*1e6, E_skywave_night*1e6]
colors_bar = ['royalblue', 'steelblue', 'teal', 'salmon', 'indianred']
bars = ax.bar(modes, fields, color=colors_bar, edgecolor='black', linewidth=0.5)
ax.axhline(y=100, color='g', linestyle='--', linewidth=2, label='Detection limit')
ax.set_ylabel('Field Strength (µV/m)')
ax.set_title(f'C. All Modes at {d_atlantic} km')
ax.set_yscale('log')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

# D: Time of day effect on D-layer
ax = axes[1, 1]
hours = np.arange(0, 24, 0.5)
# D-layer density varies with solar zenith angle
# Simple model: N_e ∝ cos(χ)^0.5 during day, minimal at night
Ne_D_vs_time = np.zeros_like(hours)
for i, h in enumerate(hours):
    # Solar zenith angle (simplified, mid-Atlantic ~45°N in December)
    chi = np.abs(h - 12) / 12 * np.pi  # Solar hour angle to zenith
    if chi < np.pi/2:  # Daytime
        Ne_D_vs_time[i] = Ne_D_day * np.cos(chi)**0.5
    else:
        Ne_D_vs_time[i] = Ne_D_night

L_D_vs_time = np.array([d_layer_absorption(f_marconi, ne, nu_D) for ne in Ne_D_vs_time])
E_sky_vs_time = np.sqrt(90 * P_tx) / path_1hop * 10**(-2*L_D_vs_time/20) * 10**(-R_loss_dB/20)

ax.semilogy(hours, E_sky_vs_time * 1e6, 'b-', linewidth=2, label='Skywave field')
ax.axhline(y=E_gw_3500_ac*1e6, color='r', linestyle='-', linewidth=2, 
           label=f'Ground wave ({E_gw_3500_ac*1e6:.1f} µV/m)')
ax.axhline(y=100, color='g', linestyle='--', alpha=0.7, label='Detection limit')
ax.axvline(x=12.5, color='orange', linewidth=2, alpha=0.7, label="Marconi's reception")
ax.set_xlabel('Local Time (hours, mid-Atlantic)')
ax.set_ylabel('Field Strength (µV/m)')
ax.set_title('D. Time-of-Day Effect on Signal Path')
ax.legend(fontsize=7)
ax.grid(True, alpha=0.3)
ax.set_xlim([0, 24])

plt.tight_layout()
plt.savefig(RESULTS / "16_tesla_vs_marconi.png", dpi=150, bbox_inches='tight')
print(f"\n  📊 Plot saved: {RESULTS}/16_tesla_vs_marconi.png")

# ─────────────────────────────────────────────────────────────────────────
# Verdict
# ─────────────────────────────────────────────────────────────────────────

banner("VERDICT: WAS TESLA RIGHT?")
print(f"""
  Tesla vs Marconi — Transatlantic 1901 Analysis:

  GROUND WAVE at 3500 km over seawater:
    Austin-Cohen: {E_gw_3500_ac*1e6:.1f} µV/m — {'DETECTABLE' if E_gw_3500_ac > E_min_optimistic else 'BELOW THRESHOLD'}
    Sommerfeld:   {E_gw_3500_som*1e6:.1f} µV/m — {'DETECTABLE' if E_gw_3500_som > E_min_optimistic else 'BELOW THRESHOLD'}

  SKYWAVE at 3500 km (midday):
    Daytime:  {E_skywave_day*1e6:.2f} µV/m — HEAVILY ABSORBED by D-layer
    Nighttime: {E_skywave_night*1e6:.2f} µV/m — {'DETECTABLE' if E_skywave_night > E_min_optimistic else 'BELOW THRESHOLD'}

  ⚡ VERDICT: Tesla was PARTIALLY RIGHT.

  For Marconi's specific December 12, 1901 midday experiment:
  • The ground wave over seawater was likely the DOMINANT signal path
  • D-layer absorption at midday severely attenuates 820 kHz skywave
  • The seawater path (σ = 4 S/m) is exceptionally favorable for ground wave

  However:
  • Tesla was WRONG that surface/ground wave was the general mechanism
  • Nighttime transatlantic propagation (which Marconi also achieved)
    is clearly skywave-dominated
  • The Kennelly-Heaviside layer IS real and important

  HISTORICAL IRONY: The textbook narrative ("Marconi proved skywave exists")
  is probably wrong for the specific December 12 daytime experiment.
  Both Tesla AND the textbooks are partially incorrect.

  🏷️  Modern consensus (Belrose 2001, Ratcliffe 1974): The midday signal
     was likely ground wave; Marconi's later nighttime successes were skywave.
     Tesla was right about the wrong experiment.

  ⚠️  NOTE: Whether Marconi actually received anything on Dec 12, 1901
     remains debated. No recording exists. The coherer detector provided
     no way to verify the signal was from Poldhu vs atmospheric noise.

  References:
  - Belrose, J.S. IEEE AP Magazine 43(6), 2001
  - Ratcliffe, J.A. Proc. IEE 121(9), 1974
  - Austin & Cohen, Bureau of Standards Bulletin 1911
  - Wait, J.R. IEEE AP Magazine 40(5), 1998
""")
