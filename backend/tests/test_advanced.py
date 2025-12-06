import requests
import os
import zipfile

BASE_URL = 'http://127.0.0.1:5000'

def test_paste_code():
    print("\nTesting Paste Code (Java)...")
    java_code = """
    public class HelloWorld {
        public static void main(String[] args) {
            System.out.println("Hello, World");
            if (true) {
                System.out.println("Branch");
            }
        }
    }
    """
    try:
        response = requests.post(f'{BASE_URL}/predict', data={'code_text': java_code})
        if response.status_code == 200:
            print("Paste Code Success!")
        else:
            print(f"Paste Code Failed: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

def test_zip_upload():
    print("\nTesting ZIP Upload...")
    # Create dummy zip
    with zipfile.ZipFile('test_archive.zip', 'w') as z:
        z.writestr('test.py', 'def foo(): pass')
        z.writestr('test.js', 'function bar() { return 1; }')
    
    try:
        with open('test_archive.zip', 'rb') as f:
            files = {'file': f}
            response = requests.post(f'{BASE_URL}/predict', files=files)
            if response.status_code == 200:
                print("ZIP Upload Success!")
            else:
                print(f"ZIP Upload Failed: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if os.path.exists('test_archive.zip'):
            os.remove('test_archive.zip')

if __name__ == '__main__':
    test_paste_code()
    test_zip_upload()
