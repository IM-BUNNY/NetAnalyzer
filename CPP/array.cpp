#include <iostream>
#include <cstring>  

using namespace std;
class A
{
    private:
    int size;
    int *a;

    public :
    A(int a1[],int s )
    {
        size = s;
        a= new int [size];
        for (int i=0;i<size;i++)
        {
            a[i]=a1[i];
        }
    }
friend bool operator == (const A a1,const A a2)
    {
        if (a1.size != a2.size)
        return false ;
        for (int i=0;i<a2.size;++i)
        {
            if (a1.a[i]!=a2.a[i])
            return false ;
        }
        return true ;
    }

    ~A()
    {
        delete []a;
        a= nullptr;
    }
};
    
int main ()
{
    int a1[]={1,2,3,4,5};
    int a2[]={1,2,3,4};

    A obj1(a1,sizeof(a1)/sizeof(a1[0]));
    A obj2(a2,sizeof(a2)/sizeof(a2[0]));

    if(obj1==obj2)
    cout<<"Array are same ";
    else 
    cout<<"Array are diff";

    return 0;
}