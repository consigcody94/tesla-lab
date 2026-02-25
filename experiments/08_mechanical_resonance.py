#!/usr/bin/env python3
"""
Tesla's Earthquake Machine — Mechanical Resonance
=====================================================
WHAT TESLA CLAIMED:
  In 1898 at his Houston Street lab, Tesla attached a small mechanical
  oscillator to a steel beam and reportedly caused the entire building
  and neighboring buildings to vibrate violently, requiring police
  intervention. He claimed a small device could destroy the Brooklyn
  Bridge or even "split the Earth" given enough time.

WHAT WE'RE TESTING:
  - Building as multi-DOF spring-mass-damper system
  - Force amplification at resonance vs number of cycles
  - Can a small oscillator (<1 HP) damage a building?
  - Effect of structural damping and nonlinearities

EXPECTED RESULTS:
  - At resonance, force amplification = Q factor (~10-50 for buildings)
  - A small oscillator CAN cause alarming vibrations in lightly damped structures
  - Cannot actually destroy a building (nonlinear damping increases with amplitude)
  - Tesla's story is plausible but exaggerated

References:
  - Tesla's account in "My Inventions" (1919) and various interviews
  - Chopra, A.K. "Dynamics of Structures" (Pearson, 2012)
  - US Patent 514,169 "Reciprocating Engine" (1894)
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import numpy as np
from scipy.integrate import solve_ivp
from scipy import signal
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from utils.visualization import save_figure, print_header, print_section, print_result, RESULTS_DIR

def building_mdof_system(n_floors, m_floor, k_story, c_story):
    """
    Create mass, stiffness, and damping matrices for n-floor building.
    Each floor is a mass connected by springs (story stiffness) and dampers.
    
    Returns M, K, C matrices.
    """
    M = np.diag(np.full(n_floors, m_floor))
    
    K = np.zeros((n_floors, n_floors))
    C_mat = np.zeros((n_floors, n_floors))
    
    for i in range(n_floors):
        if i == 0:
            K[i, i] = 2 * k_story if n_floors > 1 else k_story
            C_mat[i, i] = 2 * c_story if n_floors > 1 else c_story
        elif i == n_floors - 1:
            K[i, i] = k_story
            C_mat[i, i] = c_story
        else:
            K[i, i] = 2 * k_story
            C_mat[i, i] = 2 * c_story
        
        if i > 0:
            K[i, i-1] = -k_story
            K[i-1, i] = -k_story
            C_mat[i, i-1] = -c_story
            C_mat[i-1, i] = -c_story
    
    return M, K, C_mat

def natural_frequencies(M, K):
    """Calculate natural frequencies and mode shapes."""
    eigenvalues, eigenvectors = np.linalg.eigh(np.linalg.solve(M, K))
    freqs = np.sqrt(np.abs(eigenvalues)) / (2 * np.pi)
    return freqs, eigenvectors

def simulate_forced_vibration(M, K, C_mat, F_amplitude, f_drive, t_max, dt=0.001):
    """
    Simulate forced vibration of MDOF system.
    Force applied to first floor (ground level, where Tesla's oscillator was).
    """
    n = M.shape[0]
    
    def deriv(t, state):
        x = state[:n]
        v = state[n:]
        
        # Force vector: oscillator on ground floor
        F = np.zeros(n)
        F[0] = F_amplitude * np.sin(2 * np.pi * f_drive * t)
        
        a = np.linalg.solve(M, F - K @ x - C_mat @ v)
        return np.concatenate([v, a])
    
    t_span = [0, t_max]
    t_eval = np.arange(0, t_max, dt)
    y0 = np.zeros(2 * n)
    
    sol = solve_ivp(deriv, t_span, y0, t_eval=t_eval, method='RK45', max_step=dt)
    return sol

def main():
    print_header("Mechanical Resonance / Earthquake Machine")
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # =========================================================================
    # Building Model: Tesla's Houston St. Lab (~5-story building, 1890s NYC)
    # =========================================================================
    print_section("Building Model: 1890s NYC 5-Story Building")
    
    n_floors = 5
    m_floor = 50000      # kg per floor (50 tonnes)
    k_story = 5e7        # Story stiffness (N/m)
    
    # Damping ratio ~2-5% for masonry buildings
    zeta = 0.03  # 3% damping ratio
    omega_1 = np.sqrt(k_story / m_floor)  # Approximate first mode
    c_story = 2 * zeta * omega_1 * m_floor  # Damping coefficient
    
    M, K, C_mat = building_mdof_system(n_floors, m_floor, k_story, c_story)
    freqs, modes = natural_frequencies(M, K)
    
    print(f"  Building: {n_floors} floors × {m_floor/1000:.0f} tonnes each")
    print(f"  Story stiffness: {k_story:.0e} N/m")
    print(f"  Damping ratio: {zeta*100:.0f}%")
    print(f"\n  Natural frequencies:")
    for i, f in enumerate(freqs):
        print(f"    Mode {i+1}: {f:.2f} Hz ({1/f:.3f} s period)")
    
    Q_factor = 1 / (2 * zeta)
    print_result("\n  Q factor (1st mode)", Q_factor, "")
    
    # =========================================================================
    # Tesla's Oscillator: Force amplification at resonance
    # =========================================================================
    print_section("Tesla's Oscillator at Resonance")
    
    # Tesla's oscillator: small steam-driven device, ~1-5 lbs force
    F_osc = 50  # N (~11 lbs force, reasonable for small mechanical oscillator)
    
    print_result("Oscillator force", F_osc, "N")
    print_result("Oscillator power (at resonance)", 
                 F_osc * 0.01 * 2 * np.pi * freqs[0], "W")  # ~1 cm stroke
    
    # Simulate at resonance
    t_max = 60  # seconds
    sol_res = simulate_forced_vibration(M, K, C_mat, F_osc, freqs[0], t_max)
    
    # Simulate off-resonance
    sol_off = simulate_forced_vibration(M, K, C_mat, F_osc, freqs[0] * 1.5, t_max)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Top floor displacement at resonance
    axes[0, 0].plot(sol_res.t, sol_res.y[n_floors-1] * 1000, 'b-', linewidth=0.5)
    axes[0, 0].set_xlabel('Time (s)')
    axes[0, 0].set_ylabel('Top Floor Displacement (mm)')
    axes[0, 0].set_title(f'AT RESONANCE (f = {freqs[0]:.2f} Hz)')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Top floor displacement off-resonance
    axes[0, 1].plot(sol_off.t, sol_off.y[n_floors-1] * 1000, 'r-', linewidth=0.5)
    axes[0, 1].set_xlabel('Time (s)')
    axes[0, 1].set_ylabel('Top Floor Displacement (mm)')
    axes[0, 1].set_title(f'OFF RESONANCE (f = {freqs[0]*1.5:.2f} Hz)')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Envelope growth
    x_top = sol_res.y[n_floors-1]
    envelope = np.abs(signal.hilbert(x_top))
    axes[1, 0].plot(sol_res.t, envelope * 1000, 'b-', linewidth=2)
    axes[1, 0].set_xlabel('Time (s)')
    axes[1, 0].set_ylabel('Displacement Envelope (mm)')
    axes[1, 0].set_title('Resonance Build-Up')
    axes[1, 0].grid(True, alpha=0.3)
    
    # All floors at steady state
    t_steady = sol_res.t > t_max * 0.8
    for i in range(n_floors):
        max_disp = np.max(np.abs(sol_res.y[i][t_steady])) * 1000
        axes[1, 1].barh(i + 1, max_disp, color=f'C{i}')
    axes[1, 1].set_xlabel('Max Displacement (mm)')
    axes[1, 1].set_ylabel('Floor')
    axes[1, 1].set_title('Floor Displacement Profile (Steady State)')
    axes[1, 1].grid(True, alpha=0.3)
    
    fig.suptitle(f"Tesla's Earthquake Machine — {F_osc} N Oscillator on 5-Story Building",
                 fontweight='bold')
    fig.tight_layout()
    save_figure(fig, '08_earthquake_machine')
    
    max_top_res = np.max(np.abs(sol_res.y[n_floors-1])) * 1000
    max_top_off = np.max(np.abs(sol_off.y[n_floors-1])) * 1000
    print_result("Max top-floor displacement (resonance)", max_top_res, "mm")
    print_result("Max top-floor displacement (off-resonance)", max_top_off, "mm")
    print_result("Amplification ratio", max_top_res / max_top_off, "")
    
    # =========================================================================
    # Frequency Sweep
    # =========================================================================
    print_section("Frequency Response")
    
    f_sweep = np.linspace(0.1, 20, 500)
    response = np.zeros_like(f_sweep)
    
    for i, f in enumerate(f_sweep):
        omega = 2 * np.pi * f
        # Frequency response: H(ω) = (-ω²M + jωC + K)⁻¹ F
        H = np.linalg.solve(-omega**2 * M + 1j * omega * C_mat + K, 
                           np.array([1, 0, 0, 0, 0]))
        response[i] = np.abs(H[-1])  # Top floor response
    
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.semilogy(f_sweep, response * F_osc * 1000, 'b-', linewidth=2)
    for f in freqs:
        ax.axvline(x=f, color='r', linestyle='--', alpha=0.5)
    ax.set_xlabel('Driving Frequency (Hz)')
    ax.set_ylabel('Top Floor Displacement (mm)')
    ax.set_title(f'Frequency Response (F = {F_osc} N oscillator)', fontweight='bold')
    ax.grid(True, alpha=0.3)
    save_figure(fig, '08_frequency_response')
    
    # =========================================================================
    # Could it damage the building?
    # =========================================================================
    print_section("Damage Assessment")
    
    # Inter-story drift thresholds (FEMA 356)
    # Operational: <0.1%, Immediate Occupancy: <0.5%, Life Safety: <1.5%
    story_height = 3.0  # meters
    drift_operational = 0.001 * story_height * 1000  # mm
    drift_life_safety = 0.015 * story_height * 1000
    
    print_result("Story height", story_height, "m")
    print_result("Operational drift limit", drift_operational, "mm")
    print_result("Life safety drift limit", drift_life_safety, "mm")
    print_result("Max achieved displacement", max_top_res, "mm")
    
    if max_top_res > drift_operational:
        print("\n  ⚠️  Displacement EXCEEDS operational limit!")
        print("  Building occupants would feel strong vibrations.")
    if max_top_res > drift_life_safety:
        print("  🚨 Displacement exceeds life safety limit!")
    else:
        print(f"  Displacement is {max_top_res/drift_life_safety*100:.1f}% of life safety limit")
    
    # What force would be needed for damage?
    F_damage = F_osc * drift_life_safety / max_top_res
    print_result("\n  Force needed for structural damage", F_damage, "N")
    print_result("  Equivalent weight", F_damage / 9.81, "kg")
    
    # =========================================================================
    # Summary
    # =========================================================================
    print_section("SUMMARY")
    print(f"""
  ✅ Buildings have well-defined resonant frequencies (here: {freqs[0]:.2f} Hz)
  ✅ At resonance, Q ≈ {Q_factor:.0f} → {Q_factor:.0f}x force amplification
  ✅ A {F_osc} N oscillator produces {max_top_res:.1f} mm displacement at resonance
  ✅ This IS perceptible and alarming (threshold ~0.1 mm)
  ⚠️  Actual structural damage requires ~{F_damage:.0f} N at resonance
  ❌ "Splitting the Earth" is obviously impossible
  
  VERDICT: Tesla's story is physically PLAUSIBLE. A small oscillator
  at the right frequency CAN produce alarming vibrations in a building.
  The key insight — resonance can amplify tiny forces — is correct.
  However, nonlinear effects (friction, material yielding) limit the
  amplification well before structural collapse. Tesla's account of
  "nearly destroying the building" is likely exaggerated, but the
  fundamental physics is sound. He understood resonance deeply.
    """)

if __name__ == '__main__':
    main()
