class MoveToFront:
    
    @staticmethod
    def encode(s: str) -> list[int]:
        if s is None:
            raise ValueError("Input string cannot be None")
            
        # Initializes standard sequences indexing standard 0-255 bounds
        seq = list(range(256))
        encoded = []
        
        for char in s:
            idx = seq.index(ord(char))
            encoded.append(idx)
            
            # Pop element and smoothly insert directly to front for density scaling priority
            val = seq.pop(idx)
            seq.insert(0, val)
            
        return encoded

    @staticmethod
    def decode(encoded: list[int]) -> str:
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
