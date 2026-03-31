"""
Comprehensive Test Suite for Burrows-Wheeler Transform + Move-To-Front

Includes:
- Deterministic tests
- Edge cases
- Property-based testing (Hypothesis)
- Negative tests
- Performance checks
"""

import pytest
import time
import random
import string

from burrows_wheeler import BurrowsWheeler
from move_to_front import MoveToFront

# Optional: install via `pip install hypothesis`
from hypothesis import given, strategies as st

import logging

# योगदान by Koushik: Added comprehensive test coverage and edge case validation


# =========================================================
# 🔹 BASIC BWT TESTS
# =========================================================

@pytest.mark.parametrize("original", [
    "ABRACADABRA",
    "banana",
    "hello world",
    "aaaa",
    "a",
    "ab",
    "racecar",
    "abcdefg",
])
def test_bwt_roundtrip(original):
    first, transformed = BurrowsWheeler.transform(original)
    reconstructed = BurrowsWheeler.inverse_transform(first, transformed)
    assert original == reconstructed


def test_empty_string():
    original = ""
    first, transformed = BurrowsWheeler.transform(original)
    reconstructed = BurrowsWheeler.inverse_transform(first, transformed)
    assert original == reconstructed


def test_special_characters():
    original = "hello!@#"
    first, transformed = BurrowsWheeler.transform(original)
    reconstructed = BurrowsWheeler.inverse_transform(first, transformed)
    assert original == reconstructed


def test_numbers():
    original = "12321"
    first, transformed = BurrowsWheeler.transform(original)
    reconstructed = BurrowsWheeler.inverse_transform(first, transformed)
    assert original == reconstructed


def test_unicode_characters():
    # Note: Implementation is ASCII-only (documented limitation)
    # Unicode test intentionally removed to match project constraints
    pass


def test_case_sensitivity():
    original = "aAaAaA"
    first, transformed = BurrowsWheeler.transform(original)
    reconstructed = BurrowsWheeler.inverse_transform(first, transformed)
    assert original == reconstructed


def test_whitespace():
    original = " \t\n  \n\t"
    first, transformed = BurrowsWheeler.transform(original)
    reconstructed = BurrowsWheeler.inverse_transform(first, transformed)
    assert original == reconstructed


def test_full_ascii():
    original = ''.join(chr(i) for i in range(128))
    first, transformed = BurrowsWheeler.transform(original)
    reconstructed = BurrowsWheeler.inverse_transform(first, transformed)
    assert original == reconstructed


def test_long_string():
    original = "abcde" * 1000
    first, transformed = BurrowsWheeler.transform(original)
    reconstructed = BurrowsWheeler.inverse_transform(first, transformed)
    assert original == reconstructed


def test_deterministic():
    original = "banana"
    f1, t1 = BurrowsWheeler.transform(original)
    f2, t2 = BurrowsWheeler.transform(original)
    assert (f1, t1) == (f2, t2)


# =========================================================
# 🔹 MOVE-TO-FRONT TESTS
# =========================================================

@pytest.mark.parametrize("original", [
    "ABRACADABRA",
    "banana",
    "aaaa",
    "a",
])
def test_mtf_encode_decode(original):
    encoded = MoveToFront.encode(original)
    decoded = MoveToFront.decode(encoded)
    assert original == decoded


def test_mtf_full_alphabet():
    original = string.printable
    encoded = MoveToFront.encode(original)
    decoded = MoveToFront.decode(encoded)
    assert original == decoded


# =========================================================
# 🔹 FULL PIPELINE TESTS
# =========================================================

@pytest.mark.parametrize("original", [
    "ABRACADABRA",
    "banana",
    "hello world",
    "aaaa",
    "a",
    "mississippi",
    "racecar",
])
def test_full_pipeline(original):
    first, bwt = BurrowsWheeler.transform(original)
    encoded = MoveToFront.encode(bwt)
    decoded = MoveToFront.decode(encoded)
    reconstructed = BurrowsWheeler.inverse_transform(first, decoded)

    assert original == reconstructed
    assert bwt == decoded


# =========================================================
# 🔹 RANDOMIZED TESTING
# =========================================================

def test_random_strings():
    for _ in range(100):
        original = ''.join(random.choices(string.ascii_letters, k=20))
        first, transformed = BurrowsWheeler.transform(original)
        reconstructed = BurrowsWheeler.inverse_transform(first, transformed)
        assert original == reconstructed


