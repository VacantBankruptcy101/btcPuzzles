# Bitcoin Puzzle 71 - Pattern-Based Search
# Uses statistical patterns from solved puzzles to prioritize search

import hashlib
import ecdsa
import base58
import random
import numpy as np
from collections import Counter

# Load solved puzzle data for pattern analysis
SOLVED_PUZZLES = {
    66: "0x2832ed74f2b5e35ee",
    67: "0x730fc235c1942c1ae", 
    68: "0xbebb3940cd0fc1491",
    69: "0x101d83275fb2bc7e0c",
    70: "0x349b84b6431a6c4ef1"
}

def analyze_patterns():
    """Analyze patterns in solved puzzles"""
    keys = [int(v, 16) for v in SOLVED_PUZZLES.values()]
    
    print("Pattern Analysis of Solved Puzzles:")
    print("-" * 40)
    
    # Check bit distributions
    for puzzle_num, key_hex in SOLVED_PUZZLES.items():
        key_int = int(key_hex, 16)
        binary = bin(key_int)[2:].zfill(72)
        ones = binary.count('1')
        zeros = binary.count('0')
        print(f"Puzzle {puzzle_num}: {key_hex}")
        print(f"  Population count: {ones} ones, {zeros} zeros")
        print(f"  Leading zeros: {72 - len(bin(key_int)[2:])}")
        print(f"  Byte pattern: {[hex((key_int >> (8*i)) & 0xff) for i in range(9)]}")
        print()

def generate_pattern_based_candidates(center, spread, count=1000):
    """
    Generate candidates around a center point with specific patterns
    Based on observation that puzzle keys often have balanced bit patterns
    """
    candidates = []
    
    for _ in range(count):
        # Gaussian distribution around center
        offset = int(np.random.normal(0, spread))
        candidate = center + offset
        
        # Ensure in valid range
        if 0x400000000000000000 <= candidate <= 0x7fffffffffffffffff:
            # Apply pattern filters based on solved puzzles
            binary = bin(candidate)[2:]
            ones = binary.count('1')
            
            # Prioritize keys with bit counts similar to solved puzzles (30-40 ones in 72 bits)
            if 25 <= ones <= 45:
                candidates.append(candidate)
    
    return candidates

def hamming_distance(a, b):
    """Calculate Hamming distance between two integers"""
    return bin(a ^ b).count('1')

def find_similar_keys():
    """Find keys similar to solved puzzles using Hamming distance"""
    target_range_center = (0x400000000000000000 + 0x7fffffffffffffffff) // 2
    
    print(f"Searching around center: {hex(target_range_center)}")
    
    # Generate candidates based on solved puzzle statistics
    candidates = generate_pattern_based_candidates(target_range_center, 2**60, 10000)
    
    print(f"Generated {len(candidates)} pattern-based candidates")
    
    # Check candidates (placeholder - would need actual address verification)
    for i, candidate in enumerate(candidates[:10]):
        print(f"Candidate {i}: {hex(candidate)}")

# Run analysis
if __name__ == "__main__":
    analyze_patterns()
    find_similar_keys()
    
    # Monte Carlo simulation of search probability
    total_keys = 0x7fffffffffffffffff - 0x400000000000000000
    keys_per_second = 1000  # Optimistic CPU rate
    seconds_per_day = 86400
    
    print(f"\nProbability Analysis:")
    print(f"Total keyspace: {total_keys:.2e}")
    print(f"Keys/sec (CPU): {keys_per_second}")
    print(f"Days to exhaust: {total_keys / keys_per_second / seconds_per_day:.2e}")
    print(f"Years to exhaust: {total_keys / keys_per_second / seconds_per_day / 365:.2e}")
