from circular_suffix_array import CircularSuffixArray

class BurrowsWheeler:
    """
    Implements Burrows-Wheeler Transform and its inverse using CircularSuffixArray.
    """
    @staticmethod
    def transform(s: str) -> tuple[int, str]:
        """
        Burrows-Wheeler Transform: reorder string to cluster identical characters.
        
        Algorithm:
        1. Generate all circular rotations of input string
        2. Sort rotations lexicographically using CircularSuffixArray
        3. Extract the last character of each sorted rotation
        4. Track which rotation is the original string (returns first index)
        
        Args:
            s: Input string to transform
            
        Returns:
            (first_index, transformed_string):
            - first_index: Position of original string in sorted rotations
            - transformed_string: Last column of sorted rotation matrix
        """
        if s is None:
            raise ValueError("Input string cannot be None")
            
        n = len(s)
        if n == 0:
            return 0, ""
            
        csa = CircularSuffixArray(s)
        first = 0
        last_column = []
        
        for i in range(n):
            idx = csa.index(i)
            # Find the original string's row which has shift of 0 (rotation amount = 0)
            if idx == 0:
                first = i
            
            # In circular representation, the last column character precedes the first column character.
            # For rotation starting at position idx, last char is at position (idx - 1) % n.
            # Using modulo ensures wrap-around: if idx=0, then (0-1) % n = n-1 (last position)
            last_char_idx = (idx - 1) % n
            last_column.append(s[last_char_idx])
            
        return first, "".join(last_column)

    @staticmethod
    def inverse_transform(first: int, transformed: str) -> str:
        """
        Inverse Burrows-Wheeler Transform: reconstruct original string.
        
        Algorithm uses LF (Last-First) mapping property:
        - The last column (input: transformed) sorted becomes the first column
        - Character at position i in last column maps to position LF[i] in next iteration
        - Follow this chain: original_pos → LF[original_pos] → LF[LF[original_pos]] → ...
        
        Implementation uses counting sort with implicit first column construction:
        1. Count character frequencies in transformed (last) column
        2. Build cumulative count array to determine first column positions
        3. Construct nxt[] array: nxt[i] tells us next position in reconstruction
        4. Follow the chain starting from 'first' index for n steps
        
        Args:
            first: Index of original string in sorted rotation matrix
            transformed: Last column of BWT (output from transform())
            
        Returns:
            Original uncompressed string
        """
        if transformed is None:
            raise ValueError("Transformed string cannot be None")
            
        n = len(transformed)
        if n == 0:
            return ""
        if not (0 <= first < n):
            raise IndexError("First index out of bounds")
            
        R = 256  # Restricted to standard and extended ASCII alphabet
        count = [0] * (R + 1)
        
        # Step 1: Count character frequencies in last column (transformed string)
        # count[i] will store cumulative count of characters with ASCII value < i
        for char in transformed:
            char_code = ord(char)
            if char_code >= R:
                raise ValueError("Character out of expected ASCII bounds")
            count[char_code + 1] += 1
            
        # Step 2: Build cumulative count array (prefix sum)
        # After this, count[c] = starting position in first column for character c
        for r in range(R):
            count[r + 1] += count[r]
            
        nxt = [0] * n
        first_col = [''] * n
        
        # Step 3: Construct nxt[] array and implicit first column
        # nxt[i] = position in last column of the next character in reconstruction
        # first_col[i] = character at position i in the sorted first column
        for i in range(n):
            char = transformed[i]
            pos = count[ord(char)]  # Current position in first column for this char
            nxt[pos] = i             # From first[pos], next step is to last[i]
            first_col[pos] = char
            count[ord(char)] += 1    # Increment for next occurrence of this character
            
        # Step 4: Reconstruct original string by following nxt[] chain
        # Start at 'first' (position of original string in sorted matrix)
        # Follow: first → nxt[first] → nxt[nxt[first]] → ... for n steps
        reconstructed = []
        curr = first
        for _ in range(n):
            reconstructed.append(first_col[curr])
            curr = nxt[curr]  # LF mapping: move to next position in reconstruction
            
        return "".join(reconstructed)
