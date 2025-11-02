"""
FraudAGENT - Insurance Claims AI Agent for Hugging Face Spaces
Optimized for Hugging Face Spaces deployment with automatic secret management.
"""

import os
import sys

# Hugging Face Spaces automatically provides secrets as environment variables
# No need to load from .env file

# Set defaults for Hugging Face Spaces
if 'APP_HOST' not in os.environ:
    os.environ['APP_HOST'] = '0.0.0.0'
if 'APP_PORT' not in os.environ:
    os.environ['APP_PORT'] = '7860'
if 'OPENAI_MODEL' not in os.environ:
    os.environ['OPENAI_MODEL'] = 'gpt-4o-mini'

# Install mock kumoai for demo mode if real SDK not available
sys.path.insert(0, os.path.dirname(__file__))
try:
    import kumoai
except ImportError:
    import mock_kumoai
    sys.modules['kumoai'] = mock_kumoai
    sys.modules['kumoai.experimental'] = mock_kumoai
    sys.modules['kumoai.experimental.rfm'] = mock_kumoai

# Now run the main application
exec(open('main_with_upload.py').read())
