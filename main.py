import sys
from burrows_wheeler import BurrowsWheeler
from move_to_front import MoveToFront

def main():
    original = sys.argv[1] if len(sys.argv) > 1 else "ABRACADABRA!"
    
    print("-" * 50)
    print("BURROWS-WHEELER COMPRESSION PIPELINE TEST")
    print("-" * 50)
    print()
    
    # 1. Burrows-Wheeler Transform
    first, bwt_str = BurrowsWheeler.transform(original)
    
    # 2. MTF Encode execution yielding lists
    mtf_encoded = MoveToFront.encode(bwt_str)
    
    # 3. MTF Decode execution returning equivalent array
    mtf_decoded = MoveToFront.decode(mtf_encoded)
    
    # 4. Inverse BWT logic ensuring lossless nature remains intact
    reconstructed = BurrowsWheeler.inverse_transform(first, mtf_decoded)
    
    # Render Exact Expected Terminal Output Style
    print(f"Original String: {original}")
    print(f"BWT First Index: {first}")
    print(f"BWT Transformed: {bwt_str}")
    print(f"MTF Encoded: {mtf_encoded}")
    print(f"MTF Decoded: {mtf_decoded}")
    print(f"Reconstructed Original: {reconstructed}")
    
    print()
    print("-" * 50)
    
    # Automated Assert Pipeline Correctness Verification
    assert original == reconstructed, "Pipeline reconstruction strictly failed losslessly!"
    assert bwt_str == mtf_decoded, "Move-To-Front execution parity check failed!"
    print("Execution Validated: Perfect lossless end-to-end integration verified.")

if __name__ == "__main__":
    main()
