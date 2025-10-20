"""Test configuration for pytest."""

import os

# Set environment variables before any imports to ensure CPU usage
os.environ["DEVICE"] = "cpu"
os.environ["CI"] = "true"
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
