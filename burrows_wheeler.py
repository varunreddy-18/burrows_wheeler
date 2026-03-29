from circular_suffix_array import CircularSuffixArray

class BurrowsWheeler:
    """
    Implements Burrows-Wheeler Transform and its inverse using CircularSuffixArray.
    """
    @staticmethod
    def transform(s: str) -> tuple[int, str]:
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
            # Find the original string's row which has shift of 0
            if idx == 0:
                first = i
            
            # In circular representation, the last column character precedes the first column character
            last_char_idx = (idx - 1) % n
            last_column.append(s[last_char_idx])
            
        return first, "".join(last_column)

    @staticmethod
    def inverse_transform(first: int, transformed: str) -> str:
        if transformed is None:
            raise ValueError("Transformed string cannot be None")
            
        n = len(transformed)
        if n == 0:
            return ""
        if not (0 <= first < n):
            raise IndexError("First index out of bounds")
            
        R = 256 # Restricted to standard and extended ASCII alphabet
        count = [0] * (R + 1)
        
        # 1. Frequency counting of each character in transformed string
        for char in transformed:
            char_code = ord(char)
            if char_code >= R:
                raise ValueError("Character out of expected ASCII bounds")
            count[char_code + 1] += 1
            
        # 2. Cumulates matrix construction to find pointer ranges in sorted column
        for r in range(R):
            count[r + 1] += count[r]
            
        nxt = [0] * n
        first_col = [''] * n
        
        # 3. Synchronously construct the next[] index array and populate the implicit sorted first column
        for i in range(n):
            char = transformed[i]
            pos = count[ord(char)]
            nxt[pos] = i
            first_col[pos] = char
            count[ord(char)] += 1
            
        # 4. Traverse next[] routing map to decode the original un-transformed sequence sequentially
        reconstructed = []
        curr = first
        for _ in range(n):
            reconstructed.append(first_col[curr])
            curr = nxt[curr]
            
        return "".join(reconstructed)
