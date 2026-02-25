"""Plasma physics utilities for Tesla Lab experiments."""
import numpy as np
from scipy import constants

E_CHARGE = constants.e
M_E = constants.m_e
EPS_0 = constants.epsilon_0
K_B = constants.k
C = constants.c

def plasma_frequency(n_e):
    """Electron plasma frequency (Hz) for electron density n_e (m^-3).
    ω_pe = sqrt(n_e * e² / (m_e * ε₀))
    """
    omega_pe = np.sqrt(n_e * E_CHARGE**2 / (M_E * EPS_0))
    return omega_pe / (2 * np.pi)

def debye_length(T_e, n_e):
    """Debye length (m) for electron temperature T_e (K) and density n_e (m^-3)."""
    return np.sqrt(EPS_0 * K_B * T_e / (n_e * E_CHARGE**2))

def collision_frequency(n_n, T_e, sigma_en=1e-19):
    """Electron-neutral collision frequency (Hz).
    n_n: neutral density (m^-3), T_e: electron temp (K)
    sigma_en: cross section (m^2), default ~1e-19 for air
    """
    v_th = np.sqrt(8 * K_B * T_e / (np.pi * M_E))
    return n_n * sigma_en * v_th

def plasma_conductivity(n_e, nu_c):
    """DC plasma conductivity (S/m).
    n_e: electron density (m^-3), nu_c: collision frequency (Hz)
    """
    return n_e * E_CHARGE**2 / (M_E * nu_c)

def plasma_sphere_energy(radius, T_e, n_e):
    """Thermal energy content of a plasma sphere (J).
    3/2 * n * k_B * T * V for electrons + ions
    """
    V = (4/3) * np.pi * radius**3
    return 3 * n_e * K_B * T_e * V  # Factor 3 = 3/2 * 2 (electrons + ions)

def bremsstrahlung_power_density(n_e, T_e, Z=1):
    """Bremsstrahlung radiation power density (W/m^3).
    P = 1.69e-32 * n_e^2 * Z^2 * sqrt(T_e)  [T_e in eV]
    """
    T_eV = K_B * T_e / E_CHARGE
    return 1.69e-32 * n_e**2 * Z**2 * np.sqrt(T_eV)

def em_cavity_modes(radius, n_max=5):
    """Resonant frequencies of EM standing waves in spherical cavity.
    Returns TM modes: x_nl zeros of spherical Bessel functions.
    Uses approximate zeros for j_n(x) = 0.
    """
    from scipy.special import spherical_jn
    from scipy.optimize import brentq
    
    modes = []
    for n in range(1, n_max + 1):
        for l_idx in range(1, n_max + 1):
            # Find l-th zero of j_n(x)
            x_low = l_idx * np.pi - np.pi/2 if n == 0 else n + l_idx * np.pi * 0.8
            x_high = x_low + np.pi
            try:
                zero = brentq(lambda x: spherical_jn(n, x), max(0.1, x_low), x_high)
                freq = zero * constants.c / (2 * np.pi * radius)
                modes.append((n, l_idx, freq))
            except (ValueError, RuntimeError):
                continue
    return sorted(modes, key=lambda x: x[2])