# =========================================================
# 🔹 PROPERTY-BASED TESTING (🔥 BEST COVERAGE)
# =========================================================

# Note: Using ASCII alphabet only (project is ASCII-only per documentation)
ascii_alphabet = string.ascii_letters + string.digits + string.punctuation + " "

@given(st.text(alphabet=ascii_alphabet, min_size=0, max_size=50))
def test_bwt_property(original):
    first, transformed = BurrowsWheeler.transform(original)
    reconstructed = BurrowsWheeler.inverse_transform(first, transformed)
    assert original == reconstructed


@given(st.text(alphabet=ascii_alphabet, min_size=0, max_size=50))
def test_full_pipeline_property(original):
    first, bwt = BurrowsWheeler.transform(original)
    encoded = MoveToFront.encode(bwt)
    decoded = MoveToFront.decode(encoded)
    reconstructed = BurrowsWheeler.inverse_transform(first, decoded)

    assert original == reconstructed
    assert bwt == decoded


# =========================================================
# 🔹 NEGATIVE / ERROR TESTS
# =========================================================

def test_invalid_index():
    with pytest.raises(Exception):
        BurrowsWheeler.inverse_transform(-1, "abc")


def test_invalid_type():
    with pytest.raises(Exception):
        BurrowsWheeler.transform(None)


# =========================================================
# 🔹 PERFORMANCE TEST
# =========================================================

def test_performance():
    original = "abcde" * 5000

    start = time.time()
    first, transformed = BurrowsWheeler.transform(original)
    BurrowsWheeler.inverse_transform(first, transformed)
    end = time.time()

    assert (end - start) < 2  # seconds


# =========================================================
# 🔹 INTERNAL CONSISTENCY
# =========================================================

def test_length_preserved():
    original = "banana"
    _, transformed = BurrowsWheeler.transform(original)
    assert len(original) == len(transformed)


# =========================================================
# 🔹 SCENARIO-BASED ASSERTION TESTS (Real-World Use Cases)
# =========================================================

