#include <iostream>
using namespace std;

class Node {
public:
    int data;
    Node* next;
    
    Node(int x) {
        data = x;
        next = NULL;
    }
};

class LinkList {
private:
    Node* head;

public:
    LinkList() { head = NULL; }
    
    ~LinkList() {
        Node* current = head;
        while (current != NULL) {
            Node* next = current->next;
            delete current;
            current = next;
        }
        head = NULL;
    }
    
    bool isEmpty() { return head == NULL; }
    
    Node* insertAtHead(int x) {
        Node* newNode = new Node(x);
        newNode->next = head;
        head = newNode;
        return head;
    }
    
    Node* insertAtEnd(int x) {
        Node* newNode = new Node(x);
        if (head == NULL) {
            head = newNode;
            return head;
        }
        
        Node* temp = head;
        while (temp->next != NULL) {
            temp = temp->next;
        }
        temp->next = newNode;
        return head;
    }
    
    Node* insertNode(int index, int x) {
        if (index < 0) return NULL;
        
        if (index == 0) {
            return insertAtHead(x);
        }
        
        Node* newNode = new Node(x);
        Node* temp = head;
        
        for (int i = 0; i < index - 1 && temp != NULL; i++) {
            temp = temp->next;
        }
        
        if (temp == NULL) {
            delete newNode;
            return NULL;
        }
        
        newNode->next = temp->next;
        temp->next = newNode;
        return head;
    }
    
    bool findNode(int x) {
        Node* temp = head;
        while (temp != NULL) {
            if (temp->data == x) {
                return true;
            }
            temp = temp->next;
        }
        return false;
    }
    
    bool deleteNode(int x) {
        if (head == NULL) return false;
        
        bool deleted = false;
        
        // Delete from head if matches
        while (head != NULL && head->data == x) {
            Node* temp = head;
            head = head->next;
            delete temp;
            deleted = true;
        }
        
        if (head == NULL) return deleted;
        
        // Delete from middle or end
        Node* current = head;
        while (current->next != NULL) {
            if (current->next->data == x) {
                Node* temp = current->next;
                current->next = temp->next;
                delete temp;
                deleted = true;
            } else {
                current = current->next;
            }
        }
        
        return deleted;
    }
    
    bool deleteFromStart() {
        if (head == NULL) return false;
        
        Node* temp = head;
        head = head->next;
        delete temp;
        return true;
    }
    
    bool deleteFromEnd() {
        if (head == NULL) return false;
        
        if (head->next == NULL) {
            delete head;
            head = NULL;
            return true;
        }
        
        Node* temp = head;
        while (temp->next->next != NULL) {
            temp = temp->next;
        }
        
        delete temp->next;
        temp->next = NULL;
        return true;
    }
    
    void displayList() {
        Node* temp = head;
        cout << "List: ";
        while (temp != NULL) {
            cout << temp->data << " -> ";
            temp = temp->next;
        }
        cout << "NULL" << endl;
    }
    
    Node* reverseList() {
        if (head == NULL || head->next == NULL) {
            return head;
        }
        
        Node* prev = NULL;
        Node* current = head;
        Node* next = NULL;
        
        while (current != NULL) {
            next = current->next;
            current->next = prev;
            prev = current;
            current = next;
        }
        
        head = prev;
        return head;
    }
    
    Node* sortList(Node* list) {
        if (list == NULL || list->next == NULL) {
            return list;
        }
        
        // Bubble sort implementation
        bool swapped;
        do {
            swapped = false;
            Node* current = list;
            Node* prev = NULL;
            
            while (current != NULL && current->next != NULL) {
                if (current->data > current->next->data) {
                    // Swap nodes
                    Node* nextNode = current->next;
                    current->next = nextNode->next;
                    nextNode->next = current;
                    
                    if (prev == NULL) {
                        list = nextNode;
                    } else {
                        prev->next = nextNode;
                    }
                    
                    prev = nextNode;
                    swapped = true;
                } else {
                    prev = current;
                    current = current->next;
                }
            }
        } while (swapped);
        
        head = list;
        return head;
    }
    
    Node* removeDuplicates(Node* list) {
        if (list == NULL || list->next == NULL) {
            return list;
        }
        
        Node* current = list;
        while (current != NULL && current->next != NULL) {
            if (current->data == current->next->data) {
                Node* temp = current->next;
                current->next = temp->next;
                delete temp;
            } else {
                current = current->next;
            }
        }
        
        head = list;
        return head;
    }
    
    Node* mergeLists(Node* list1, Node* list2) {
        if (list1 == NULL) return list2;
        if (list2 == NULL) return list1;
        
        Node* merged = NULL;
        Node* tail = NULL;
        
        if (list1->data <= list2->data) {
            merged = list1;
            list1 = list1->next;
        } else {
            merged = list2;
            list2 = list2->next;
        }
        tail = merged;
        
        while (list1 != NULL && list2 != NULL) {
            if (list1->data <= list2->data) {
                tail->next = list1;
                list1 = list1->next;
            } else {
                tail->next = list2;
                list2 = list2->next;
            }
            tail = tail->next;
        }
        
        if (list1 != NULL) {
            tail->next = list1;
        } else {
            tail->next = list2;
        }
        
        return merged;
    }
    
    Node* intersectLists(Node* list1, Node* list2) {
        Node* result = NULL;
        Node* tail = NULL;
        
        // Sort both lists first
        list1 = sortList(list1);
        list2 = sortList(list2);
        
        while (list1 != NULL && list2 != NULL) {
            if (list1->data == list2->data) {
                if (result == NULL) {
                    result = new Node(list1->data);
                    tail = result;
                } else {
                    tail->next = new Node(list1->data);
                    tail = tail->next;
                }
                list1 = list1->next;
                list2 = list2->next;
            } else if (list1->data < list2->data) {
                list1 = list1->next;
            } else {
                list2 = list2->next;
            }
        }
        
        return result;
    }
    
    // Getter for head for external operations
    Node* getHead() { return head; }
    
    // Setter for head
    void setHead(Node* newHead) { head = newHead; }
};