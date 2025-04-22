"""
Test script for LAB color conversion functionality
"""

import sys
from psd2fabric.parser.shape_parser import is_likely_lab_color, lab2rgb

def test_lab_detection():
    """Test the detection of LAB colors"""
    print("Testing LAB color detection:")
    
    # Test case from Stack Overflow
    stack_overflow_case = {
        "red": 1.0343483686447144,
        "green": 0.9487225413322449,
        "blue": -0.12634865939617157,
        "alpha": 100,
    }
    
    test_cases = [
        ([0.5, 0.5, 0.5], False),
        ([128, 128, 128], False),
        ([0.8, 0.5, -0.2], True),
        ([1.2, 0.9, 0.1], True),
        ([stack_overflow_case["red"], stack_overflow_case["green"], stack_overflow_case["blue"]], True)
    ]
    
    for values, expected in test_cases:
        result = is_likely_lab_color(values)
        print(f"Values: {values}")
        print(f"Detected as LAB: {result} (Expected: {expected})")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print("-" * 40)

def test_lab_conversion():
    """Test the conversion of LAB colors to RGB"""
    print("\nTesting LAB to RGB conversion:")
    
    # Test case from Stack Overflow
    stack_overflow_case = {
        "red": 1.0343483686447144,
        "green": 0.9487225413322449,
        "blue": -0.12634865939617157,
        "alpha": 100,
    }
    
    # Convert to LAB values [L, a, b]
    lab_values = [stack_overflow_case["green"], stack_overflow_case["blue"], stack_overflow_case["red"]]
    print(f"LAB values: {lab_values}")
    
    # Convert to RGB
    rgb_values = lab2rgb(lab_values)
    print(f"RGB values: {[int(v) for v in rgb_values]}")
    
    # Convert to hex
    r, g, b = [int(v) for v in rgb_values]
    hex_color = f"#{r:02x}{g:02x}{b:02x}"
    print(f"Hex color: {hex_color}")
    
    # Compare with expected yellow color from Stack Overflow post (approximately)
    expected_color = "#fff200"  # Yellow color mentioned in Stack Overflow
    similarity = "Close to expected" if hex_color[:3] == "#ff" else "Different from expected"
    print(f"Similarity to expected yellow: {similarity}")
    print("-" * 40)

if __name__ == "__main__":
    print("LAB Color Conversion Test")
    print("=" * 40)
    test_lab_detection()
    test_lab_conversion()
