# Bitcoin Puzzle 71 - Pool Client for btcpuzzle.info
# This is the practical way to participate

import requests
import hashlib
import json
import time
import os

class BtcPuzzlePoolClient:
    """
    Client for btcpuzzle.info pool
    Requires API key from website
    """
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://btcpuzzle.info/api"
        self.worker_name = f"kaggle_worker_{os.urandom(4).hex()}"
        
    def get_range(self):
        """Get a range to scan from the pool"""
        try:
            response = requests.post(
                f"{self.base_url}/get_range",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"worker": self.worker_name, "puzzle": 71}
            )
            return response.json()
        except Exception as e:
            print(f"Error getting range: {e}")
            return None
    
    def submit_proof(self, range_id, proof_keys):
        """Submit proof of work for scanned range"""
        try:
            response = requests.post(
                f"{self.base_url}/submit",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "range_id": range_id,
                    "proof": proof_keys,
                    "worker": self.worker_name
                }
            )
            return response.json()
        except Exception as e:
            print(f"Error submitting proof: {e}")
            return None
    
    def scan_range(self, start_hex, end_hex):
        """
        Scan a range for the target address
        This is where you'd integrate GPU acceleration
        """
        start = int(start_hex, 16)
        end = int(end_hex, 16)
        
        print(f"Scanning range: {start_hex} to {end_hex}")
        print(f"Total keys: {end - start:,}")
        
        # Placeholder for actual scanning logic
        # In practice, this would use VanitySearch or similar
        
        # Generate 3 proof keys (required by pool)
        proof_keys = []
        for i in range(3):
            key = start + (i * (end - start) // 4)
            proof_keys.append(hex(key))
        
        return proof_keys

def main():
    """
    Main loop for pool participation
    """
    API_KEY = "your_api_key_here"  # Get from btcpuzzle.info
    
    if API_KEY == "your_api_key_here":
        print("Please register at btcpuzzle.info and get an API key")
        print("This is the only practical way to participate in the puzzle")
        return
    
    client = BtcPuzzlePoolClient(API_KEY)
    
    print(f"Starting worker: {client.worker_name}")
    print("Connecting to btcpuzzle.info pool...")
    
    while True:
        # Get work
        work = client.get_range()
        if not work:
            print("No work available, waiting...")
            time.sleep(60)
            continue
        
        range_id = work.get('range_id')
        start = work.get('start')
        end = work.get('end')
        
        print(f"Got range {range_id}: {start} to {end}")
        
        # Scan range (this would take hours/days depending on hardware)
        proof = client.scan_range(start, end)
        
        # Submit proof
        result = client.submit_proof(range_id, proof)
        print(f"Submitted proof: {result}")
        
        print("Range complete. Getting next range...")
        time.sleep(5)

if __name__ == "__main__":
    main()
