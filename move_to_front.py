class MoveToFront:
    """
    Move-To-Front (MTF) Transform: preprocess data to improve subsequent compression.
    
    Algorithm Principle:
    Maintain a dynamic sequence of all 256 ASCII characters. When encoding or decoding:
    1. Find the position of the current character
    2. Output the position (encoding) or character at position (decoding)
    3. Move that character to the front
    
    Effect: Characters that appear consecutively will have small indices (0, 1, 2...)
    This creates runs of small numbers, dramatically improving compressibility.
    
    Time Complexity: O(n²)
    - Reason: list.index(element) is O(256) = O(1) in practice, but actually O(n)
    - list.pop(index) + list.insert(0, val) are O(256) = O(1) amortized
    - However, for full correctness: O(n) characters × O(n) list operations = O(n²)
    - More precisely: O(n × 256) = O(n) since alphabet size is constant
    
    Space Complexity: O(256) = O(1) - fixed alphabet size
    
    Alternative Optimizations (not implemented):
    - Use HashMap for O(n log n): {char: index, index: char}
    - Use Linked List for O(n): element deletion O(1), but list access O(n)
    - Current approach: clarity over optimization
    """
    
    @staticmethod
    def encode(s: str) -> list[int]:
        """
        Encode string using Move-To-Front transform.
        
        Algorithm:
        - Maintain sequence: [0, 1, 2, ..., 255] (all ASCII characters by code)
        - For each character in input:
          1. Find its position in sequence: list.index(ord(char))
          2. Append position to output
          3. Move character to front: pop from current position, insert at 0
        
        Complexity:
        - list.index(): O(256) ≈ O(1) in practice
        - list.pop(): O(1) at end, O(n) worst case
        - list.insert(0, x): O(n) to shift elements
        - Per character: ~O(1) since alphabet is fixed size
        - Total: O(n) for n characters
        
        Args:
            s: String to encode
            
        Returns:
            List of integers (0-255) representing indices in moving sequence
        """
        if s is None:
            raise ValueError("Input string cannot be None")
            
        # Initializes standard sequences indexing standard 0-255 bounds
        seq = list(range(256))
        encoded = []
        
        for char in s:
            # Find position of character's ASCII code in sequence
            # PERFORMANCE NOTE: list.index() scans linearly - could use HashMap
            idx = seq.index(ord(char))
            encoded.append(idx)
            
            # Pop element from position idx and insert at front for next iteration
            # OPTIMIZATION OPPORTUNITY: Linked list for O(1) removal
            val = seq.pop(idx)
            seq.insert(0, val)
            
        return encoded

    @staticmethod
    def decode(encoded: list[int]) -> str:
        """
        Decode Move-To-Front encoded list back to original string.
        
        Algorithm:
        - Maintain same sequence: [0, 1, 2, ..., 255]
        - For each index in encoded list:
          1. Convert value at sequence[index] to character: chr(val)
          2. Append character to output
          3. Move that character to front (same as encode)
        
        Note: Encode and decode are symmetric - same sequence maintenance
        
        Args:
            encoded: List of indices (output from encode())
            
        Returns:
            Original string before encoding
        """
        if encoded is None:
            raise ValueError("Encoded list cannot be None")
            
        seq = list(range(256))
        decoded = []
        
        for idx in encoded:
            val = seq[idx]
            decoded.append(chr(val))
            
            # Map elements backwards via shifting decoding
            seq.pop(idx)
            seq.insert(0, val)
            
        return "".join(decoded)
