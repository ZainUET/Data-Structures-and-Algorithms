#include <iostream>
using namespace std;

class StackArray {
private:
    int* arr;
    int capacity;
    int topIndex;

public:
    StackArray(int size = 100) {
        capacity = size;
        arr = new int[capacity];
        topIndex = -1;
    }
    
    ~StackArray() {
        delete[] arr;
    }
    
    bool isEmpty() {
        return topIndex == -1;
    }
    
    bool isFull() {
        return topIndex == capacity - 1;
    }
    
    void push(int x) {
        if (isFull()) {
            cout << "Stack Overflow!" << endl;
            return;
        }
        arr[++topIndex] = x;
    }
    
    int pop() {
        if (isEmpty()) {
            cout << "Stack Underflow!" << endl;
            return -1;
        }
        return arr[topIndex--];
    }
    
    int peek() {
        if (isEmpty()) {
            cout << "Stack is empty!" << endl;
            return -1;
        }
        return arr[topIndex];
    }
    
    void display() {
        if (isEmpty()) {
            cout << "Stack is empty!" << endl;
            return;
        }
        cout << "Stack (top to bottom): ";
        for (int i = topIndex; i >= 0; i--) {
            cout << arr[i] << " ";
        }
        cout << endl;
    }
    
    string toString() {
        string result = "";
        for (int i = topIndex; i >= 0; i--) {
            result += to_string(arr[i]) + " ";
        }
        return result;
    }
};