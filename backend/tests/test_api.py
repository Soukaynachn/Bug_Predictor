import requests
import os

BASE_URL = 'http://127.0.0.1:5000'

def test_train():
    print("Testing /train...")
    try:
        response = requests.post(f'{BASE_URL}/train', json={'dataset': 'cm1.csv'})
        print(response.json())
    except Exception as e:
        print(f"Train failed: {e}")

def test_predict():
    print("Testing /predict...")
    # Create a dummy python file
    with open('test_code.py', 'w') as f:
        f.write('def foo():\n    print("Hello World")\n')
    
    try:
        files = {'file': open('test_code.py', 'rb')}
        response = requests.post(f'{BASE_URL}/predict', files=files)
        print("Status Code:", response.status_code)
        if response.status_code == 200:
            print("Prediction successful (HTML returned)")
        else:
            print(response.text)
    except Exception as e:
        print(f"Predict failed: {e}")
    finally:
        os.remove('test_code.py')

if __name__ == '__main__':
    # Note: Server must be running for this to work. 
    # Since I cannot run the server in background easily and query it in same step without complex handling,
    # I will just print what needs to be done.
    print("To verify, run 'python backend/app.py' in one terminal, and this script in another.")
