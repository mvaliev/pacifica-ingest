#!/usr/bin/python
"""Test ingest."""
import os
import requests


def test_upload():
    """Test the upload."""
    bundle_path = 'test_data/baby.tar'
    print('file size: ' + str(os.path.getsize(bundle_path)))
    with open(bundle_path, 'rb') as filefd:
        req = requests.post(
            'http://127.0.0.1:8066/upload',
            data=filefd,
            headers={
                'Content-Type': 'application/octet-stream'
            }
        )
        result = req.status_code
        print(result)
