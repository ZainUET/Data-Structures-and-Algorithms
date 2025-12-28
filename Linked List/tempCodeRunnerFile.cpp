class DoublyNode {
public:
    int data;
    DoublyNode* next;
    DoublyNode* prev;
    
    DoublyNode(int x) {
        data = x;
        next = NULL;
        prev = NULL;
    }
};

class DoublyLinkList {
private:
    DoublyNode* head;
    DoublyNode* tail;

public:
    DoublyLinkList() {
        head = tail = NULL;
    }
    
    ~DoublyLinkList() {
        DoublyNode* current = head;
        while (current != NULL) {
            DoublyNode* next = current->next;
            delete current;
            current = next;
        }
        head = tail = NULL;
    }
    
    bool isEmpty() { return head == NULL; }
    
    DoublyNode* insertAtHead(int x) {
        DoublyNode* newNode = new DoublyNode(x);
        if (isEmpty()) {
            head = tail = newNode;
        } else {
            newNode->next = head;
            head->prev = newNode;
            head = newNode;
        }
        return head;
    }
    
    DoublyNode* insertAtEnd(int x) {
        DoublyNode* newNode = new DoublyNode(x);
        if (isEmpty()) {
            head = tail = newNode;
        } else {
            tail->next = newNode;
            newNode->prev = tail;
            tail = newNode;
        }
        return head;
    }
    
    DoublyNode* insertNode(int index, int x) {
        if (index < 0) return NULL;
        
        if (index == 0) {
            return insertAtHead(x);
        }
        
        DoublyNode* newNode = new DoublyNode(x);
        DoublyNode* temp = head;
        
        for (int i = 0; i < index - 1 && temp != NULL; i++) {
            temp = temp->next;
        }
        
        if (temp == NULL) {
            delete newNode;
            return NULL;
        }
        
        newNode->next = temp->next;
        newNode->prev = temp;
        
        if (temp->next != NULL) {
            temp->next->prev = newNode;
        } else {
            tail = newNode;
        }
        
        temp->next = newNode;
        return head;
    }
    
    bool findNode(int x) {
        DoublyNode* temp = head;
        while (temp != NULL) {
            if (temp->data == x) {
                return true;
            }
            temp = temp->next;
        }
        return false;
    }
    
    bool deleteNode(int x) {
        if (isEmpty()) return false;
        
        bool deleted = false;
        DoublyNode* current = head;
        
        while (current != NULL) {
            if (current->data == x) {
                if (current->prev != NULL) {
                    current->prev->next = current->next;
                } else {
                    head = current->next;
                }
                
                if (current->next != NULL) {
                    current->next->prev = current->prev;
                } else {
                    tail = current->prev;
                }
                
                DoublyNode* toDelete = current;
                current = current->next;
                delete toDelete;
                deleted = true;
            } else {
                current = current->next;
            }
        }
        
        return deleted;
    }
    
    bool deleteFromStart() {
        if (isEmpty()) return false;
        
        DoublyNode* temp = head;
        head = head->next;
        
        if (head != NULL) {
            head->prev = NULL;
        } else {
            tail = NULL;
        }
        
        delete temp;
        return true;
    }
    
    bool deleteFromEnd() {
        if (isEmpty()) return false;
        
        DoublyNode* temp = tail;
        tail = tail->prev;
        
        if (tail != NULL) {
            tail->next = NULL;
        } else {
            head = NULL;
        }
        
        delete temp;
        return true;
    }
    
    void displayList() {
        DoublyNode* temp = head;
        cout << "List (forward): ";
        while (temp != NULL) {
            cout << temp->data << " <-> ";
            temp = temp->next;
        }
        cout << "NULL" << endl;
    }
    
    void displayReverse() {
        DoublyNode* temp = tail;
        cout << "List (backward): ";
        while (temp != NULL) {
            cout << temp->data << " <-> ";
            temp = temp->prev;
        }
        cout << "NULL" << endl;
    }
    
    DoublyNode* reverseList() {
        if (isEmpty() || head->next == NULL) {
            return head;
        }
        
        DoublyNode* current = head;
        DoublyNode* temp = NULL;
        
        while (current != NULL) {
            temp = current->prev;
            current->prev = current->next;
            current->next = temp;
            current = current->prev;
        }
        
        if (temp != NULL) {
            head = temp->prev;
        }
        
        return head;
    }
};