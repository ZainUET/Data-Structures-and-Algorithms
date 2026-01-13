/**Question No.3 											  [10 marks]
Create an array A of 20 integers. We want to hash elements in A. Use the double hash technique for insertion of elements. Use the given formula to calculate the index of element to be added. Give user the ability to add element on CMD. On each insertion, print the array A.
h(x)=h_1 (x)+i*h_2 (x)
h_1 (x)=x mod 7
h_2 (x)=x mod 3
After adding 10 elements, write the array here which is being displayed on cmd.**/


#include <iostream>
#include <vector>
#include <iomanip>
using namespace std;

class DoubleHashTable {
private:
    static const int SIZE = 20;
    int table[SIZE];
    int count;
    
    int h1(int x) {
        return x % 7;
    }
    
    int h2(int x) {
        int result = x % 3;
        return (result == 0) ? 1 : result;
    }
    
public:
    DoubleHashTable() {
        for (int i = 0; i < SIZE; i++) {
            table[i] = -1;
        }
        count = 0;
    }
    
    bool insert(int x) {
        if (count >= SIZE) {
            cout << "Table is full! Cannot insert " << x << endl;
            return false;
        }
        
        int i = 0;
        while (i < SIZE) {
            int index = (h1(x) + i * h2(x)) % SIZE;
            
            if (table[index] == -1) { 
                table[index] = x;
                count++;
                cout << "Inserted " << x << " at index " << index << endl;
                printTable();
                return true;
            } else {
                cout << "Collision at index " << index << " for value " << x 
                     << ". Trying next probe..." << endl;
                i++;
            }
        }
        
        cout << "Could not insert " << x << " - probing failed after " 
             << SIZE << " attempts" << endl;
        return false;
    }
    
    void printTable() {
        cout << "\nCurrent Hash Table (Size = " << SIZE << "):\n";
        cout << "Index\tValue\n";
        cout << "-----\t-----\n";
        
        for (int i = 0; i < SIZE; i++) {
            cout << setw(3) << i << "\t";
            if (table[i] == -1)
                cout << "Empty";
            else
                cout << table[i];
            cout << endl;
        }
        cout << "------------------------\n";
    }
    
    vector<int> getTableArray() {
        vector<int> result(SIZE);
        for (int i = 0; i < SIZE; i++) {
            result[i] = table[i];
        }
        return result;
    }
    
    void interactiveInsert() {
        cout << "Double Hashing Implementation\n";
        cout << "Formula: h(x) = (x % 7) + i * (x % 3) mod 20\n";
        cout << "Table size: 20\n";
        cout << "Enter up to 10 integers to insert:\n";
        
        int elementsAdded = 0;
        
        while (elementsAdded < 10) {
            cout << "Enter element " << (elementsAdded + 1) << "/10 (or -1 to stop): ";
            int x;
            cin >> x;
            
            if (x == -1) {
                break;
            }
            
            if (insert(x)) {
                elementsAdded++;
            }
        }
        
        cout << "\nFinal array after adding " << elementsAdded << " elements:\n";
        vector<int> finalArray = getTableArray();
        
        cout << "[";
        for (int i = 0; i < SIZE; i++) {
            if (finalArray[i] == -1)
                cout << "NULL";
            else
                cout << finalArray[i];
            
            if (i < SIZE - 1) cout << ", ";
        }
        cout << "]\n";
    }
};

void testWithPredefinedInputs() {
    DoubleHashTable ht;
    
    int testInputs[] = {25, 12, 8, 19, 33, 47, 52, 61, 14, 28};
    int numInputs = sizeof(testInputs) / sizeof(testInputs[0]);
    
    cout << "Simulating insertion of " << numInputs << " elements:\n";
    
    for (int i = 0; i < numInputs; i++) {
        cout << "\nInserting " << testInputs[i] << ":\n";
        ht.insert(testInputs[i]);
    }
    
    cout << "\nFinal hash table array:\n";
    vector<int> finalArray = ht.getTableArray();
    
    cout << "Answer (array after 10 insertions):\n";
    cout << "[";
    for (int i = 0; i < finalArray.size(); i++) {
        if (finalArray[i] == -1)
            cout << "NULL";
        else
            cout << finalArray[i];
        
        if (i < finalArray.size() - 1) cout << ", ";
    }
    cout << "]\n";
}

int main() {
    testWithPredefinedInputs();
    
    return 0;
}