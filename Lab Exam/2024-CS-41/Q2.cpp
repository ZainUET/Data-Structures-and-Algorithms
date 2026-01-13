/**Question No.2 											    
Implement Insertion sort, such that your algorithms sort the elements on even indexes only and leave 
the odd indexes without any change. Pass start, end  and array as parameter.**/

#include <iostream>
#include <vector>
using namespace std;

void insertionSortEvenIndices(int arr[], int start, int end) {
    vector<int> evenIndices;
    
    for (int i = start; i <= end; i++) {
        if (i % 2 == 0) { 
            evenIndices.push_back(i);
        }
    }
    
    for (int i = 1; i < evenIndices.size(); i++) {
        int currentIdx = evenIndices[i];
        int currentVal = arr[currentIdx];
        int j = i - 1;
        
        while (j >= 0 && arr[evenIndices[j]] > currentVal) {
            arr[evenIndices[j + 1]] = arr[evenIndices[j]];
            j--;
        }
        
        arr[evenIndices[j + 1]] = currentVal;
    }
}

void insertionSortEvenIndicesAlt(int arr[], int start, int end) {    vector<int> evenValues;
    vector<int> evenIndices;
    
    for (int i = start; i <= end; i++) {
        if (i % 2 == 0) {
            evenValues.push_back(arr[i]);
            evenIndices.push_back(i);
        }
    }
    
    for (int i = 1; i < evenValues.size(); i++) {
        int key = evenValues[i];
        int j = i - 1;
        
        while (j >= 0 && evenValues[j] > key) {
            evenValues[j + 1] = evenValues[j];
            j--;
        }
        evenValues[j + 1] = key;
    }
    
    for (int i = 0; i < evenIndices.size(); i++) {
        arr[evenIndices[i]] = evenValues[i];
    }
}

void printArray(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        cout << arr[i] << " ";
    }
    cout << endl;
}

int main() {
    int arr[] = {9, 1, 5, 2, 8, 3, 7, 4, 6, 5};
    int n = sizeof(arr) / sizeof(arr[0]);
    
    cout << "Original array: ";
    printArray(arr, n);
    
    insertionSortEvenIndices(arr, 0, n - 1);
    
    cout << "After sorting even indices: ";
    printArray(arr, n);

    cout << "\nExplanation:\n";
    cout << "Even indices (0, 2, 4, 6, 8): ";
    for (int i = 0; i < n; i += 2) {
        cout << arr[i] << " ";
    }
    cout << "\nOdd indices remain unchanged.\n";
    
    return 0;
}