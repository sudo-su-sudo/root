#!/usr/bin/env python3
"""
Transformation Vector Analysis

Shows the actual difference vector between plaintext and ciphertext vectors,
and tests whether encryption is additive (can you just add a vector?).

Addresses user's questions:
1. What's the difference between ciphertext vector and plaintext vector?
2. Can you add this difference to plaintext to get ciphertext?
3. What does "APOLLO123" look like as a 128-dimensional vector?
"""

import numpy as np
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad


def bytes_to_vector(data, dim=128):
    """Convert bytes to normalized vector of fixed dimension."""
    vector = np.zeros(dim)
    for i, byte in enumerate(data[:dim]):
        vector[i] = byte / 255.0
    return vector


def text_to_vector(text, dim=128):
    """Convert text to normalized vector."""
    return bytes_to_vector(text.encode(), dim)


def encrypt_aes(plaintext):
    """Encrypt plaintext with AES-256-CBC (random IV each time)."""
    key = b'0123456789abcdef0123456789abcdef'  # 32 bytes for AES-256
    iv = get_random_bytes(16)  # Random IV
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return iv + ciphertext  # Return IV + ciphertext


def print_vector(name, vector, show_all=True):
    """Print vector in readable format."""
    print(f"\n{name}:")
    if show_all:
        # Show in groups of 10
        for i in range(0, len(vector), 10):
            end = min(i + 10, len(vector))
            values = ", ".join([f"{v:.3f}" for v in vector[i:end]])
            print(f"  [{i:3d}-{end-1:3d}]: {values}")
    else:
        # Show first 20
        values = ", ".join([f"{v:.3f}" for v in vector[:20]])
        print(f"  First 20: {values}")
        print(f"  ... (128 total dimensions)")


