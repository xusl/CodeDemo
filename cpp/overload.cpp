#include<iostream>  
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <sstream>
using namespace std;  
#define MAX_LEN 256
#define FORMAT(x) "%"#x  "s"


class base {
    public:
        base() {
            cout << "base init" << endl;
        };
        ~base() {
        cout << "base destory" << endl;
        };
        //virtual void test_override(int num) = 0;
        virtual void test_override(int num) { 
            cout << __LINE__ << "base :" << __func__ << ", " << num << endl;
        }
        virtual void test_overwrite(string text) {
            cout << __LINE__ << "base :" << __func__ << ", " << text << endl;
        }
};

class bar : public base{
    public:
        bar();
        ~bar();
        void test_override(int num);
        void test_overwrite(float f);
};


bar::bar() {
    cout << "bar constructor" << endl;
}


bar::~bar() {
    cout << "bar destroy" << endl;
}

void bar::test_override(int num) {
    cout << __LINE__ << "bar :" << __func__ << ",  " << num << endl;
}

void bar::test_overwrite(float f) {
    cout << __LINE__ << "bar :" << __func__ << ", " << f << endl;
}

int main()  { 
    bar bt;
    base* b = &bt; //new bar();
    b->test_override(3);
    b->test_overwrite("hel");

    bt.test_override(11);
    bt.test_overwrite(0.000001);
    //bt.test_overwrite("wooo");

    return 0;     
}  
