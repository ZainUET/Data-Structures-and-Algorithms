class StackLinkedList {
private:
    Node* top;

public:
    StackLinkedList() {
        top = NULL;
    }
    
    ~StackLinkedList() {
        while (!isEmpty()) {
            pop();
        }
    }
    
    bool isEmpty() {
        return top == NULL;
    }
    
    void push(int x) {
        Node* newNode = new Node(x);
        newNode->next = top;
        top = newNode;
    }
    
    int pop() {
        if (isEmpty()) {
            cout << "Stack Underflow!" << endl;
            return -1;
        }
        Node* temp = top;
        int data = temp->data;
        top = top->next;
        delete temp;
        return data;
    }
    
    int peek() {
        if (isEmpty()) {
            cout << "Stack is empty!" << endl;
            return -1;
        }
        return top->data;
    }
    
    void display() {
        if (isEmpty()) {
            cout << "Stack is empty!" << endl;
            return;
        }
        cout << "Stack (top to bottom): ";
        Node* temp = top;
        while (temp != NULL) {
            cout << temp->data << " ";
            temp = temp->next;
        }
        cout << endl;
    }
    
    string toString() {
        string result = "";
        Node* temp = top;
        while (temp != NULL) {
            result += to_string(temp->data) + " ";
            temp = temp->next;
        }
        return result;
    }
};