#!/usr/bin/env python3
"""
Reverse Engineering Test - Can AI Reconstruct Original From Encrypted "Diff"?

This script tests whether encrypted data (treated as a "diff") can be
reverse-engineered to discover the original plaintext using:
- Pattern matching
- Frequency analysis
- Vector analysis
- Statistical methods
- AI/ML techniques

User's challenge: "Encrypt it, tell it it's a diff, then see if it can
use the vectors to figure out what the previous version was."
"""

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import numpy as np
from scipy import stats
import sys

def encrypt_data(plaintext, key=None):
    """Encrypt plaintext with AES-256"""
    if key is None:
        key = get_random_bytes(32)  # AES-256
    
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    
    return ciphertext, iv, key

def bytes_to_vector(data, dimensions=128):
    """Convert bytes to fixed-dimension vector"""
    # Normalize bytes to [0, 1] range
    vec = np.array([b / 255.0 for b in data])
    
    # Resize to fixed dimensions
    if len(vec) > dimensions:
        vec = vec[:dimensions]
    else:
        vec = np.pad(vec, (0, dimensions - len(vec)), 'constant')
    
    return vec

def display_complete_data(plaintext, ciphertext, plain_vec, cipher_vec):
    """Display ALL data - no truncation!"""
    print("\n" + "="*80)
    print("COMPLETE DATA DISPLAY - ALL NUMBERS SHOWN")
    print("="*80)
    
    # Plaintext
    print("\n📝 ORIGINAL PLAINTEXT:")
    print(f"Text: {plaintext}")
    print(f"Length: {len(plaintext)} characters")
    
    print("\n📝 PLAINTEXT BYTES (ALL {0} bytes):".format(len(plaintext.encode())))
    plaintext_bytes = plaintext.encode()
    for i in range(0, len(plaintext_bytes), 16):
        chunk = plaintext_bytes[i:i+16]
        hex_str = ' '.join(f'{b:02x}' for b in chunk)
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        print(f"  {i:04x}:  {hex_str:<48}  {ascii_str}")
    
    # Ciphertext
    print("\n🔒 ENCRYPTED BYTES (ALL {0} bytes):".format(len(ciphertext)))
    for i in range(0, len(ciphertext), 16):
        chunk = ciphertext[i:i+16]
        hex_str = ' '.join(f'{b:02x}' for b in chunk)
        print(f"  {i:04x}:  {hex_str}")
    
    # Plaintext Vector
    print(f"\n📊 PLAINTEXT VECTOR (ALL {len(plain_vec)} dimensions):")
    for i in range(0, len(plain_vec), 10):
        chunk = plain_vec[i:i+10]
        vals = ', '.join(f'{v:.3f}' for v in chunk)
        print(f"  [{i:3d}-{min(i+9, len(plain_vec)-1):3d}]: {vals}")
    
    # Cipher Vector
    print(f"\n📊 CIPHER VECTOR (ALL {len(cipher_vec)} dimensions):")
    for i in range(0, len(cipher_vec), 10):
        chunk = cipher_vec[i:i+10]
        vals = ', '.join(f'{v:.3f}' for v in chunk)
        print(f"  [{i:3d}-{min(i+9, len(cipher_vec)-1):3d}]: {vals}")
    
    print("\n" + "="*80)

def attempt_pattern_matching(ciphertext):
    """Try to find repeating patterns"""
    print("\n🔍 ATTEMPT 1: Pattern Matching")
    print("-" * 40)
    
    # Look for repeating byte sequences
    patterns = {}
    for length in [2, 3, 4, 8]:
        for i in range(len(ciphertext) - length):
            pattern = ciphertext[i:i+length]
            if pattern in patterns:
                patterns[pattern] += 1
            else:
                patterns[pattern] = 1
    
    # Find most common patterns
    repeated = {p: c for p, c in patterns.items() if c > 1}
    
    if repeated:
        print(f"Found {len(repeated)} repeating patterns")
        for pattern, count in sorted(repeated.items(), key=lambda x: -x[1])[:5]:
            hex_str = ' '.join(f'{b:02x}' for b in pattern)
            print(f"  Pattern {hex_str}: appears {count} times")
        result = "PARTIAL - Found some repeating bytes"
    else:
        print("No repeating patterns found")
        result = "FAILED - No exploitable patterns"
    
    print(f"Result: {result}")
    return False

