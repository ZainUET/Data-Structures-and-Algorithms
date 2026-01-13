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

    void bfs(){
        queue<int> Q;
        vector<bool> vis(v,false);

        Q.push(0);
        vis[0]=true;

        while(Q.size()>0){
        int u = Q.front();
        Q.pop();

        cout<< u <<" ";

        for(int v: l[u]){
            if(!vis[v]){
                vis[v]=true;
                Q.push(v);
            }
        }
    }
        cout<<endl;
    }
};


int main(){
    graph g(5);
    g.addEdge(0,1);
    g.addEdge(1,2);
    g.addEdge(1,3);
    g.addEdge(2,3);
    g.addEdge(2,4);
 
    g.bfs();
    return 0;

}