class CircularSuffixArray:
    """
    Circular Suffix Array representation for the Burrows-Wheeler transform.
    Constructs the sorted suffix array using the prefix doubling algorithm.
    """
    def __init__(self, s: str):
        if s is None:
            raise ValueError("Input string cannot be None")
        
        self._length = len(s)
        if self._length == 0:
            self._indices = []
            return

        n = self._length
        
        # Initialize ranks based on standard character ASCII values
        ranks = [ord(c) for c in s]
        indices = list(range(n))
        
        k = 1
        while k < n:
            # Sort indices based on rank pairs from previous iteration length k
            indices.sort(key=lambda i: (ranks[i], ranks[(i + k) % n]))
            
            # Recompute ranks according to new sorted pairs
            new_ranks = [0] * n
            rank = 0
            for i in range(1, n):
                prev = indices[i - 1]
                curr = indices[i]
                
                prev_pair = (ranks[prev], ranks[(prev + k) % n])
                curr_pair = (ranks[curr], ranks[(curr + k) % n])
                
                if prev_pair != curr_pair:
                    rank += 1
                new_ranks[curr] = rank
            
            ranks = new_ranks
            k *= 2
            
            # Fully sorted once all suffix string ranks are uniquely identified
            if rank == n - 1:
                break
                
        self._indices = indices

    def length(self) -> int:
        """Returns the length of the string."""
        return self._length

    def index(self, i: int) -> int:
        """Returns the index in the original string of the ith sorted suffix."""
        if not (0 <= i < self._length):
            raise IndexError("Index out of bounds")
        return self._indices[i]
