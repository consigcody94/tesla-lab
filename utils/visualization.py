"""Visualization utilities for Tesla Lab experiments."""
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving
import matplotlib.pyplot as plt
import numpy as np
import os

# Publication-quality defaults
plt.rcParams.update({
    'figure.figsize': (10, 7),
    'figure.dpi': 150,
    'font.size': 12,
    'font.family': 'serif',
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'legend.fontsize': 11,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'lines.linewidth': 2,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'figure.facecolor': 'white',
    'savefig.bbox': 'tight',
    'savefig.dpi': 150,
})

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results')

def save_figure(fig, name, formats=('png',)):
    """Save figure to results directory."""
    os.makedirs(RESULTS_DIR, exist_ok=True)
    for fmt in formats:
        path = os.path.join(RESULTS_DIR, f'{name}.{fmt}')
        fig.savefig(path)
        print(f"  📊 Saved: {path}")
    plt.close(fig)

def tesla_style_plot(title, xlabel, ylabel):
    """Create a styled figure for Tesla experiments."""
    fig, ax = plt.subplots()
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return fig, ax

def multi_panel(nrows, ncols, title=None):
    """Create multi-panel figure."""
    fig, axes = plt.subplots(nrows, ncols, figsize=(5*ncols, 4*nrows))
    if title:
        fig.suptitle(title, fontweight='bold', fontsize=16)
    fig.tight_layout(rect=[0, 0, 1, 0.96] if title else [0, 0, 1, 1])
    return fig, axes

def print_header(experiment_name):
    """Print experiment header."""
    print("\n" + "="*70)
    print(f"⚡ TESLA LAB: {experiment_name}")
    print("="*70)

def print_section(name):
    """Print section header."""
    print(f"\n{'─'*50}")
    print(f"  {name}")
    print(f"{'─'*50}")

def print_result(label, value, unit=""):
    """Print a formatted result."""
    if isinstance(value, float):
        if abs(value) < 0.01 or abs(value) > 1e6:
            print(f"  {label}: {value:.4e} {unit}")
        else:
            print(f"  {label}: {value:.4f} {unit}")
    else:
        print(f"  {label}: {value} {unit}")
