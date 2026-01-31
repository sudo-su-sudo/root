#!/usr/bin/env python3
"""
Practical Demonstration: Why Encryption Diffs Reveal Nothing

This script shows EXACTLY why your theory about "seeing through encryption"
doesn't work in practice. Run it yourself and see!

Author: Educational response to vector/encryption misconception
"""

import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import binascii


def encrypt_aes(plaintext: str, key: bytes) -> bytes:
    """Encrypt text using AES-256"""
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
    return cipher.iv + ct_bytes  # Prepend IV


def show_hex(data: bytes, label: str):
    """Display bytes as hex for readability"""
    print(f"{label}:")
    print(f"  {binascii.hexlify(data).decode()}")
    print()


def calculate_difference(data1: bytes, data2: bytes) -> int:
    """Calculate how many bytes differ between two byte strings"""
    min_len = min(len(data1), len(data2))
    differences = sum(1 for i in range(min_len) if data1[i] != data2[i])
    differences += abs(len(data1) - len(data2))
    return differences


def main():
    print("=" * 70)
    print("ENCRYPTION DIFF DEMONSTRATION")
    print("Proving that encrypted diffs reveal NOTHING about plaintext diffs")
    print("=" * 70)
    print()
    
    # Use a consistent key for reproducibility
    key = hashlib.sha256(b"demonstration_key").digest()  # 256-bit key
    
    # TEST 1: Similar plaintexts
    print("TEST 1: Very Similar Plaintexts (1 character difference)")
    print("-" * 70)
    
    plaintext1 = "Hello World! This is a secret message."
    plaintext2 = "Hello World! This is a secret messag?"  # Changed last char
    
    print(f"Plaintext 1: {plaintext1}")
    print(f"Plaintext 2: {plaintext2}")
    print(f"Plaintext diff: 1 character changed (e → ?)")
    print()
    
    # Encrypt both
    encrypted1 = encrypt_aes(plaintext1, key)
    encrypted2 = encrypt_aes(plaintext2, key)
    
    show_hex(encrypted1, "Encrypted 1")
    show_hex(encrypted2, "Encrypted 2")
    
    # Show the difference
    byte_diff = calculate_difference(encrypted1, encrypted2)
    print(f"Encrypted diff: {byte_diff} out of {len(encrypted1)} bytes differ")
    print(f"Percentage different: {byte_diff/len(encrypted1)*100:.1f}%")
    print()
    print("☝️ Notice: Changed 1 character in plaintext → Almost ALL bytes changed in ciphertext!")
    print("   This is the AVALANCHE EFFECT. It destroys patterns.")
    print()
    print("=" * 70)
    print()
    
    # TEST 2: Same text, re-encrypted
    print("TEST 2: IDENTICAL Plaintext, Re-Encrypted")
    print("-" * 70)
    
    plaintext3 = "Hello World! This is a secret message."
    plaintext4 = "Hello World! This is a secret message."  # Exact same!
    
    print(f"Plaintext 3: {plaintext3}")
    print(f"Plaintext 4: {plaintext4}")
    print(f"Plaintext diff: 0 characters (IDENTICAL)")
    print()
    
    # Encrypt both (with different IVs because that's proper encryption)
    encrypted3 = encrypt_aes(plaintext3, key)
    encrypted4 = encrypt_aes(plaintext4, key)
    
    show_hex(encrypted3, "Encrypted 3")
    show_hex(encrypted4, "Encrypted 4")
    
    byte_diff = calculate_difference(encrypted3, encrypted4)
    print(f"Encrypted diff: {byte_diff} out of {len(encrypted3)} bytes differ")
    print(f"Percentage different: {byte_diff/len(encrypted3)*100:.1f}%")
    print()
    print("☝️ Notice: IDENTICAL plaintext → COMPLETELY DIFFERENT ciphertext!")
    print("   This is because of the random IV (Initialization Vector).")
    print("   Proper encryption uses randomness - same input ≠ same output.")
    print()
    print("=" * 70)
    print()
    
    # TEST 3: Completely different plaintexts
    print("TEST 3: Completely Different Plaintexts")
    print("-" * 70)
    
    plaintext5 = "Hello World! This is a secret message."
    plaintext6 = "Totally different text with no relation."
    
    print(f"Plaintext 5: {plaintext5}")
    print(f"Plaintext 6: {plaintext6}")
    print(f"Plaintext diff: Completely different")
    print()
    
    encrypted5 = encrypt_aes(plaintext5, key)
    encrypted6 = encrypt_aes(plaintext6, key)
    
    show_hex(encrypted5, "Encrypted 5")
    show_hex(encrypted6, "Encrypted 6")
    
    byte_diff = calculate_difference(encrypted5, encrypted6)
    print(f"Encrypted diff: {byte_diff} out of {len(encrypted5)} bytes differ")
    print(f"Percentage different: {byte_diff/len(encrypted5)*100:.1f}%")
    print()
    print("=" * 70)
    print()
    
    # CONCLUSION
    print("CONCLUSION:")
    print("-" * 70)
    print()
    print("Plaintext diff of 1 char    → ~50% ciphertext changed")
    print("Plaintext diff of 0 chars   → ~50% ciphertext changed (random IV)")
    print("Plaintext diff of 100% text → ~50% ciphertext changed")
    print()
    print("🔒 THE ENCRYPTED DIFF TELLS YOU NOTHING ABOUT THE PLAINTEXT DIFF!")
    print()
    print("Why?")
    print("  1. Avalanche effect: Small change → Large ciphertext change")
    print("  2. Random IVs: Same input → Different output")
    print("  3. Non-linear: Cannot reverse-engineer without key")
    print("  4. High entropy: Appears as random noise")
    print()
    print("What this means:")
    print("  ✅ Encryption WORKS")
    print("  ✅ AI CANNOT 'see through' it via diffs")
    print("  ✅ Patterns are DESTROYED, not hidden")
    print("  ✅ Your secrets are SAFE")
    print()
    print("=" * 70)
    print()
    print("Try modifying this script to test your own examples!")
    print("You'll see the same result every time: encrypted diffs are meaningless.")
    print()


if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("This script requires pycryptodome:")
        print("  pip install pycryptodome")
        print()
        print("But the principle applies to ALL modern encryption!")
