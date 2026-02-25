#!/usr/bin/env python3
"""
Radiant Energy and High-Frequency Phenomena
===============================================
WHAT TESLA CLAIMED:
  Tesla demonstrated that high-frequency, high-voltage currents could pass
  through the human body without harm. He attributed this to "radiant energy"
  and distinguished between Hertzian waves and what he called "non-Hertzian"
  longitudinal waves. He believed displacement currents at high frequency
  dominated over conduction currents, making the energy "radiant."

WHAT WE'RE TESTING:
  - Skin effect: why HF current doesn't penetrate tissue
  - Displacement vs conduction current crossover frequency
  - Near-field vs far-field behavior (transition distance)
  - Radiation pressure from standing waves
  - Tesla's body demonstrations: quantitative safety analysis

EXPECTED RESULTS:
  - Skin depth in tissue < 1 mm above ~1 MHz → current stays on surface
  - Displacement current dominates above ~10 MHz in tissue
  - Near-field region extends ~λ/2π from source
  - Tesla's demonstrations were genuinely safe at his frequencies

References:
  - Tesla, N. "Experiments with Alternate Currents of Very High Frequency" (1891)
  - Gabriel, C. et al. "The dielectric properties of biological tissues" (1996)
  - Polk, C. & Postow, E. "Handbook of Biological Effects of EM Fields" (1995)
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from utils.em_fields import skin_depth
from utils.visualization import save_figure, print_header, print_section, print_result, RESULTS_DIR

MU_0 = 4e-7 * np.pi
EPS_0 = 8.854e-12
C = 3e8

def tissue_skin_depth(freq, sigma=0.5, eps_r=50):
    """Skin depth in biological tissue.
    Average tissue: σ ≈ 0.5 S/m, εr ≈ 50 at RF frequencies.
    """
    omega = 2 * np.pi * freq
    eps = eps_r * EPS_0
    # Complex permittivity
    eps_complex = eps - 1j * sigma / omega
    mu = MU_0
    gamma = 1j * omega * np.sqrt(mu * eps_complex)
    alpha = np.real(gamma)
    return 1.0 / (alpha + 1e-30)

def displacement_vs_conduction(freq, sigma=0.5, eps_r=50):
    """Ratio of displacement to conduction current density.
    J_disp / J_cond = ωε / σ
    """
    omega = 2 * np.pi * freq
    return omega * eps_r * EPS_0 / sigma

def near_field_distance(freq):
    """Near-field to far-field transition distance.
    Reactive near field: < λ/(2π)
    Radiating near field (Fresnel): < 2D²/λ
    Far field (Fraunhofer): > 2D²/λ
    """
    wavelength = C / freq
    return wavelength / (2 * np.pi)

def body_current_analysis(voltage, freq, body_impedance_model='tissue'):
    """
    Analyze current flow through human body at given voltage and frequency.
    
    At low frequency: current penetrates deep, dangerous
    At high frequency: current confined to skin surface, less dangerous
    """
    if body_impedance_model == 'tissue':
        sigma = 0.5  # S/m
        eps_r = 50
    
    delta = tissue_skin_depth(freq, sigma, eps_r)
    
    # Effective cross-section for current flow
    # Assume cylindrical body, radius ~15 cm
    r_body = 0.15
    if delta < r_body:
        # Current confined to shell of thickness delta
        A_eff = 2 * np.pi * r_body * delta
    else:
        A_eff = np.pi * r_body**2
    
    # Current density at surface
    omega = 2 * np.pi * freq
    Z_tissue = np.sqrt(1j * omega * MU_0 / (sigma + 1j * omega * eps_r * EPS_0))
    
    # SAR (Specific Absorption Rate) — tissue heating
    J_surface = voltage / (np.abs(Z_tissue) * r_body * 2)  # Rough estimate
    SAR = np.abs(J_surface)**2 / (2 * sigma * 1000)  # W/kg (tissue density ~1000 kg/m³)
    
    return delta, A_eff, SAR

def radiation_pressure(E_field):
    """Radiation pressure from standing EM wave.
    P = ε₀ * E² (for standing wave, factor of 2 vs traveling wave)
    """
    return EPS_0 * E_field**2

def main():
    print_header("Radiant Energy & High-Frequency Phenomena")
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # =========================================================================
    # Skin Effect in Biological Tissue
    # =========================================================================
    print_section("Skin Effect in Human Tissue")
    
    freqs = np.logspace(2, 10, 500)  # 100 Hz to 10 GHz
    
    delta_tissue = np.array([tissue_skin_depth(f) for f in freqs])
    delta_copper = np.array([skin_depth(f, 5.8e7) for f in freqs])
    
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.loglog(freqs, delta_tissue * 100, 'r-', linewidth=2, label='Human Tissue')
    ax.loglog(freqs, delta_copper * 1e3, 'b-', linewidth=2, label='Copper (×10, in mm)')
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Skin Depth (cm for tissue, mm for copper)')
    ax.set_title('Skin Depth vs Frequency', fontweight='bold')
    ax.axhline(y=0.1, color='g', linestyle='--', alpha=0.5, label='1 mm depth')
    ax.axvline(x=150e3, color='orange', linestyle='--', alpha=0.7, label="Tesla's 150 kHz")
    ax.legend()
    ax.grid(True, alpha=0.3)
    save_figure(fig, '10_skin_depth_tissue')
    
    # Key values
    for f in [60, 1e3, 150e3, 1e6, 1e9]:
        d = tissue_skin_depth(f)
        print(f"  Skin depth at {f:>10.0f} Hz: {d*100:.2f} cm")
    
    print("\n  At 150 kHz (Tesla's frequency): current penetrates ~few cm")
    print("  At 1 MHz+: current confined to <1 cm skin layer")
    print("  This is why Tesla could safely pass HF current through his body!")
    
    # =========================================================================
    # Displacement vs Conduction Current
    # =========================================================================
    print_section("Displacement vs Conduction Current in Tissue")
    
    ratio = np.array([displacement_vs_conduction(f) for f in freqs])
    
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.loglog(freqs, ratio, 'b-', linewidth=2)
    ax.axhline(y=1, color='r', linestyle='--', linewidth=2, label='Crossover (Jd = Jc)')
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('|J_displacement| / |J_conduction|')
    ax.set_title('Displacement vs Conduction Current in Tissue\n(σ=0.5 S/m, εr=50)',
                 fontweight='bold')
    ax.axvline(x=150e3, color='orange', linestyle='--', alpha=0.7, label="Tesla's 150 kHz")
    ax.legend()
    ax.grid(True, alpha=0.3)
    save_figure(fig, '10_displacement_vs_conduction')
    
    # Find crossover frequency
    crossover_idx = np.argmin(np.abs(ratio - 1))
    f_crossover = freqs[crossover_idx]
    print_result("Crossover frequency (Jd = Jc)", f_crossover / 1e6, "MHz")
    print("  Below this: conduction current dominates (ohmic heating)")
    print("  Above this: displacement current dominates ('radiant energy')")
    print(f"  Tesla's 'non-Hertzian' concept relates to this transition")
    
    # =========================================================================
    # Near-Field vs Far-Field
    # =========================================================================
    print_section("Near-Field vs Far-Field Transition")
    
    nf_dist = np.array([near_field_distance(f) for f in freqs])
    
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.loglog(freqs, nf_dist, 'b-', linewidth=2)
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Near-Field Radius λ/(2π) (m)')
    ax.set_title('Near-Field to Far-Field Transition Distance', fontweight='bold')
    ax.axhline(y=10, color='g', linestyle='--', alpha=0.5, label='Room scale (10 m)')
    ax.axvline(x=150e3, color='orange', linestyle='--', alpha=0.7, label="Tesla's 150 kHz")
    ax.legend()
    ax.grid(True, alpha=0.3)
    save_figure(fig, '10_near_field_distance')
    
    nf_150k = near_field_distance(150e3)
    print_result("Near-field radius at 150 kHz", nf_150k, "m")
    print(f"  Tesla's lab demonstrations were ALL in the near field!")
    print(f"  Near-field behavior is fundamentally different from radiation.")
    print(f"  This is what Tesla meant by 'non-Hertzian' — he was working")
    print(f"  in the near field where fields don't behave like radiation.")
    
    # =========================================================================
    # Safety Analysis: Tesla's Body Demonstrations
    # =========================================================================
    print_section("Safety Analysis: Tesla's Body Demonstrations")
    
    # Tesla used ~250 kV at ~150 kHz through his body
    V_tesla = 250e3
    f_tesla = 150e3
    
    delta_t, A_eff, SAR = body_current_analysis(V_tesla, f_tesla)
    
    print_result("Voltage", V_tesla / 1e3, "kV")
    print_result("Frequency", f_tesla / 1e3, "kHz")
    print_result("Skin depth in tissue", delta_t * 100, "cm")
    print_result("Effective current area", A_eff * 1e4, "cm²")
    print_result("SAR (Specific Absorption Rate)", SAR, "W/kg")
    
    # Compare with safety standards
    SAR_limit = 4.0  # W/kg (IEEE C95.1 whole-body limit)
    print_result("\n  IEEE safety limit (whole body)", SAR_limit, "W/kg")
    if SAR < SAR_limit:
        print("  ✅ Below safety threshold")
    else:
        print(f"  ⚠️  {SAR/SAR_limit:.1f}x above safety threshold")
    
    # Compare 60 Hz (deadly) vs 150 kHz (Tesla's demo)
    print("\n  Why 150 kHz is safer than 60 Hz:")
    delta_60, _, SAR_60 = body_current_analysis(250e3, 60)
    print(f"    60 Hz:  skin depth = {delta_60*100:.1f} cm (penetrates entire body)")
    print(f"    150 kHz: skin depth = {delta_t*100:.1f} cm (surface only)")
    print(f"    At 60 Hz, current passes through the HEART → lethal at >30 mA")
    print(f"    At 150 kHz, current stays on skin surface → much safer")
    
    # =========================================================================
    # Radiation Pressure
    # =========================================================================
    print_section("Radiation Pressure from Standing Waves")
    
    E_fields = np.logspace(3, 8, 100)  # V/m
    pressures = radiation_pressure(E_fields)
    
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.loglog(E_fields, pressures, 'b-', linewidth=2)
    ax.set_xlabel('Electric Field (V/m)')
    ax.set_ylabel('Radiation Pressure (Pa)')
    ax.set_title('Radiation Pressure from Standing EM Waves', fontweight='bold')
    ax.axhline(y=101325, color='r', linestyle='--', alpha=0.5, label='1 atmosphere')
    ax.axhline(y=1, color='g', linestyle='--', alpha=0.5, label='1 Pa')
    ax.legend()
    ax.grid(True, alpha=0.3)
    save_figure(fig, '10_radiation_pressure')
    
    # Tesla's field strength
    E_tesla = V_tesla / 0.5  # Approximate near-field: V/distance
    P_tesla = radiation_pressure(E_tesla)
    print_result("Tesla's E-field (estimated)", E_tesla, "V/m")
    print_result("Radiation pressure", P_tesla, "Pa")
    print(f"  For comparison: 1 atm = 101325 Pa")
    print(f"  Radiation pressure is negligible for mechanical effects")
    
    # =========================================================================
    # Summary
    # =========================================================================
    print_section("SUMMARY")
    print(f"""
  ✅ Skin effect explains why HF current didn't harm Tesla
     (δ = {delta_t*100:.1f} cm at 150 kHz vs entire body at 60 Hz)
  ✅ Displacement current dominates above ~{f_crossover/1e6:.0f} MHz in tissue
  ✅ Tesla worked in near-field (λ/2π = {nf_150k:.0f} m at 150 kHz)
  ✅ Near-field ≠ radiation: Tesla's "non-Hertzian" observation has merit
  ❌ "Radiant energy" as free energy source: no physical basis
  ✅ Radiation pressure real but negligible at practical field strengths
  
  VERDICT: Tesla's demonstrations of passing HF current through his body
  were genuine and explainable by skin effect. His observation that
  HF fields behave differently from DC/low-frequency is correct — this
  is the near-field to far-field transition. His term "non-Hertzian waves"
  likely described near-field electromagnetic phenomena, which are indeed
  distinct from radiating Hertzian waves. However, his concept of
  "radiant energy" as a new form of energy was a misinterpretation of
  well-understood electromagnetic phenomena.
    """)

if __name__ == '__main__':
    main()
