# Bitcoin Puzzle 71 - CPU Brute Force (Educational Only)
# WARNING: This is astronomically slow - for demonstration only

import hashlib
import ecdsa
import base58
import os
from multiprocessing import Pool, cpu_count
import numpy as np

# Target address for Puzzle 71
TARGET_ADDRESS = "1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU"

# Puzzle 71 range: 2^70 to 2^71-1
START_RANGE = 0x400000000000000000  # 2^70
END_RANGE = 0x7fffffffffffffffff    # 2^71-1

def private_key_to_wif(private_key_hex):
    """Convert private key hex to WIF format"""
    extended_key = "80" + private_key_hex.zfill(64)
    first_sha256 = hashlib.sha256(bytes.fromhex(extended_key)).hexdigest()
    second_sha256 = hashlib.sha256(bytes.fromhex(first_sha256)).hexdigest()
    checksum = second_sha256[:8]
    final_key = extended_key + checksum
    wif = base58.b58encode(bytes.fromhex(final_key)).decode('utf-8')
    return wif

def private_key_to_address(private_key_int):
    """Convert private key integer to Bitcoin address"""
    # Convert to 32-byte hex
    private_key_hex = format(private_key_int, '064x')
    
    # Generate public key using ECDSA
    sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key_hex), curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    public_key = b'\x04' + vk.to_string()
    
    # SHA256 then RIPEMD160
    sha256_bpk = hashlib.sha256(public_key).digest()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256_bpk)
    hash160 = ripemd160.digest()
    
    # Add network byte and checksum
    network_hash160 = b'\x00' + hash160
    checksum = hashlib.sha256(hashlib.sha256(network_hash160).digest()).digest()[:4]
    address_bytes = network_hash160 + checksum
    address = base58.b58encode(address_bytes).decode('utf-8')
    
    return address, private_key_hex

def check_key(private_key_int):
    """Check if a private key generates the target address"""
    try:
        address, private_key_hex = private_key_to_address(private_key_int)
        if address == TARGET_ADDRESS:
            return True, private_key_int, private_key_hex
        return False, None, None
    except:
        return False, None, None

def random_search_worker(args):
    """Worker for random search"""
    worker_id, iterations = args
    import random
    random.seed(os.urandom(32) + str(worker_id).encode())
    
    for i in range(iterations):
        # Random search within range
        private_key = random.randint(START_RANGE, END_RANGE)
        found, pk_int, pk_hex = check_key(private_key)
        if found:
            return pk_int, pk_hex
        if i % 1000 == 0 and worker_id == 0:
            print(f"Worker {worker_id}: Checked {i} keys...")
    return None

def sequential_search_worker(args):
    """Worker for sequential search"""
    worker_id, start, end = args
    for i in range(start, end):
        found, pk_int, pk_hex = check_key(i)
        if found:
            return pk_int, pk_hex
        if i % 10000 == 0 and worker_id == 0:
            print(f"Progress: {i}/{end}")
    return None

# Main execution
if __name__ == "__main__":
    print(f"Bitcoin Puzzle 71 Solver")
    print(f"Target: {TARGET_ADDRESS}")
    print(f"Range: {hex(START_RANGE)} to {hex(END_RANGE)}")
    print(f"Total keys: {END_RANGE - START_RANGE:,}")
    print(f"WARNING: This will take effectively forever on CPU!\n")
    
    # For demonstration, check just a few keys
    test_keys = [
        START_RANGE,
        START_RANGE + 1,
        START_RANGE + 2,
        (START_RANGE + END_RANGE) // 2,
    ]
    
    print("Testing sample keys:")
    for key in test_keys:
        addr, pk_hex = private_key_to_address(key)
        print(f"Private Key: {pk_hex}")
        print(f"Address: {addr}")
        print(f"Match: {addr == TARGET_ADDRESS}\n")
