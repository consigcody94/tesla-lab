#!/bin/bash
# Tesla Lab Setup
set -e
echo "🔬 Setting up Tesla Lab..."
pip install -r requirements.txt
mkdir -p results
echo "✅ Setup complete. Run experiments with: python experiments/01_tesla_coil_resonance.py"
