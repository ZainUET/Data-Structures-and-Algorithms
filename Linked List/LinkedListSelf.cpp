#include<iostream>
using namespace std;


class Node{
    public:
    int data;
    Node* next;

    Node(int val){
        data = val;
        next=NULL;

    }
};

class List{
    Node* head;
    Node* tail;
    
    public:
    List(){
        head=tail=NULL;
    }

    void push_front(int val){
        Node* newNode=new Node(val);
        if(head==NULL){
            head=tail=newNode;
            return;
        }
        else{
            newNode->next=head;
            head=newNode;
        }
    }

    void push_back(int val){
        Node* newNode=new Node(val);
        if(head==NULL){
            head=tail=newNode;
        }
        else{
            tail->next=newNode;
            tail=newNode;
        }
    }

    void pop_front(){
        if(head==NULL){
            cout<<"List is Empty";
            return;}
        
        Node* temp=head;
        head=head->next;
        temp->next=NULL;

        delete temp;

    }


    void pop_back(){
        if(head==NULL){
            cout<<"List is Empty";
            return;
        }

        Node* temp=head;

        while(temp->next!=tail){
            temp=temp->next;
        }

        temp->next=NULL;
        delete tail;
        tail=temp;

    }

    void insert(int val,int pos){
        if(pos<0){
            cout<<"Invalid Position";
            return;
        }
        if(pos==0){
            push_front(val);
        }

        Node* temp=head;
        for(int i=0;i<pos-1;i++){
            temp=temp->next;
        }

        Node* newNode=new Node(val);
        newNode->next=temp->next;
        temp->next=newNode;

    }

    void printLL(){
        Node* temp=head;

        while(temp!=NULL){
            cout<<temp->data<<"  ";
            temp=temp->next;
        }

        cout<<endl;

    }

};

int main(){
    List LL;
    LL.push_front(2);
    LL.push_front(3);
    LL.push_front(1);

    LL.insert(10,5);
    LL.printLL();

}
