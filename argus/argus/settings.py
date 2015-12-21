"""
Argus deployment settings and defaults.
The settings of argus are passed via environment variables.
"""
import os

ARGUS_ADDRESS = os.getenv('ARGUS_ADDRESS', '0.0.0.0')
ARGUS_PORT = os.getenv('ARGUS_PORT', '5000')
ARGUS_ROOT = os.getenv('ARGUS_ROOT', '/')