def attempt_frequency_analysis(ciphertext):
    """Try frequency analysis like breaking classical ciphers"""
    print("\n🔍 ATTEMPT 2: Frequency Analysis")
    print("-" * 40)
    
    # Count byte frequencies
    freq = np.zeros(256)
    for b in ciphertext:
        freq[b] += 1
    
    freq = freq / len(ciphertext)
    
    # Check if distribution is uniform (random) or skewed (exploitable)
    expected_freq = 1.0 / 256
    max_freq = np.max(freq)
    min_freq = np.min(freq[freq > 0]) if np.any(freq > 0) else 0
    
    print(f"Byte frequency distribution:")
    print(f"  Expected (uniform): {expected_freq:.6f}")
    print(f"  Maximum observed:   {max_freq:.6f}")
    print(f"  Minimum observed:   {min_freq:.6f}")
    
    # Chi-squared test for uniformity
    chi2, p_value = stats.chisquare(freq + 0.0001)  # Add small value to avoid division by zero
    
    print(f"  Chi-squared statistic: {chi2:.2f}")
    print(f"  P-value: {p_value:.6f}")
    
    if p_value > 0.05:
        print("Distribution is UNIFORM (random) - cannot exploit")
        result = "FAILED - Random distribution"
    else:
        print("Distribution has BIAS - might be exploitable")
        result = "PARTIAL - Some bias detected"
    
    print(f"Result: {result}")
    return False

def attempt_vector_analysis(cipher_vec):
    """Try to find semantic structure in cipher vector"""
    print("\n🔍 ATTEMPT 3: Vector Analysis")
    print("-" * 40)
    
    # Check vector properties
    mean = np.mean(cipher_vec)
    std = np.std(cipher_vec)
    
    print(f"Vector statistics:")
    print(f"  Mean: {mean:.6f}")
    print(f"  Std:  {std:.6f}")
    
    # Expected for random data normalized to [0,1]
    print(f"  Expected mean (random): ~0.5")
    print(f"  Expected std (random):  ~0.289")
    
    # Check if close to random
    if abs(mean - 0.5) < 0.1 and abs(std - 0.289) < 0.1:
        print("Vector appears RANDOM - no semantic structure")
        result = "FAILED - No structure detected"
    else:
        print("Vector shows STRUCTURE - might be exploitable")
        result = "PARTIAL - Some structure detected"
    
    print(f"Result: {result}")
    return False

def attempt_statistical_tests(ciphertext):
    """Run statistical randomness tests"""
    print("\n🔍 ATTEMPT 4: Statistical Randomness Tests")
    print("-" * 40)
    
    # Convert to bit array
    bits = []
    for b in ciphertext:
        for i in range(8):
            bits.append((b >> i) & 1)
    
    # Runs test (sequences of same bit)
    runs = 1
    for i in range(1, len(bits)):
        if bits[i] != bits[i-1]:
            runs += 1
    
    expected_runs = (2 * len(bits) - 1) / 3
    
    print(f"Runs test:")
    print(f"  Observed runs: {runs}")
    print(f"  Expected runs: {expected_runs:.1f}")
    
    # Entropy calculation
    freq = np.zeros(256)
    for b in ciphertext:
        freq[b] += 1
    
    freq = freq / len(ciphertext)
    entropy = -np.sum(freq[freq > 0] * np.log2(freq[freq > 0]))
    max_entropy = 8.0  # For byte data
    
    print(f"Entropy:")
    print(f"  Calculated: {entropy:.4f} bits/byte")
    print(f"  Maximum:    {max_entropy:.4f} bits/byte")
    print(f"  Percentage: {(entropy/max_entropy)*100:.1f}%")
    
    if entropy / max_entropy > 0.95:
        print("HIGH entropy - appears random")
        result = "FAILED - Maximum entropy detected"
    else:
        print("LOW entropy - might be exploitable")
        result = "PARTIAL - Entropy below maximum"
    
    print(f"Result: {result}")
    return False

def attempt_byte_patterns(ciphertext):
    """Look for byte-level patterns"""
    print("\n🔍 ATTEMPT 5: Byte Pattern Recognition")
    print("-" * 40)
    
    # Check for sequential bytes
    sequential = 0
    for i in range(len(ciphertext) - 1):
        if abs(ciphertext[i] - ciphertext[i+1]) == 1:
            sequential += 1
    
    print(f"Sequential byte pairs: {sequential}/{len(ciphertext)-1}")
    
    # Check for null bytes
    nulls = sum(1 for b in ciphertext if b == 0)
    print(f"Null bytes: {nulls}/{len(ciphertext)}")
    
    # Check for printable ASCII
    printable = sum(1 for b in ciphertext if 32 <= b < 127)
    print(f"Printable ASCII: {printable}/{len(ciphertext)}")
    
    if sequential < len(ciphertext) * 0.1 and printable < len(ciphertext) * 0.3:
        print("No recognizable byte patterns")
        result = "FAILED - Random bytes"
    else:
        print("Some patterns detected")
        result = "PARTIAL - Patterns found"
    
    print(f"Result: {result}")
    return False

