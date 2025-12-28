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

int main() {
    StackArray s(5);
    s.push(10);
    s.push(20);
    s.push(30);
    s.display();

    cout << "Top element: " << s.peek() << endl;
    cout << "Popped: " << s.pop() << endl;
    s.display();

    s.push(40);
    s.push(50);
    s.push(60); 
    s.display();

    return 0;
}
