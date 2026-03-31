from burrows_wheeler import BurrowsWheeler
from move_to_front import MoveToFront

def main():
    # Take input directly from user (no quotes needed)
    original = input("Enter the string: ")
    
    print("-" * 50)
    print("BURROWS-WHEELER COMPRESSION PIPELINE TEST")
    print("-" * 50)
    print()
    
    # 1. Burrows-Wheeler Transform
    first, bwt_str = BurrowsWheeler.transform(original)
    
    # 2. MTF Encode
    mtf_encoded = MoveToFront.encode(bwt_str)
    
    # 3. MTF Decode
    mtf_decoded = MoveToFront.decode(mtf_encoded)
    
    # 4. Inverse BWT
    reconstructed = BurrowsWheeler.inverse_transform(first, mtf_decoded)
    
    # Output
    print(f"Original String: {original}")
    print(f"BWT First Index: {first}")
    print(f"BWT Transformed: {bwt_str}")
    print(f"MTF Encoded: {mtf_encoded}")
    print(f"MTF Decoded: {mtf_decoded}")
    print(f"Reconstructed Original: {reconstructed}")
    
    print()
    print("-" * 50)
    
    # Validation
    assert original == reconstructed, "Pipeline reconstruction strictly failed losslessly!"
    assert bwt_str == mtf_decoded, "Move-To-Front execution parity check failed!"
    print("Execution Validated: Perfect lossless end-to-end integration verified.")

if __name__ == "__main__":
    main()