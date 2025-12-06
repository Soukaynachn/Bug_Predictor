import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.core.features import FeatureExtractor

def test_multilang():
    extractor = FeatureExtractor()
    
    # Test Python (Radon)
    print("Testing Python (Radon)...")
    py_code = """
def hello():
    print("Hello")
    if True:
        print("World")
"""
    py_features = extractor.extract_from_code(py_code, "test.py")
    print(f"Python Features: {py_features}")
    assert py_features['cyclomatic_complexity'] > 0
    
    # Test Java (Lizard)
    print("\nTesting Java (Lizard)...")
    java_code = """
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World");
        if (args.length > 0) {
            System.out.println("Args");
        }
    }
}
"""
    java_features = extractor.extract_from_code(java_code, "test.java")
    print(f"Java Features: {java_features}")
    assert java_features['cyclomatic_complexity'] > 0
    assert java_features['loc'] > 0

    # Test C++ (Lizard)
    print("\nTesting C++ (Lizard)...")
    cpp_code = """
#include <iostream>
using namespace std;

int main() {
    cout << "Hello World";
    for(int i=0; i<10; i++) {
        cout << i;
    }
    return 0;
}
"""
    cpp_features = extractor.extract_from_code(cpp_code, "test.cpp")
    print(f"C++ Features: {cpp_features}")
    assert cpp_features['cyclomatic_complexity'] > 0
    
    print("\n✅ All multi-language tests passed!")

if __name__ == "__main__":
    test_multilang()
