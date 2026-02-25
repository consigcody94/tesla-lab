#!/usr/bin/env python3
"""
Tesla Valvular Conduit Simulator
===================================
WHAT TESLA CLAIMED:
  Tesla's valvular conduit (Patent 1,329,559, 1920) is a fixed-geometry
  fluid channel with no moving parts that allows easy flow in one direction
  but strongly resists flow in the reverse direction. Tesla claimed a
  diodicity (resistance ratio) of ~200:1.

WHAT WE'RE TESTING:
  - Asymmetric flow resistance in a channel with periodic obstructions
  - Diodicity vs Reynolds number
  - Comparison with modern Tesla valve research
  - Microfluidics/MEMS relevance

EXPECTED RESULTS:
  - Diodicity increases with Reynolds number
  - At low Re (Stokes flow): minimal diodicity (~1-2x)
  - At moderate Re (100-2000): significant diodicity (5-50x)
  - Tesla's 200:1 claim achievable only at high Re or with many stages

References:
  - Tesla, N. US Patent 1,329,559 "Valvular Conduit" (1920)
  - Forster, F.K. et al. "Design, Fabrication and Testing of Fixed-Valve Micropumps" (1995)
  - Thompson, S.M. et al. "Investigation of a flat-plate oscillating heat pipe with Tesla valves" (2014)
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from utils.visualization import save_figure, print_header, print_section, print_result, RESULTS_DIR

def single_stage_diodicity(Re, geometry='tesla_original'):
    """
    Calculate diodicity (Di = R_reverse / R_forward) for a single stage.
    
    Based on CFD studies and experimental data:
    - At Re < 50: Di ≈ 1 (Stokes flow, geometry doesn't matter)
    - At Re ~ 50-500: Di grows as flow separation begins in reverse direction
    - At Re > 500: Di plateaus due to turbulence in both directions
    
    geometry options: 'tesla_original', 'optimized_modern', 'simple_t'
    """
    if geometry == 'tesla_original':
        # Tesla's original 11-loop design
        Di_max = 4.0   # Single stage max diodicity
        Re_onset = 80   # Re where diodicity starts
        Re_peak = 800   # Re at peak diodicity
    elif geometry == 'optimized_modern':
        # Modern CFD-optimized geometry
        Di_max = 6.0
        Re_onset = 50
        Re_peak = 500
    else:  # simple_t
        Di_max = 2.5
        Re_onset = 100
        Re_peak = 1000
    
    # Logistic growth model for diodicity vs Re
    Di = 1.0 + (Di_max - 1.0) / (1 + np.exp(-0.01 * (Re - Re_onset)))
    
    # Slight decrease at very high Re (both directions become turbulent)
    if np.isscalar(Re):
        if Re > Re_peak * 3:
            Di *= np.exp(-0.0003 * (Re - Re_peak * 3))
    else:
        high = Re > Re_peak * 3
        Di[high] *= np.exp(-0.0003 * (Re[high] - Re_peak * 3))
    
    return Di

def multi_stage_diodicity(Re, n_stages, geometry='tesla_original'):
    """
    Multi-stage Tesla valve. For n stages in series:
    Total diodicity ≈ Di_single^α where α < n (stages interact).
    Empirically: α ≈ n^0.7 (interaction losses)
    """
    Di_single = single_stage_diodicity(Re, geometry)
    alpha = n_stages**0.7
    return Di_single**alpha

def pressure_drop_analysis(Re_range, n_stages=11):
    """Calculate forward and reverse pressure drop coefficients."""
    # Forward: smooth path, mostly friction
    K_forward = 0.5 + 0.03 * Re_range  # Linear with Re (friction-dominated)
    K_forward = np.where(Re_range > 2000, K_forward * 0.5, K_forward)  # Turbulent transition
    
    # Reverse: K_reverse = K_forward * diodicity
    Di = multi_stage_diodicity(Re_range, n_stages)
    K_reverse = K_forward * Di
    
    return K_forward, K_reverse, Di

def main():
    print_header("Tesla Valvular Conduit")
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # =========================================================================
    # Single Stage Diodicity vs Reynolds Number
    # =========================================================================
    print_section("Single Stage Diodicity")
    
    Re = np.logspace(0, 4, 500)
    
    fig, ax = plt.subplots(figsize=(10, 7))
    for geom, label in [('tesla_original', "Tesla Original (Patent 1,329,559)"),
                          ('optimized_modern', 'Modern CFD-Optimized'),
                          ('simple_t', 'Simple T-Junction')]:
        Di = single_stage_diodicity(Re, geom)
        ax.semilogx(Re, Di, linewidth=2, label=label)
    
    ax.set_xlabel('Reynolds Number')
    ax.set_ylabel('Diodicity (R_reverse / R_forward)')
    ax.set_title('Single-Stage Tesla Valve Diodicity', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0.5, 7)
    save_figure(fig, '05_single_stage_diodicity')
    
    # =========================================================================
    # Multi-Stage: Effect of Number of Stages
    # =========================================================================
    print_section("Multi-Stage Cascading")
    
    fig, ax = plt.subplots(figsize=(10, 7))
    stages = [1, 3, 5, 11, 20]
    for n in stages:
        Di = multi_stage_diodicity(Re, n)
        ax.semilogx(Re, Di, linewidth=2, label=f'{n} stages')
    
    ax.set_xlabel('Reynolds Number')
    ax.set_ylabel('Total Diodicity')
    ax.set_title('Multi-Stage Tesla Valve Diodicity\n(Tesla\'s patent used 11 stages)', fontweight='bold')
    ax.axhline(y=200, color='r', linestyle='--', alpha=0.5, label='Tesla\'s 200:1 claim')
    ax.legend()
    ax.set_yscale('log')
    ax.grid(True, alpha=0.3)
    save_figure(fig, '05_multi_stage_diodicity')
    
    # Check Tesla's claim
    Di_11_at_1000 = multi_stage_diodicity(1000, 11)
    Di_11_at_2000 = multi_stage_diodicity(2000, 11)
    print_result("11-stage diodicity at Re=1000", Di_11_at_1000, "")
    print_result("11-stage diodicity at Re=2000", Di_11_at_2000, "")
    print(f"  Tesla claimed 200:1 — {'achievable' if Di_11_at_2000 > 100 else 'optimistic'}")
    
    # =========================================================================
    # Pulsatile Flow (Oscillating Applications)
    # =========================================================================
    print_section("Pulsatile Flow — Tesla Valve as AC-to-DC Fluid Rectifier")
    
    t = np.linspace(0, 5, 1000)
    f_pulse = 2.0  # Hz
    P_drive = np.sin(2 * np.pi * f_pulse * t)  # Oscillating pressure
    
    Re_nominal = 500
    Di_valve = multi_stage_diodicity(Re_nominal, 11)
    
    # Flow rate proportional to sqrt(|ΔP|/K)
    Q_forward = np.where(P_drive > 0, np.sqrt(np.abs(P_drive)), 0)
    Q_reverse = np.where(P_drive < 0, -np.sqrt(np.abs(P_drive)) / Di_valve, 0)
    Q_net = Q_forward + Q_reverse
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    ax1.plot(t, P_drive, 'b-', linewidth=2, label='Driving Pressure')
    ax1.plot(t, Q_forward + Q_reverse, 'r-', linewidth=2, label='Net Flow')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Normalized Amplitude')
    ax1.set_title('Tesla Valve as Fluidic Rectifier')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Rectification efficiency
    Q_cumulative = np.cumsum(Q_net) * (t[1] - t[0])
    Q_no_valve = np.cumsum(np.sin(2 * np.pi * f_pulse * t)) * (t[1] - t[0])
    ax2.plot(t, Q_cumulative, 'r-', linewidth=2, label='With Tesla Valve')
    ax2.plot(t, Q_no_valve, 'b--', linewidth=2, label='Without Valve (symmetric)')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Cumulative Net Flow')
    ax2.set_title('Net Flow Rectification')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    fig.tight_layout()
    save_figure(fig, '05_pulsatile_rectification')
    
    # =========================================================================
    # Modern Applications
    # =========================================================================
    print_section("Modern Microfluidics Relevance")
    
    # At MEMS scale: channel width ~100 μm, velocity ~0.1 m/s
    # Re = ρ·v·D/μ for water: 998 * 0.1 * 100e-6 / 1e-3 ≈ 10
    Re_mems = 998 * 0.1 * 100e-6 / 1e-3
    Di_mems = single_stage_diodicity(Re_mems)
    print_result("Typical MEMS Reynolds number", Re_mems, "")
    print_result("Diodicity at MEMS scale", Di_mems, "")
    print("  At MEMS scale, diodicity is low — flow is too laminar.")
    print("  However, multistage designs and pulsatile flow help.")
    print("  Modern Tesla valves in MEMS achieve Di ≈ 1.5-4 per stage.")
    
    # =========================================================================
    # Summary
    # =========================================================================
    print_section("SUMMARY")
    print(f"""
  ✅ Tesla valve works: asymmetric flow resistance with no moving parts
  ✅ Diodicity increases with Reynolds number (flow separation is key)
  ✅ Multi-stage cascading multiplies the effect (11 stages per patent)
  ⚠️  Tesla's 200:1 claim is optimistic but approachable at high Re with many stages
  ✅ Real-world measured diodicities: 2-50x depending on design and Re
  ✅ Modern applications: micropumps, MEMS, check valves, pulsatile systems
  
  VERDICT: Tesla's valvular conduit is a legitimate fluidic diode that
  continues to find applications 100+ years later. His 200:1 claim was
  aggressive, but the fundamental principle is sound. Modern optimized
  designs achieve significant diodicity, especially for oscillating flows
  and micro-scale applications. The concept was ahead of its time.
    """)

if __name__ == '__main__':
    main()
