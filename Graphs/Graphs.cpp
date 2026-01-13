#include<iostream>
#include<vector>
#include<list>
#include<queue>
using namespace std;

class graph{
    int v;
    list<int> *l;

public:
    graph(int v){
        this->v=v;
        l=new list<int>[v];
    }

    void addEdge(int u,int v){
        l[u].push_back(v);
        l[v].push_back(v);
    }

    void printAdjlist(){
        for(int i=0;i<v;i++){
            cout<<i<<" : ";
            for(int neigh:l[i]){
                cout<<neigh<<" ";
            }
            cout<<endl;
        }
    }
};


int main(){
    graph g(5);
    g.addEdge(0,1);
    g.addEdge(1,2);
    g.addEdge(1,3);
    g.addEdge(2,3);
    g.addEdge(2,4);
    
    g.printAdjlist();
    return 0;

}