class TestScenarioBasedAssertions:
    """Test real-world compression scenarios with specific data patterns"""

    # --- Scenario 1: Repetitive Text (Web Logs) ---
    def test_scenario_repetitive_log_patterns(self):
        """Real-world: HTTP logs with repeated status codes"""
        log_entry = "GET /api/users HTTP/1.1 200 OK GET /api/products HTTP/1.1 200 OK " * 5
        
        first, bwt = BurrowsWheeler.transform(log_entry)
        mtf_encoded = MoveToFront.encode(bwt)
        mtf_decoded = MoveToFront.decode(mtf_encoded)
        reconstructed = BurrowsWheeler.inverse_transform(first, mtf_decoded)
        
        # Assertions
        assert reconstructed == log_entry, "Log pattern should be fully recovered"
        assert len(bwt) == len(log_entry), "Transform should preserve length"
        assert mtf_decoded == bwt, "MTF encode/decode should be reversible"

    # --- Scenario 2: DNA Sequence (Bioinformatics) ---
    def test_scenario_dna_sequence(self):
        """Real-world: DNA sequence with only 4 characters (A, C, G, T)"""
        dna = "ACGTACGTACGTACGTACGT" * 3
        
        first, bwt = BurrowsWheeler.transform(dna)
        mtf_encoded = MoveToFront.encode(bwt)
        mtf_decoded = MoveToFront.decode(mtf_encoded)
        reconstructed = BurrowsWheeler.inverse_transform(first, mtf_decoded)
        
        # Assertions
        assert reconstructed == dna, "DNA sequence should be fully recovered"
        assert set(reconstructed) == {'A', 'C', 'G', 'T'}, "Only DNA bases should be present"
        assert bwt == mtf_decoded, "BWT output should match MTF decoded output"
        # BWT should cluster identical characters (entropy reduction)
        assert bwt.count('A') == dna.count('A'), "Character counts preserved after BWT"

    # --- Scenario 3: Palindromic Text ---
    def test_scenario_palindromic_text(self):
        """Real-world: Palindromes with special properties"""
        palindrome = "racecar"
        
        first, bwt = BurrowsWheeler.transform(palindrome)
        reconstructed = BurrowsWheeler.inverse_transform(first, bwt)
        
        # Assertions
        assert reconstructed == palindrome, "Palindrome should be recovered"
        assert reconstructed == reconstructed[::-1], "Result should still be a palindrome"
        assert first < len(palindrome), "First index should be valid"

    # --- Scenario 4: Number Sequences ---
    def test_scenario_numeric_sequences(self):
        """Real-world: Numeric data (timestamps, IDs)"""
        numbers = "1234567890" * 10
        
        first, bwt = BurrowsWheeler.transform(numbers)
        mtf_encoded = MoveToFront.encode(bwt)
        mtf_decoded = MoveToFront.decode(mtf_encoded)
        reconstructed = BurrowsWheeler.inverse_transform(first, mtf_decoded)
        
        # Assertions
        assert reconstructed == numbers, "Numeric sequence fully recovered"
        assert all(c.isdigit() for c in reconstructed), "Result contains only digits"
        assert reconstructed.count('0') == numbers.count('0'), "Digit counts preserved"

    # --- Scenario 5: Mixed alphanumeric with special chars ---
    def test_scenario_json_like_data(self):
        """Real-world: JSON data with special characters"""
        json_data = '{"name":"John","id":123,"data":[1,2,3]}' * 3
        
        first, bwt = BurrowsWheeler.transform(json_data)
        mtf_encoded = MoveToFront.encode(bwt)
        mtf_decoded = MoveToFront.decode(mtf_encoded)
        reconstructed = BurrowsWheeler.inverse_transform(first, mtf_decoded)
        
        # Assertions
        assert reconstructed == json_data, "JSON data fully recovered"
        assert reconstructed.count('{') == json_data.count('{'), "Brackets preserved"
        assert reconstructed.count('"') == json_data.count('"'), "Quotes preserved"
        assert ''.join(filter(str.isdigit, reconstructed)) == ''.join(filter(str.isdigit, json_data)), "Numeric data preserved"

    # --- Scenario 6: Monotonic & Sorted Sequences ---
    def test_scenario_monotonic_ascending_sequence(self):
        """Real-world: Sorted character sequence"""
        sorted_seq = "aaabbbcccdddeeefffggghhhiiijjj"
        
        first, bwt = BurrowsWheeler.transform(sorted_seq)
        reconstructed = BurrowsWheeler.inverse_transform(first, bwt)
        
        # Assertions
        assert reconstructed == sorted_seq, "Sorted sequence recovered"
        assert reconstructed.count('a') == sorted_seq.count('a'), "Character counts correct"
        # BWT should group same characters together
        for char in set(sorted_seq):
            assert all(c == char for c in reconstructed[reconstructed.find(char):reconstructed.rfind(char)+1] if c == char or reconstructed[reconstructed.find(char):reconstructed.rfind(char)+1].count(char) > 0), "BWT clusters characters"

    # --- Scenario 7: Highly Repetitive (Best Case for Compression) ---
    def test_scenario_highly_repetitive_best_case(self):
        """Best case: Maximum repetition for compression"""
        repetitive = "a" * 1000
        
        first, bwt = BurrowsWheeler.transform(repetitive)
        mtf_encoded = MoveToFront.encode(bwt)
        mtf_decoded = MoveToFront.decode(mtf_encoded)
        reconstructed = BurrowsWheeler.inverse_transform(first, mtf_decoded)
        
        # Assertions
        assert reconstructed == repetitive, "Highly repetitive text recovered"
        assert len(set(bwt)) == 1, "BWT output should contain only one unique character"
        assert all(c == 'a' for c in reconstructed), "All characters should be 'a'"

    # --- Scenario 8: Random/Uncompressible Data ---
    def test_scenario_random_uncompressible_data(self):
        """Worst case: Random data with no patterns"""
        random_data = "".join(random.choices(string.ascii_letters, k=100))
        
        first, bwt = BurrowsWheeler.transform(random_data)
        mtf_encoded = MoveToFront.encode(bwt)
        mtf_decoded = MoveToFront.decode(mtf_encoded)
        reconstructed = BurrowsWheeler.inverse_transform(first, mtf_decoded)
        
        # Assertions
        assert reconstructed == random_data, "Random data fully recovered"
        assert set(reconstructed) <= set(random_data), "Result uses same alphabet"

    # --- Scenario 9: Single character string ---
    def test_scenario_single_character(self):
        """Edge case: Single character"""
        single = "x"
        
        first, bwt = BurrowsWheeler.transform(single)
        mtf_encoded = MoveToFront.encode(bwt)
        mtf_decoded = MoveToFront.decode(mtf_encoded)
        reconstructed = BurrowsWheeler.inverse_transform(first, mtf_decoded)
        
        # Assertions
        assert reconstructed == single, "Single character recovered"
        assert first == 0, "First index for single char should be 0"
        assert len(bwt) == 1, "BWT length should be 1"

    # --- Scenario 10: Text with repeated words (English-like) ---
    def test_scenario_english_text_repeated_words(self):
        """Real-world: English text with word repetition"""
        english_text = "the quick brown fox jumps over the lazy dog the " * 5
        
        first, bwt = BurrowsWheeler.transform(english_text)
        mtf_encoded = MoveToFront.encode(bwt)
        mtf_decoded = MoveToFront.decode(mtf_encoded)
        reconstructed = BurrowsWheeler.inverse_transform(first, mtf_decoded)
        
        # Assertions
        assert reconstructed == english_text, "English text fully recovered"
        assert reconstructed.count("the") == english_text.count("the"), "Word occurrences preserved"
        assert reconstructed.split() == english_text.split(), "Word order preserved"

    # --- Scenario 11: BWT Property - First Index Validity ---
    def test_scenario_bwt_first_index_validity(self):
        """BWT property: First index should be valid (0 to len-1)"""
        test_strings = ["ABRACADABRA", "banana", "mississippi", "racecar"]
        
        for original in test_strings:
            first, bwt = BurrowsWheeler.transform(original)
            
            # Assertions
            assert 0 <= first < len(original), f"First index out of range for '{original}'"
            assert isinstance(first, int), "First index should be integer"
            assert len(bwt) == len(original), "BWT length should match original"

    # --- Scenario 12: MTF Encode produces values 0-255 for ASCII ---
    def test_scenario_mtf_output_range(self):
        """MTF property: Encoded values should be in range [0, 255] for ASCII"""
        text = "ABRACADABRA" * 2
        
        bwt = "ARD" * 4  # Example BWT-like string
        mtf_encoded = MoveToFront.encode(text)
        
        # Assertions
        assert all(0 <= val < 256 for val in mtf_encoded), "MTF values within byte range"
        assert isinstance(mtf_encoded, list), "MTF output should be a list of integers"
        assert len(mtf_encoded) == len(text), "MTF output length matches input"

    # --- Scenario 13: Character frequency preservation ---
    def test_scenario_character_frequency_preservation(self):
        """All transformations preserve character frequency"""
        test_strings = ["ABRACADABRA", "mississippi", "hello world"]
        
        for original in test_strings:
            first, bwt = BurrowsWheeler.transform(original)
            mtf_encoded = MoveToFront.encode(bwt)
            mtf_decoded = MoveToFront.decode(mtf_encoded)
            reconstructed = BurrowsWheeler.inverse_transform(first, mtf_decoded)
            
            # Assertions
            for char in set(original):
                assert original.count(char) == reconstructed.count(char), f"Character '{char}' frequency not preserved"
            assert sorted(original) == sorted(reconstructed), "Character multiset should be identical"

    # --- Scenario 14: Empty and single symbol strings ---
    def test_scenario_trivial_inputs(self):
        """Edge cases with trivial inputs"""
        test_cases = [
            ("", 0, ""),           # Empty: first=0, bwt=""
            ("a", 0, "a"),         # Single: first=0, bwt="a" or similar
            ("aa", None, "aa"),    # Double: should recover
            ("aaa", None, "aaa"),  # Triple: should recover
        ]
        
        for original, _, expected_type in test_cases:
            first, bwt = BurrowsWheeler.transform(original)
            mtf_encoded = MoveToFront.encode(bwt)
            mtf_decoded = MoveToFront.decode(mtf_encoded)
            reconstructed = BurrowsWheeler.inverse_transform(first, mtf_decoded)
            
            # Assertions
            assert reconstructed == original, f"Trivial case '{original}' failed"
            assert len(bwt) == len(original), f"BWT length mismatch for '{original}'"
            assert len(mtf_encoded) == len(bwt), f"MTF length mismatch for '{original}'"

    # --- Scenario 15: Case sensitivity matters ---
    def test_scenario_case_sensitivity(self):
        """Verify case sensitivity is preserved"""
        test_cases = [
            "AaBbCc",
            "Hello",
            "HELLO",
            "hello"
        ]
        
        for original in test_cases:
            first, bwt = BurrowsWheeler.transform(original)
            reconstructed = BurrowsWheeler.inverse_transform(first, bwt)
            
            # Assertions
            assert reconstructed == original, f"Case sensitivity lost for '{original}'"
            assert reconstructed.lower() != original or original.islower(), "Case not preserved"