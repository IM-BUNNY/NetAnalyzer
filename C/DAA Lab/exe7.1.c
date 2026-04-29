#include <stdio.h>
#include <limits.h>


int fact(int n);

int main ()
{
    int n=5;
    int s = fact(n);
    printf("%d ", s);
    return 0;
}
int fact(int n)
{
    if (n==0 || n==1)
    {
        return 1 ;
    }
    else 
    {
        return (n * fact(n-1) );
    }
}
