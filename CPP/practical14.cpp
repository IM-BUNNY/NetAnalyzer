#include<iostream>
using namespace std;

class Building
{ 
    protected:
    float Height;
    float Width;

    public:
    Building(float h, float w): Height(h),Width(w)
    {    
        cout<<"Building Constructed with Height "<< h <<"and Width "<< w ;        
    }
    ~Building()
    {
        cout<<"Building Destructed ";
    }
};

class height : public Building 
{

    public: 
    height (float h) : Building ( h ,0)
    {
        cout<<"Height constructed ";
    }
    ~height()
    {
        cout<<"Height destructed ";
    }

    double getHeight() const {
        return Height ;
    }
};

class width : public Building 
{
    public:
    width(float w ): Building (0,w)
    {
        cout<<"Width constructed";
    }
    ~width()
    {
        cout<<"Width destructed ";
    }
    double getWidth() const {
        return Width;
    }
};

class Feet : public height , public width
{
    public:
    Feet(double hFeet, double wFeet) : height(hFeet), width(wFeet) {
        cout << "Feet object created with height: " << height::Height << " feet and width: " << width::Width << " feet." << endl;
    }

    ~Feet() {
        cout << "Feet destroyed." << endl;
    }

    double heightToInches() const {
        return height::Height * 12; 
    }

    double widthToInches() const {
        return width::Width * 12; 
    }

};