def main():
    print("=" * 80)
    print("TRANSFORMATION VECTOR ANALYSIS")
    print("=" * 80)
    
    plaintext = "The secret password is: APOLLO123"
    
    # ========================================================================
    # QUESTION 1: What does APOLLO123 look like as a vector?
    # ========================================================================
    print("\n" + "=" * 80)
    print("QUESTION 1: What does 'APOLLO123' look like as a 128-dimensional vector?")
    print("=" * 80)
    
    apollo_vec = text_to_vector("APOLLO123", dim=128)
    print_vector("APOLLO123 Vector (128 dimensions)", apollo_vec, show_all=True)
    
    print("\nCharacter-by-character breakdown:")
    apollo_text = "APOLLO123"
    for i, char in enumerate(apollo_text):
        byte_val = ord(char)
        normalized = byte_val / 255.0
        print(f"  '{char}' (0x{byte_val:02X}) → {normalized:.3f}")
    
    # ========================================================================
    # QUESTION 2: What's the difference vector?
    # ========================================================================
    print("\n" + "=" * 80)
    print("QUESTION 2: What's the difference between plaintext and ciphertext vectors?")
    print("=" * 80)
    
    # Encrypt once
    ciphertext = encrypt_aes(plaintext)
    
    # Convert to vectors
    plaintext_vec = text_to_vector(plaintext, dim=128)
    ciphertext_vec = bytes_to_vector(ciphertext, dim=128)
    
    # Calculate difference
    diff_vec = ciphertext_vec - plaintext_vec
    
    print("\nVectors for encryption #1:")
    print_vector("Plaintext Vector", plaintext_vec, show_all=False)
    print_vector("Ciphertext Vector", ciphertext_vec, show_all=False)
    print_vector("Difference Vector (cipher - plain)", diff_vec, show_all=False)
    
    # ========================================================================
    # QUESTION 3: Can you add the difference to get ciphertext?
    # ========================================================================
    print("\n" + "=" * 80)
    print("QUESTION 3: Can you add diff_vec to plaintext_vec to get ciphertext_vec?")
    print("=" * 80)
    
    reconstructed = plaintext_vec + diff_vec
    matches = np.allclose(reconstructed, ciphertext_vec)
    
    print(f"\nTest: plaintext_vec + diff_vec = ciphertext_vec")
    print(f"Result: {matches} ✓" if matches else f"Result: {matches} ✗")
    print(f"\nFirst 10 values comparison:")
    print(f"  Reconstructed: {[f'{v:.3f}' for v in reconstructed[:10]]}")
    print(f"  Actual cipher: {[f'{v:.3f}' for v in ciphertext_vec[:10]]}")
    print(f"  Match: {'YES' if matches else 'NO'}")
    
    # ========================================================================
    # THE KEY INSIGHT: Does it work for the NEXT encryption?
    # ========================================================================
    print("\n" + "=" * 80)
    print("THE KEY QUESTION: Does the same diff_vec work for the NEXT encryption?")
    print("=" * 80)
    
    print("\nEncrypting the SAME plaintext again (with new random IV)...")
    
    # Encrypt the SAME plaintext again
    ciphertext2 = encrypt_aes(plaintext)
    ciphertext_vec2 = bytes_to_vector(ciphertext2, dim=128)
    
    # Calculate new difference
    diff_vec2 = ciphertext_vec2 - plaintext_vec
    
    print_vector("New Ciphertext Vector", ciphertext_vec2, show_all=False)
    print_vector("New Difference Vector", diff_vec2, show_all=False)
    
    # Compare the two difference vectors
    correlation = np.corrcoef(diff_vec, diff_vec2)[0, 1]
    
    print(f"\nComparison of difference vectors:")
    print(f"  Correlation between diff_vec_1 and diff_vec_2: {correlation:.4f}")
    print(f"  (1.0 = identical, 0.0 = no relationship, -1.0 = opposite)")
    
    if abs(correlation) < 0.1:
        print(f"  → The diff vectors are UNCORRELATED (random!)")
    else:
        print(f"  → The diff vectors have some correlation")
    
    # ========================================================================
    # TEST: Can we use the OLD diff_vec on the NEW ciphertext?
    # ========================================================================
    print("\n" + "=" * 80)
    print("TEST: Can we use the OLD diff_vec to reconstruct from NEW ciphertext?")
    print("=" * 80)
    
    # Try to use old diff_vec to "decrypt" new ciphertext
    attempted_plaintext = ciphertext_vec2 - diff_vec
    matches_new = np.allclose(attempted_plaintext, plaintext_vec)
    
    print(f"\nTest: ciphertext_vec2 - diff_vec_1 = plaintext_vec?")
    print(f"Result: {matches_new} {'✓' if matches_new else '✗'}")
    
    print(f"\nFirst 10 values comparison:")
    print(f"  Attempted plaintext: {[f'{v:.3f}' for v in attempted_plaintext[:10]]}")
    print(f"  Actual plaintext:    {[f'{v:.3f}' for v in plaintext_vec[:10]]}")
    print(f"  Match: {'YES' if matches_new else 'NO'}")
    
    # Show the error
    error = np.linalg.norm(attempted_plaintext - plaintext_vec)
    print(f"\nError magnitude: {error:.3f}")
    print(f"(If it worked, error would be ~0.0)")
    
    # ========================================================================
    # MULTIPLE ENCRYPTIONS: Show that diff is ALWAYS different
    # ========================================================================
    print("\n" + "=" * 80)
    print("MULTIPLE ENCRYPTIONS: Showing diff_vec changes every time")
    print("=" * 80)
    
    print("\nEncrypting the SAME plaintext 5 times...")
    diff_vectors = []
    
    for i in range(5):
        ct = encrypt_aes(plaintext)
        ct_vec = bytes_to_vector(ct, dim=128)
        diff = ct_vec - plaintext_vec
        diff_vectors.append(diff)
        
        print(f"\nEncryption #{i+1}:")
        print(f"  First 10 diff values: {[f'{v:.3f}' for v in diff[:10]]}")
    
    # Calculate correlations between all pairs
    print("\nCorrelations between different diff_vectors:")
    for i in range(len(diff_vectors)):
        for j in range(i + 1, len(diff_vectors)):
            corr = np.corrcoef(diff_vectors[i], diff_vectors[j])[0, 1]
            print(f"  diff_vec_{i+1} vs diff_vec_{j+1}: {corr:.4f}")
    
    # ========================================================================
    # COMPLETE VECTORS: Show ALL 128 dimensions
    # ========================================================================
    print("\n" + "=" * 80)
    print("COMPLETE VECTORS: All 128 dimensions shown")
    print("=" * 80)
    
    print_vector("Complete Plaintext Vector (all 128 dims)", plaintext_vec, show_all=True)
    print_vector("Complete Ciphertext Vector (all 128 dims)", ciphertext_vec, show_all=True)
    print_vector("Complete Difference Vector (all 128 dims)", diff_vec, show_all=True)
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    print("""
YOUR QUESTIONS ANSWERED:

1. "What vector can you add to plaintext to get ciphertext?"
   → For ONE specific encryption: diff_vec = cipher_vec - plain_vec
   → This works: plain_vec + diff_vec = cipher_vec ✓

2. "Can you subtract from ciphertext to get plaintext?"
   → For THAT SAME encryption: plain_vec = cipher_vec - diff_vec ✓
   
3. "What about the NEXT encryption?"
   → NEW diff_vec! Completely different! (correlation ≈ 0)
   → Old diff_vec DOESN'T WORK on new encryption ✗
   
4. "What does APOLLO123 look like as a vector?"
   → Shown above in complete 128-dimensional form
   → Each character converted to normalized value (byte/255)

THE KEY INSIGHT:

Encryption is NOT additive: E(x) ≠ x + k (constant)
Encryption IS non-linear: E(x) = f(x, key, random_IV)

Because of random IVs:
- Same plaintext → Different ciphertext (every time)
- Different diff_vec (every time)
- Cannot learn a fixed transformation
- Cannot "add a vector" to decrypt

That's why encryption works!
""")
    
    print("=" * 80)
    print("EXPERIMENT COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
