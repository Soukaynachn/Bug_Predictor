#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

void bubbleSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
            }
        }
    }
}

int main() {
    vector<int> data = {64, 34, 25, 12, 22, 11, 90};
    
    cout << "Unsorted array: ";
    for (int val : data) cout << val << " ";
    cout << endl;
    
    bubbleSort(data);
    
    cout << "Sorted array: ";
    for (int val : data) cout << val << " ";
    cout << endl;
    
    return 0;
}
