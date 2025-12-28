#include <iostream>
#include <list>
using namespace std;

class Stack {
    list<int> ll;
public:
    void push(int val) {
        ll.push_front(val);
    }

    void pop() {
        if (!ll.empty())
            ll.pop_front();
    }

    int top() {
        if (!ll.empty())
            return ll.front();
        return -1;
    }

    bool empty() {
        return ll.empty();
    }
};

int main() {
    Stack s;
    s.push(1);
    s.push(2);
    s.push(3);

    while (!s.empty()) {
        cout << s.top() << " ";
        s.pop();
    }

    return 0;
}
