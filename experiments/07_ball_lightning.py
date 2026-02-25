#!/usr/bin/env python3
"""
Ball Lightning Simulation
============================
WHAT TESLA CLAIMED:
  Tesla reported producing luminous spheres ("fireballs") in his laboratory
  using high-frequency, high-voltage discharges. At Colorado Springs with
  ~12 MV at ~150 kHz, he observed self-sustaining luminous spheres that
  persisted for seconds. He believed these were related to his resonant
  transformer's ability to create standing electromagnetic waves.

WHAT WE'RE TESTING:
  - EM standing waves in a spherical cavity (could they confine plasma?)
  - Energy requirements for sustained plasma spheres
  - Multiple theoretical models for ball lightning
  - Tesla's specific conditions: feasibility analysis

EXPECTED RESULTS:
  - EM cavity modes exist but don't naturally confine plasma
  - Energy dissipation (bremsstrahlung + conduction) is very fast
  - Tesla's parameters could produce transient plasma spheres
  - No single theory fully explains ball lightning

References:
  - Tesla, N. "Colorado Springs Notes" (1899)
  - Abrahamson, J. & Dinniss, J. "Ball lightning caused by oxidation of nanoparticle networks" (2000)
  - Ohtsuki, Y.H. & Ofuruton, H. "Reproduction of ball lightning" (1991)
  - Kapitsa, P.L. "On the Nature of Ball Lightning" (1955)
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from utils.plasma import (plasma_frequency, debye_length, plasma_sphere_energy,
                          bremsstrahlung_power_density)
from utils.visualization import save_figure, print_header, print_section, print_result, RESULTS_DIR

C_LIGHT = 3e8
EPS_0 = 8.854e-12
K_B = 1.381e-23
E_CHARGE = 1.602e-19

def em_sphere_resonances(radius, n_modes=5):
    """
    EM resonant frequencies for spherical cavity.
    TM modes: f_nl = x_nl * c / (2π * a)
    where x_nl are zeros of j_n(x) (spherical Bessel functions).
    
    Approximate zeros for first few modes:
    """
    # Known zeros of spherical Bessel functions j_n(x)
    # j_0: π, 2π, 3π, ...
    # j_1: 4.493, 7.725, 10.90, ...
    # j_2: 5.763, 9.095, 12.32, ...
    zeros = {
        0: [np.pi, 2*np.pi, 3*np.pi],
        1: [4.493, 7.725, 10.904],
        2: [5.763, 9.095, 12.323],
        3: [6.988, 10.417, 13.698],
        4: [8.183, 11.705, 15.040],
    }
    
    modes = []
    for n in range(min(n_modes, 5)):
        for l, x_nl in enumerate(zeros[n]):
            freq = x_nl * C_LIGHT / (2 * np.pi * radius)
            modes.append((n, l + 1, freq))
    
    return sorted(modes, key=lambda x: x[2])

def plasma_lifetime(radius, T_e, n_e, n_neutral=2.5e25):
    """
    Estimate plasma sphere lifetime based on energy balance.
    
    Energy in: none (self-sustaining after formation)
    Energy out: bremsstrahlung + thermal conduction + recombination
    
    Returns lifetime in seconds.
    """
    V = (4/3) * np.pi * radius**3
    A = 4 * np.pi * radius**2
    
    # Total thermal energy
    E_thermal = plasma_sphere_energy(radius, T_e, n_e)
    
    # Bremsstrahlung power loss
    P_brem = bremsstrahlung_power_density(n_e, T_e) * V
    
    # Thermal conduction loss (simplified)
    # P_cond = κ · A · ΔT / L, where κ ~ n_e * k_B * v_th * λ_mfp
    v_th = np.sqrt(K_B * T_e / (9.109e-31))
    lambda_mfp = 1e-4  # Mean free path in dense plasma (~0.1 mm)
    kappa = n_e * K_B * v_th * lambda_mfp / 3
    P_cond = kappa * A * T_e / radius
    
    # Recombination loss
    alpha_recomb = 2e-13 * (T_e / 300)**(-0.7)  # m³/s (radiative recombination)
    P_recomb = alpha_recomb * n_e**2 * V * (13.6 * E_CHARGE)  # Ionization energy per recombination
    
    P_total = P_brem + P_cond + P_recomb
    
    lifetime = E_thermal / P_total if P_total > 0 else 0
    
    return lifetime, {'brem': P_brem, 'cond': P_cond, 'recomb': P_recomb, 'total': P_total, 'energy': E_thermal}

def main():
    print_header("Ball Lightning")
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # =========================================================================
    # EM Cavity Modes
    # =========================================================================
    print_section("EM Standing Waves in Spherical Cavity")
    
    radii = [0.05, 0.10, 0.20, 0.50]  # 5 cm to 50 cm
    
    print("\n  Radius (cm) | Lowest TM Mode (GHz) | Wavelength (cm)")
    print("  " + "-" * 55)
    for r in radii:
        modes = em_sphere_resonances(r)
        f_low = modes[0][2]
        lam = C_LIGHT / f_low * 100
        print(f"  {r*100:>10.0f}   | {f_low/1e9:>19.2f}  | {lam:>14.1f}")
    
    print("\n  Note: For a 10 cm sphere, lowest mode is ~1.5 GHz (microwave)")
    print("  Tesla's 150 kHz is WAY below cavity resonance for any reasonable size")
    print("  → EM cavity confinement is NOT the mechanism")
    
    # =========================================================================
    # Plasma Sphere Energy & Lifetime
    # =========================================================================
    print_section("Plasma Sphere Energy Balance")
    
    # Parameter sweep: temperature and density
    T_range = np.logspace(3, 5, 50)  # 1,000 to 100,000 K
    n_range = np.logspace(18, 23, 50)  # Electron density
    radius_bl = 0.10  # 10 cm ball lightning
    
    # Lifetime map
    lifetimes = np.zeros((len(T_range), len(n_range)))
    for i, T in enumerate(T_range):
        for j, n_e in enumerate(n_range):
            lt, _ = plasma_lifetime(radius_bl, T, n_e)
            lifetimes[i, j] = lt
    
    fig, ax = plt.subplots(figsize=(10, 7))
    T_grid, N_grid = np.meshgrid(n_range, T_range)
    cs = ax.contourf(np.log10(T_grid), np.log10(N_grid), np.log10(lifetimes + 1e-30),
                     levels=np.linspace(-10, 2, 25), cmap='plasma')
    cbar = fig.colorbar(cs, label='log₁₀(Lifetime / s)')
    ax.set_xlabel('log₁₀(Electron Density / m⁻³)')
    ax.set_ylabel('log₁₀(Temperature / K)')
    ax.set_title('Ball Lightning Lifetime (10 cm radius)\nParameter Space', fontweight='bold')
    
    # Mark observed ball lightning region
    ax.axhline(y=np.log10(5000), color='w', linestyle='--', alpha=0.5)
    ax.text(19, np.log10(5000) + 0.1, 'Observed BL temp ~5000 K', color='white', fontsize=10)
    
    save_figure(fig, '07_ball_lightning_lifetime')
    
    # Specific case: Tesla's conditions
    print_section("Tesla's Conditions")
    T_tesla = 10000  # K
    n_e_tesla = 1e21  # m^-3
    lt_tesla, losses = plasma_lifetime(radius_bl, T_tesla, n_e_tesla)
    
    print_result("Plasma temperature", T_tesla, "K")
    print_result("Electron density", n_e_tesla, "m⁻³")
    print_result("Thermal energy", losses['energy'], "J")
    print_result("Bremsstrahlung loss", losses['brem'], "W")
    print_result("Conduction loss", losses['cond'], "W")
    print_result("Recombination loss", losses['recomb'], "W")
    print_result("Total power loss", losses['total'], "W")
    print_result("Estimated lifetime", lt_tesla * 1e3, "ms")
    print(f"  Observed ball lightning: 1-10 seconds")
    print(f"  Pure plasma model gives: {lt_tesla*1e3:.1f} ms — too short!")
    
    # =========================================================================
    # Competing Theories Comparison
    # =========================================================================
    print_section("Competing Theories for Ball Lightning")
    
    theories = {
        'Kapitsa (1955)': {
            'mechanism': 'External microwave standing waves maintain plasma',
            'energy_source': 'Atmospheric microwave radiation',
            'lifetime': 'Continuous while source exists',
            'problems': 'No known natural microwave source of sufficient power'
        },
        'Abrahamson-Dinniss (2000)': {
            'mechanism': 'Oxidizing silicon nanoparticle network from lightning strike on soil',
            'energy_source': 'Chemical (Si + O₂ → SiO₂)',
            'lifetime': '1-10 s (matches observations)',
            'problems': 'Indoor ball lightning, no soil contact'
        },
        'Ohtsuki-Ofuruton (1991)': {
            'mechanism': 'Microwave-heated fireball in lab',
            'energy_source': 'External microwave 2.45 GHz',
            'lifetime': '1-2 s after microwave off',
            'problems': 'Requires external energy source'
        },
        'Tesla (1899)': {
            'mechanism': 'HF resonant transformer creates standing waves',
            'energy_source': 'Coupled resonant circuit at 150 kHz',
            'lifetime': 'Seconds (per Tesla\'s notes)',
            'problems': '150 kHz too low for EM cavity confinement'
        }
    }
    
    for name, theory in theories.items():
        print(f"\n  {name}:")
        for k, v in theory.items():
            print(f"    {k}: {v}")
    
    # =========================================================================
    # Energy vs Radius
    # =========================================================================
    print_section("Energy Content vs Ball Lightning Radius")
    
    radii_sweep = np.linspace(0.01, 0.5, 100)
    energies_plasma = [plasma_sphere_energy(r, 10000, 1e21) for r in radii_sweep]
    energies_chemical = [(4/3) * np.pi * r**3 * 1e7 for r in radii_sweep]  # ~10 MJ/m³ chemical
    
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.semilogy(radii_sweep * 100, energies_plasma, 'b-', linewidth=2, label='Pure Plasma (10⁴ K, 10²¹ m⁻³)')
    ax.semilogy(radii_sweep * 100, energies_chemical, 'r-', linewidth=2, label='Chemical (Si nanoparticles)')
    ax.set_xlabel('Ball Lightning Radius (cm)')
    ax.set_ylabel('Energy Content (J)')
    ax.set_title('Ball Lightning Energy Content', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Observed range
    ax.axhspan(1e3, 1e6, alpha=0.1, color='green', label='Observed range (est.)')
    ax.legend()
    save_figure(fig, '07_ball_lightning_energy')
    
    # =========================================================================
    # Summary
    # =========================================================================
    print_section("SUMMARY")
    print(f"""
  ✅ Tesla did produce luminous plasma spheres in his lab
  ✅ High-voltage, high-frequency discharges CAN create transient fireballs
  ❌ EM cavity confinement doesn't work at 150 kHz (wavelength >> sphere)
  ❌ Pure plasma model gives lifetime ~{lt_tesla*1e3:.0f} ms (observed: 1-10 s)
  ⚠️  Chemical energy (nanoparticle oxidation) better explains long lifetimes
  
  VERDICT: Tesla almost certainly produced real plasma phenomena, but
  his understanding of the mechanism was incomplete. Ball lightning
  remains one of the least understood atmospheric phenomena. The
  Abrahamson-Dinniss chemical model currently best explains observed
  lifetimes, but no single theory is fully satisfactory. Tesla's
  observations were genuine and scientifically valuable.
    """)

if __name__ == '__main__':
    main()
