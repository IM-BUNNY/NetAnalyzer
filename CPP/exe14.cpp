#include<iostream>
using namespace std;

class demo
{
    int a ;
    public: 
    void getdata()
    {
        cout<<"enter a no:";
        cin>>a;
    }
    void putdata()
    {
        cout<<"\nvalue : "<<a;
    }
    demo operator +(demo b)
    {
        demo c;
        c.a=a+b.a;
        return c;
    }
};
int main()
{
    demo a,b,c;
    a.getdata();
    b.getdata();
    c=a+b;
    a.putdata();
    b.putdata();
    c.putdata();
        return 0;
}
