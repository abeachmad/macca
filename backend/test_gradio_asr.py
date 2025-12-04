#!/usr/bin/env python3
import sys
from gradio_client import Client

print("Testing Gradio ASR Space...")
print("Connecting to abeachmad/macca-asr...")

try:
    client = Client("abeachmad/macca-asr")
    print("✓ Connected successfully")
    
    # Test with a dummy audio file
    test_audio = sys.argv[1] if len(sys.argv) > 1 else "/tmp/test.webm"
    print(f"Testing transcription with: {test_audio}")
    
    result = client.predict(
        audio=test_audio,
        api_name="/transcribe"
    )
    
    print(f"Result type: {type(result)}")
    print(f"Result: {result}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
