#!/usr/bin/env python3
import os
import sys

# Set environment
os.environ['KUMO_API_KEY'] = 'demo-kumo-key'
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', 'sk-test')
os.environ['APP_HOST'] = '0.0.0.0'
os.environ['APP_PORT'] = '7862'

# Install mock kumoai
sys.path.insert(0, '/home/ubuntu/insurance-claims-kumo-agent')
import mock_kumoai
sys.modules['kumoai'] = mock_kumoai
sys.modules['kumoai.experimental'] = mock_kumoai
sys.modules['kumoai.experimental.rfm'] = mock_kumoai

# Now run the application
exec(open('main_with_upload.py').read())
