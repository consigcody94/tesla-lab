"""Electromagnetic field utilities for Tesla Lab experiments."""
import numpy as np
from scipy import constants

# Physical constants
MU_0 = constants.mu_0          # Permeability of free space (H/m)
EPS_0 = constants.epsilon_0    # Permittivity of free space (F/m)
C = constants.c                # Speed of light (m/s)
E_CHARGE = constants.e         # Elementary charge (C)

def skin_depth(frequency, conductivity, mu_r=1.0):
    """Calculate skin depth (m) for EM wave in conductor.
    δ = sqrt(2 / (ω·μ·σ))
    """
    omega = 2 * np.pi * frequency
    return np.sqrt(2.0 / (omega * mu_r * MU_0 * conductivity))

def wave_impedance(frequency, conductivity, epsilon_r=1.0, mu_r=1.0):
    """Complex wave impedance of a lossy medium."""
    omega = 2 * np.pi * frequency
    eps = epsilon_r * EPS_0
    mu = mu_r * MU_0
    # Complex permittivity with conductivity
    eps_complex = eps - 1j * conductivity / omega
    return np.sqrt(mu / eps_complex)

def propagation_constant(frequency, conductivity, epsilon_r=1.0, mu_r=1.0):
    """Complex propagation constant γ = α + jβ for lossy medium."""
    omega = 2 * np.pi * frequency
    eps = epsilon_r * EPS_0
    mu = mu_r * MU_0
    eps_complex = eps - 1j * conductivity / omega
    gamma = 1j * omega * np.sqrt(mu * eps_complex)
    return gamma

def resonant_frequency_LC(L, C_cap):
    """Resonant frequency of LC circuit: f = 1/(2π√(LC))."""
    return 1.0 / (2.0 * np.pi * np.sqrt(L * C_cap))

def coil_inductance_wheeler(N, R, l):
    """Wheeler's approximation for single-layer solenoid inductance (H).
    N: number of turns, R: radius (m), l: length (m)
    """
    # Convert to inches for Wheeler's formula, then back to H
    R_in = R * 39.3701
    l_in = l * 39.3701
    L_uH = (R_in**2 * N**2) / (9 * R_in + 10 * l_in)
    return L_uH * 1e-6

def self_capacitance_medhurst(R, l):
    """Medhurst approximation for self-capacitance of solenoid (F).
    R: radius (m), l: length (m)
    """
    D = 2 * R
    ratio = l / D
    # Medhurst empirical formula (pF per cm of coil diameter)
    H = 0.1126 * l / D + 0.08 + 0.27 / (l / D)
    C_pF = H * D * 100  # D in cm
    return C_pF * 1e-12

def zenneck_wave_attenuation(frequency, sigma_ground=0.01, eps_r_ground=15):
    """Attenuation of Zenneck surface wave (Np/m).
    Returns (radial_attenuation, vertical_decay_air, vertical_decay_ground).
    """
    omega = 2 * np.pi * frequency
    k0 = omega / C
    eps2 = eps_r_ground - 1j * sigma_ground / (omega * EPS_0)
    
    # Zenneck wave radial propagation constant
    kz = k0 * np.sqrt(eps2 / (1 + eps2))
    alpha_radial = np.abs(np.imag(kz)) if np.real(kz) > 0 else np.abs(kz.imag)
    
    # Vertical decay constants
    gamma_air = np.sqrt(kz**2 - k0**2)
    gamma_ground = np.sqrt(kz**2 - k0**2 * eps2)
    
    return np.real(kz), np.abs(np.real(gamma_air)), np.abs(np.real(gamma_ground))
