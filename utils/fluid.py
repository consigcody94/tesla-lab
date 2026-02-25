"""Fluid dynamics utilities for Tesla Lab experiments."""
import numpy as np
from scipy.integrate import solve_ivp

def reynolds_number(rho, v, L, mu):
    """Reynolds number: Re = ρvL/μ."""
    return rho * v * L / mu

def boundary_layer_thickness(x, Re_x):
    """Blasius boundary layer thickness: δ ≈ 5x/√(Re_x)."""
    return 5.0 * x / np.sqrt(Re_x)

def pipe_friction_factor(Re, relative_roughness=0.0):
    """Darcy friction factor. Laminar: 64/Re. Turbulent: Colebrook (iterative)."""
    if np.isscalar(Re):
        Re = np.array([Re])
    f = np.where(Re < 2300, 64.0 / Re, 0.02)  # Initial guess for turbulent
    
    # Colebrook iteration for turbulent
    turb = Re >= 2300
    for _ in range(20):
        f_old = f.copy()
        rhs = -2.0 * np.log10(relative_roughness / 3.7 + 2.51 / (Re * np.sqrt(f + 1e-30)))
        f_new = 1.0 / (rhs**2 + 1e-30)
        f = np.where(turb, f_new, f)
        if np.max(np.abs(f - f_old)) < 1e-10:
            break
    return f.squeeze()

def disk_gap_flow(omega, r_inner, r_outer, gap, nu, N_points=100):
    """Solve viscous flow between rotating disk and stationary surface.
    Returns (r, v_theta, tau_wall) for Tesla turbine analysis.
    omega: angular velocity (rad/s)
    r_inner, r_outer: radii (m)
    gap: disk spacing (m)
    nu: kinematic viscosity (m^2/s)
    """
    r = np.linspace(r_inner, r_outer, N_points)
    
    # For narrow gap (gap << r), approximate as Couette flow between disks
    # v_theta varies linearly across gap, from 0 (stationary) to omega*r (rotating)
    # Shear stress: tau = mu * omega * r / gap
    mu = nu * 1000  # Assuming water density ~1000 kg/m3 for dynamic viscosity
    
    v_theta = omega * r  # At the rotating disk surface
    tau_wall = mu * omega * r / gap  # Wall shear stress
    
    return r, v_theta, tau_wall

def torque_on_disk(omega, r_inner, r_outer, gap, nu, rho=1000):
    """Total torque on one side of one disk in Tesla turbine.
    T = ∫ τ(r) · r · 2πr dr from r_inner to r_outer
    """
    mu = nu * rho
    # τ = μ·ω·r/gap, so T = 2π·μ·ω/gap · ∫r³ dr
    T = 2 * np.pi * mu * omega / gap * (r_outer**4 - r_inner**4) / 4
    return T

def valvular_conduit_resistance(Re, direction='forward', geometry_factor=1.0):
    """Simplified flow resistance for Tesla's valvular conduit.
    Forward: relatively smooth flow path
    Reverse: flow encounters multiple obstructions creating turbulence
    Returns pressure drop coefficient (dimensionless).
    """
    if direction == 'forward':
        # Mild turns, mostly laminar-like even at moderate Re
        if Re < 500:
            K = 2.0 * geometry_factor
        else:
            K = 2.0 * geometry_factor + 0.005 * (Re - 500)
    else:
        # Reverse: turbulent separation at each bucket, high losses
        if Re < 200:
            K = 4.0 * geometry_factor  # Even laminar has higher loss
        else:
            K = 4.0 * geometry_factor + 0.05 * (Re - 200)
    return K
