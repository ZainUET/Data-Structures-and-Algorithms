#include <iostream>
using namespace std;

class QueueArray {
private:
    int* arr;
    int capacity;
    int frontIndex;
    int rearIndex;
    int count;

public:
    QueueArray(int size = 100) {
        capacity = size;
        arr = new int[capacity];
        frontIndex = 0;
        rearIndex = -1;
        count = 0;
    }

    ~QueueArray() {
        delete[] arr;
    }

    bool isEmpty() {
        return count == 0;
    }

    bool isFull() {
        return count == capacity;
    }

    void enqueue(int x) {
        if (isFull()) {
            cout << "Queue Overflow!" << endl;
            return;
        }
        rearIndex = (rearIndex + 1) % capacity;
        arr[rearIndex] = x;
        count++;
    }

    int dequeue() {
        if (isEmpty()) {
            cout << "Queue Underflow!" << endl;
            return -1;
        }
        int item = arr[frontIndex];
        frontIndex = (frontIndex + 1) % capacity;
        count--;
        return item;
    }

    int peek() {
        if (isEmpty()) {
            cout << "Queue is empty!" << endl;
            return -1;
        }
        return arr[frontIndex];
    }

    void display() {
        if (isEmpty()) {
            cout << "Queue is empty!" << endl;
            return;
        }
        cout << "Queue (front to rear): ";
        for (int i = 0; i < count; i++) {
            int index = (frontIndex + i) % capacity;
            cout << arr[index] << " ";
        }
        cout << endl;
    }
};

int main() {
    QueueArray q(5);
    q.enqueue(10);
    q.enqueue(20);
    q.enqueue(30);
    q.display();
    cout << "Dequeued: " << q.dequeue() << endl;
    q.display();
    q.enqueue(40);
    q.enqueue(50);
    q.enqueue(60); 
    q.display();
    return 0;
}