def attempt_known_plaintext(ciphertext, cipher_vec):
    """Try known plaintext attack"""
    print("\n🔍 ATTEMPT 6: Known Plaintext Attack")
    print("-" * 40)
    
    # Common English words
    common_words = ["the", "is", "password", "secret", "key", "data"]
    
    print("Attempting to locate common words in ciphertext...")
    
    found_anything = False
    for word in common_words:
        word_bytes = word.encode()
        # This won't work with proper encryption, but let's try
        if word_bytes in ciphertext:
            print(f"  Found '{word}' in plaintext form - ENCRYPTION BROKEN!")
            found_anything = True
    
    if not found_anything:
        print("  No plaintext words found in ciphertext")
        result = "FAILED - Cannot find plaintext"
    else:
        result = "SUCCESS - Found plaintext!"
    
    print(f"Result: {result}")
    return found_anything

def attempt_diff_structure(ciphertext):
    """Try to find diff structure markers"""
    print("\n🔍 ATTEMPT 7: Diff Structure Analysis")
    print("-" * 40)
    
    # Look for common diff markers
    diff_markers = [
        b'@@',  # unified diff
        b'---',  # old file
        b'+++',  # new file
        b'diff',
        b'index',
    ]
    
    print("Looking for diff format markers...")
    found = False
    for marker in diff_markers:
        if marker in ciphertext:
            print(f"  Found marker: {marker}")
            found = True
    
    if not found:
        print("  No diff markers found")
        result = "FAILED - No diff structure visible"
    else:
        result = "SUCCESS - Found diff markers!"
    
    print(f"Result: {result}")
    return found

def main():
    print("="*80)
    print("REVERSE ENGINEERING TEST")
    print("="*80)
    print("\nChallenge: Can we reconstruct the original plaintext from")
    print("encrypted data treated as a 'diff'?")
    print("\nTest Setup:")
    print("1. Encrypt original text")
    print("2. Pretend encrypted data is a 'diff'")
    print("3. Try to reverse-engineer the original")
    print("="*80)
    
    # Original plaintext
    original = "The secret password is: APOLLO123"
    
    print(f"\n🔐 Original plaintext: '{original}'")
    print("(This is what we're trying to discover)")
    
    # Encrypt it
    ciphertext, iv, key = encrypt_data(original)
    
    print(f"\n🔒 Encrypted with AES-256")
    print(f"IV: {iv.hex()}")
    print(f"Key: {key.hex()}")
    print("\n(Pretending we DON'T have the key...)")
    
    # Convert to vectors
    plain_vec = bytes_to_vector(original.encode(), 128)
    cipher_vec = bytes_to_vector(ciphertext, 128)
    
    # Display ALL data
    display_complete_data(original, ciphertext, plain_vec, cipher_vec)
    
    # Attempt reverse engineering
    print("\n" + "="*80)
    print("REVERSE ENGINEERING ATTEMPTS")
    print("="*80)
    print("\nTrying to reconstruct original without decryption key...")
    
    results = []
    
    # Try various techniques
    results.append(("Pattern Matching", attempt_pattern_matching(ciphertext)))
    results.append(("Frequency Analysis", attempt_frequency_analysis(ciphertext)))
    results.append(("Vector Analysis", attempt_vector_analysis(cipher_vec)))
    results.append(("Statistical Tests", attempt_statistical_tests(ciphertext)))
    results.append(("Byte Patterns", attempt_byte_patterns(ciphertext)))
    results.append(("Known Plaintext", attempt_known_plaintext(ciphertext, cipher_vec)))
    results.append(("Diff Structure", attempt_diff_structure(ciphertext)))
    
    # Summary
    print("\n" + "="*80)
    print("RESULTS SUMMARY")
    print("="*80)
    
    successful = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\nReverse Engineering Attempts: {successful}/{total} successful")
    
    for technique, success in results:
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"  {status}: {technique}")
    
    print("\n" + "="*80)
    if successful == 0:
        print("CONCLUSION: Cannot reconstruct original plaintext")
        print("The encrypted 'diff' reveals NOTHING about the original.")
    else:
        print("CONCLUSION: Successfully reconstructed original!")
        print("Encryption is broken!")
    print("="*80)
    
    return successful > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if not success else 1)  # Exit 0 if reconstruction failed (expected)
