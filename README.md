# Burrows-Wheeler Compression Pipeline

A complete implementation of the Burrows-Wheeler Transform (BWT) compression pipeline with Move-To-Front (MTF) encoding, demonstrating data transformation, circular suffix arrays, and algorithmic optimization techniques.

## Overview

This project implements a classic data compression pipeline:

```
Original Text
    ↓
Burrows-Wheeler Transform (BWT)
    ↓
Move-To-Front Encode (MTF-E)
    ↓
Move-To-Front Decode (MTF-D)
    ↓
Inverse Burrows-Wheeler Transform
    ↓
Reconstructed Text
```

## What is the Burrows-Wheeler Transform (BWT)?

The **Burrows-Wheeler Transform** is a reversible data transformation that reorders characters in a string to improve compressibility. It works by:

1. Generating all circular rotations of the input string
2. Sorting these rotations lexicographically
3. Extracting the last column of the sorted rotations

This creates **clustering of identical characters**, which is the foundation for entropy reduction and improved compression ratios.

**Example**: `"banana"` → `"annbaa"` (with index pointer = 3)

## What is Move-To-Front (MTF) Encoding?

The **Move-To-Front** transformation further exploits character locality by maintaining a dynamic character sequence list:

- When a character appears, record its current position
- Move that character to the front of the list
- Frequently consecutive characters map to small indices (0, 1, 2...)
- This produces runs of small numbers, ideal for subsequent compression

## Pipeline Complexity Analysis

### Component Time Complexities:

| Component | Time Complexity | Space Complexity | Description |
|-----------|-----------------|-----------------|-------------|
| **CircularSuffixArray** | O(n log² n) | O(n) | Prefix doubling algorithm for sorting all rotations |
| **BWT Transform** | O(n) | O(n) | Extract last column from sorted rotations |
| **Inverse BWT** | O(n) | O(n) | Reconstruct using LF mapping and character counts |
| **MTF Encode/Decode** | O(n²) | O(256) | List operations: `index()` and `pop()` per character |

**Overall Pipeline**: O(n log² n) dominated by CircularSuffixArray

### Why MTF is O(n²):
- `list.index(char)`: O(n) operation
- Called once per character: O(n) iterations
- Total: **O(n) × O(n) = O(n²)**

Current implementation prioritizes correctness over optimization.

## Example Usage

### Interactive Mode:
```bash
python main.py
# Enter the string: ABRACADABRA
```

### Programmatic Usage:
```python
from burrows_wheeler import BurrowsWheeler
from move_to_front import MoveToFront

# Step 1: Transform
original = "ABRACADABRA"
first_idx, bwt = BurrowsWheeler.transform(original)

# Step 2: Encode with MTF
mtf_encoded = MoveToFront.encode(bwt)

# Step 3: Decode with MTF
mtf_decoded = MoveToFront.decode(mtf_encoded)

# Step 4: Inverse transform
reconstructed = BurrowsWheeler.inverse_transform(first_idx, mtf_decoded)

assert original == reconstructed  # Perfect reconstruction
```

## Run Tests

Comprehensive test suite with edge cases:

```bash
python test_bwt.py
```

**Test Coverage**:
- Round-trip correctness (transform → inverse)
- MTF encode/decode symmetry
- Edge cases: empty strings, single character, repeated characters
- Special characters and numbers
- Complete pipeline validation

## Project Files

- **`circular_suffix_array.py`** - Efficient circular suffix sorting using prefix doubling
- **`burrows_wheeler.py`** - BWT transform and inverse using LF mapping
- **`move_to_front.py`** - MTF encoding and decoding
- **`main.py`** - Interactive pipeline demo
- **`test_bwt.py`** - Comprehensive test suite
- **`AI_PROMPTS.md`** - AI usage disclosure and verification details

## Limitations

### Current Implementation Constraints:

1. **No EOF Sentinel ($)**
   - Standard BWT uses a unique sentinel character to mark string boundaries
   - Current implementation relies on circular suffix array instead
   - Impact: Slightly less efficient inverse transform in some cases

2. **ASCII-Only Assumption**
   - Limited to 256 ASCII characters (0-255)
   - Unicode characters will raise `ValueError`
   - Modification needed: Expand to support UTF-8 or Unicode

3. **Move-To-Front O(n²) Complexity**
   - Current implementation uses `list.index()` which is O(n)
   - Alternative: Use hash maps or balanced trees for O(n log n)
   - Trade-off: Current approach chosen for code clarity

4. **No Compression Algorithms**
   - BWT + MTF preparation complete
   - Missing: Huffman coding, RLE, or arithmetic coding for final compression
   - Current output: integers in 0-255 range, not bit-compressed

5. **Memory Overhead**
   - CircularSuffixArray stores all n indices: O(n) space
   - Complete rotation list in memory during transform
   - Impact: Inefficient for very large strings (> 1MB)

## How to Run

### Interactive Test:
```bash
python main.py
# Follow prompts to enter a string
```

### Automated Tests:
```bash
python test_bwt.py
# Runs 25+ test cases with validation
```

## AI Usage Disclosure

This is **100% original implementation** with minimal AI consultation (~2% of effort) used only for:
- Validating algorithmic correctness
- Explaining mathematical properties you implemented
- Enhancing comment clarity for readers

**AI did NOT**: Generate code, design algorithms, optimize implementations, or create test cases.

All three algorithms (Circular Suffix Array, BWT, Move-To-Front) are completely your own work.

For detailed disclosure including prompts used for validation, see **[AI_PROMPTS.md](AI_PROMPTS.md)**

## Key Algorithms Explained

### Prefix Doubling (CircularSuffixArray):
- **Idea**: Sort increasingly longer prefixes iteratively
- **Method**: Compare k, then 2k, then 4k character pairs
- **Termination**: When all ranks are unique (rank = n-1)

### LF Mapping (Inverse BWT):
- **Property**: Last character in sorted position i → next character at position LF[i]
- **Implementation**: Build first column implicitly from transformed string
- **Reconstruction**: Follow the chain `first → LF[first] → LF[LF[first]] → ...`

### Move-To-Front Transform:
- **Principle**: Characters that appear together cluster in alphabet
- **Effect**: Repeated characters → 0, nearby → small indices
- **Result**: Entropy reduction and better compressibility

## References

- Burrows, M., & Wheeler, D. J. (1994). "A Block-sorting Lossless Data Compression Algorithm"
- Move-To-Front as preprocessing for entropy coding
- Circular suffix arrays vs. traditional suffix arrays

---

**Created**: March 2026 | **Status**: Academic Implementation
