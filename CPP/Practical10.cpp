#include<iostream>

using namespace std;

class Distance 
{
    private :
        float k_meter;
        float meter;


    public :
        Distance (float km, float m)
        {
            meter = m;
            k_meter= km;
        }

        Distance (float miles )
        {
            k_meter = int(miles / 0.621371);
             meter = (miles / 0.621371 - k_meter) * 1000;
        }

        operator float()
        {
            float miles ;
            miles=(k_meter + meter / 1000) * 0.621371;
            return miles;
        }
        void display()
        {
            cout<<" Distance in Kilometer and Meters = "<< k_meter<<" KM"<<meter<<" M";
        }
};
int main ()
{   
    float km,m;
    cout<<"Enter the distance in Km and m = ";
    cin>>km>>m;
    Distance d1(km,m);

    float mile = d1;
    cout<<"Distance in miles = "<<mile<<" miles ";

    float miles;
    cout<<"\nEnter the miles value = ";
    cin>>miles;
    Distance d2(miles);
    d2.display();

}