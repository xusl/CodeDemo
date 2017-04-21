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

template<typename T>
inline void swap(T data[], int i, int j) { 
#if 0
    int ia = 2, ib =2;
    cout << ia << ", " << ib << endl;
    ia ^= ib ^= ia ^=ib;
    cout << ia << ", " << ib << endl;
    ia ^= ia ^= ia ^=ia;
    cout << ia << ", " << ib << endl;
#endif
    /*if i == j, this is not two data swap, it just one data, and the result
     * is 0.
     * */
    if (i == j) {
        //printf("swap %d <=> %d\n", i, j);
        return;
    }
    data[j] ^= data[i] ^= data[j] ^= data[i]; 
}

template<typename T>
void print_array(T const data[], int length) {
    //cout << endl;
    for(int i = 0; i < length; i++){
        cout << data[i] << " ";
    }
    cout << endl;
}

template<typename T>
void insert_sort(T data[], int length) {
    for(int pivot = 1; pivot < length; pivot++) {
        /*
        if (data[pivot] > data[pivot -1]) {
            continue;
        }
        */
        T dot = data[pivot];
        int cursor = pivot;
        for(; cursor > 0; cursor--) {
            if (dot < data[cursor - 1] )
                data[cursor] = data[cursor - 1];
            else {
          //      cout << dot << endl;
          // there are omission that when dot is the least data,
          // and will never go here, so it should asign dot after loop
                //data[cursor] = dot;
                break;
            }
        }
        //cout << dot << endl;
        //print_array(data, length);
        data[cursor] = dot;
    }
}

template<class T> void bubble(T data[], int length) {
    for (int i=0; i < length; i++) {
        for(int j = length - 1; j > i; j--) {
            if (data[j - 1] > data [j])
                swap(data, j - 1, j);
        }
    }
}

template<typename T> void insert(T data[], int length) {
    for (int pivot = 1; pivot < length; pivot++) {
        T pivot_data = data[pivot];
        int i = pivot;
        for(; i > 0 && data[i - 1] > pivot_data; i--) {
            data[i] = data[i-1];
        }
        data[i] = pivot_data;
    }
}

template <class T> void shell(T data[], int length) {
    int gap = length;
    //while((gap = floor(gap)/2) > 0) {
    while((gap = gap/2) > 0) {
        for(int i = gap; i < length; i++) {
            for(int j = i - gap ; j >= 0; j -= gap) {
                if (data[j] > data[j+gap])
                    swap(data, j + gap, j);
                else
                    break;
            }
        }
    }
}

template<typename T> void heap_adjust(T data[], int length, int i) {
    while(true) {
        int max = i;//  node i
        int left = 2 * i + 1;// left is the left child of node i
        int right = 2 * ( i + 1 );// the right child of node i
        if (left < length && data[max] < data[left]) {
            max = left;
        }
        if (right < length && data[max] < data[right]) {
            max = right;
        }

        if (max != i) {
            data[max] ^= data[i] ^= data[max] ^= data[i];
            i = max;
        } else {
            break;
        }
    }
}


//deep n heap have maximum (2^n - 1) node
// 1 + 2 + 4 + 8 + 16 + 2^(n-1) = 2^n - 1
// in binary, it may be more clear:
//  000..001
//  000..010
//  000..100
//  001..000
//  010..000
//  100..000
template<typename T> void heap_sort(T data[], int length) {
    //initialize heap, build heap from array data, after adjust, the first
    //element is the least element in the sequence.
    for ( int i = (length - 1) / 2; i >= 0; --i) {
        heap_adjust(data, length, i);
    }

    //from the last element to adjust the sequence.
    for (int i = length - 1; i > 0; --i) {
        //swap the heap top node data[0] with that last element in the heap
        //data[0] ^= data[i] ^= data[0] ^= data[i]; 
        swap(data, 0, i);
        heap_adjust(data, i, 0);
    }
}

template< class T> void mergesort(T data[], int length) {
    if (length <= 1)
        return;
    int middle = floor((length + 1) / 2);

    mergesort(data, middle);
    mergesort(data + middle, length - middle);
    int first = 0; 
    while(first < middle && middle <= length -1) {
        //insert sort solution
        if (data[first] > data[middle]) {
            T pivot = data[middle];
            for(int i = middle; i >= first; i--){
                data[i] = data[i - 1];
            }
            data[first] = pivot;
            middle ++;
        } else {
            first ++;
        }
    } 
}

template<class T> void selectsort(T data[], int length) {
    for (int i = 0; i < length - 1; i++) {
        int min_index = i;
        T min_value = data[i];
        for(int j = i + 1; j < length; j++) {
            if (data[j] < data[min_index]) {
                min_index = j;
            }
        }
        swap(data, i, min_index);
    }
}

template< class T> void quicksort(T data[], int length) {
    if (length <= 1)
        return;
#if 0
    int index = 0;
    T pivot = data[length -1];

    for(int i = 0; i < length - 1; i++) {
        if (data[i] < pivot) {
            swap(data, index++, i);
        }
    }
    swap(data, length - 1, index);
#else
    int index = length - 1;
    T pivot = data[0];

    for(int i = length - 1; i > 0 ; i--) {
        if (data[i] > pivot) { //if (data[i] < pivot) {
            swap(data, index--, i);
        }
    }
    swap(data, 0, index);

#endif

    quicksort(data, index);
    quicksort(data + index + 1, length - index -1);
}

typedef void (* sort_method)(int[], int);
static int qsort_cmp(const void *p1, const void *p2) {
    if (p1 == p2)
        return 0;
    if (p1 == NULL)
        return -1;
    if (p2 == NULL)
        return 1;
    //int v1 = static_cast<int> (*p1);
    //int v2 = static_cast<int> (*p2);
    int v1 = *(int *)p1;
    int v2 = *(int *)p2;
    if (v1 == v2)
        return 0;
    if (v1 > v2 )
        return 1;
    return -1; 
}

void sort_test(string name, sort_method method) {
    int data[] = {3, 1, 909, 33, 999, 9, 0, 1, 3, 18, 35, 1000, 900, 2, 5, 13, 7, 8, 11111, 0};
    int bytes = sizeof data;
    int length = bytes / sizeof data[0];
    int *base = (int *)malloc(bytes);
    if (base == NULL) {
        cout << "oom" << endl;
        return;
    }
    memcpy(base, data, bytes);
    cout << "xxxxxxxxxxxxxxx" << "Test Sort Method: " << name << "xxxxxxxxxxxxxxxxxx" << endl;
    print_array(data, length);
    method(data, length);
    print_array(data, length);

    qsort(base, length, sizeof(int), qsort_cmp);
    if (memcmp(base, data, bytes) == 0) {
        cout << name << " test pass " << endl;
    } else {
        cout << name << " test failed" << endl;
    }
    free(base);
}

void trim(string data, string& extra);
void trim1(string data, string& extra) {
    //result.erase(result.end() - 1, result.end());
    /*if (data.rfind('\n') == string::npos) {
        extra += data;
        return;
    }*/
    data = extra + data;
    if (data.at(data.size() - 1) == '\n') {
        extra.clear();
    } else {
        extra = data;
        extra.substr(extra.rfind('\n') + 1);
    }

    size_t found = data.rfind("\n"); 
    
    if (found != 0 && found != string::npos) {
        data.erase(found);
    }

    found = data.rfind("\n"); 
    if (found != string::npos) {
        data.erase(0, found + 1);
    }

#if 1
    ;
    while((found = data.find('\b'))!= string::npos) {
        data.erase(found - 1, 2);
    }
    //printf("trim text: %s\n", result.c_str());
#endif

OUT:
    /*
    size_t len = data.size() + 1;
    char * buffer = (char *)malloc(len);
    if (buffer == NULL) {
        cout << "OOM" << endl;
        return;
    }
    memset(buffer, 0, len);
    snprintf(buffer, len, "%s", data.c_str());
    free(buffer);
    */
 //   cout << buffer << endl;
//    printf("%s\n", buffer);
    cout << "'" << data << "'" << endl;

    std::ostringstream oss;
    oss << data;
    //cout << oss.str() << endl;
}

void trim(string data, string& extra) {
    //result.erase(result.end() - 1, result.end());
    /*if (data.rfind('\n') == string::npos) {
        extra += data;
        return;
    }*/
    data = extra + data;
    if (data.at(data.size() - 1) == '\n') {
        extra.clear();
    } else {
        extra = data;
        extra.substr(extra.rfind('\n') + 1);
    }

    size_t found = data.rfind("\n"); 
    
    if (found != 0 && found != string::npos) {
       // data.erase(found);
    }

    found = data.rfind("\n"); 
    if (found != string::npos) {
        data.erase(0, found + 1);
    }

#if 1
    ;
    while((found = data.find('\b'))!= string::npos) {
        data.erase(found - 1, 2);
    }
    //printf("trim text: %s\n", result.c_str());
#endif

OUT:
    /*
    size_t len = data.size() + 1;
    char * buffer = (char *)malloc(len);
    if (buffer == NULL) {
        cout << "OOM" << endl;
        return;
    }
    memset(buffer, 0, len);
    snprintf(buffer, len, "%s", data.c_str());
    free(buffer);
    */
 //   cout << buffer << endl;
//    printf("%s\n", buffer);
    cout << "'" << data << "'" << endl;

    std::ostringstream oss;
    oss << data;
    //cout << oss.str() << endl;
}

static void backspace(string result, char flag) {
    size_t found = string::npos;
    cout << "orgin:" << result << endl;
    while((found = result.find(flag)) != string::npos) {
        if (found > 0)
            result.erase(found - 1, 2);
        else
            result.erase(0,1);
    }

    cout << "handle:" << result << endl;
}

static void test(string result) {
        size_t found = result.rfind("\n");
        if (found != string::npos) {
            result.erase(found);
        }
        found = result.rfind("\n");
        if (found != string::npos) {
            result.erase(0, found + 1);
        }
        //use printf to handle \b (backspace) in the result data;
        while((found = result.find('\b')) != string::npos) {
            if(found > 0)
                result.erase(found - 1, 2);
            else
                result.erase(0, 1);
        }

    cout << "handle:" << result << endl; 
}

string data="GET /0/nor-ipq40xx-single.img HTTP/1.1\
User-Agent: Wget/1.17.1 (linux-gnu)\
Accept: */*\
Accept-Encoding: identity\
Host: 10.0.0.4\
Connection: Keep-Alive";

string openwrt = "Writing from <stdin> to /dev/mtd9 ...  [ ][e][w][e][w][e]";

int main()  {

    bar bt;
    base* b = &bt; //new bar();
    b->test_override(3);
    b->test_overwrite("hel");

    bt.test_override(11);
    bt.test_overwrite(0.000001);
    //bt.test_overwrite("wooo");

    //delete b;
    //char ussd_data [] = { 0X49,0X68,0X72,0X20,0X47,0X75,0X74,0X68,0X61,0X62,0X65,0X6E,0X20,0X62,0X65,0X74,0X72,0X7B,0X67,0X74,0X3A,0X20,0X31,0X32,0X2C,0X30,0X39,0X1B,0X65,0X2E, };
    //printf("%s\n\n\n", ussd_data); 
    std::ostringstream ossPort;
    const char *host = "192.168.1.1";
    int port = 8080;
    int index = 0;
    const char *filename = "nor.img";
	ossPort << "wget http://" << host << ":" << port << "/";
	ossPort << index << "/" << filename;
	ossPort << " -O /tmp/" << filename;

    printf("%s\n\n\n", ossPort.str().c_str());

    port = 3;
    char p[256]={0};
    const int i = MAX_LEN;
    int got =    sscanf(data.c_str(), "GE /%d/%255s ", &port, p);
    string st = "123\n456";           //10个字符  
    string substr = st;
    cout << " format " << FORMAT(i) << endl;
    cout << "xxxxxxxxxx port:" << port <<endl;
    cout << "file : " << p <<endl;
    cout << "got: " << got  <<endl;
    // cout<< st.rfind("\r\n") << endl;  //按照定义应返回-1，实际是2  
    size_t found = st.rfind("\r\n");
    if (found != string::npos)
    substr = st.substr(found + 2); 
    cout << "now : " << substr << endl; 
    const char* pid = "1bbb"; 
    printf("0x%x\n", atoi(pid));
    string segment("");
    trim("1. Hello ", segment);
    trim("World!", segment);
    trim("\r\n", segment);
    trim("2. ", segment);
    trim("Hello World!\r\n", segment);
    trim("\r\n 1 next line\r\n 2 line\r\n3. Hello World'''!\r\nsdffdf", segment);
    trim("\r\n 1 next line\r\n 2 line\r\n4. Hello World'''!\r\n5. Hel", segment);
    trim("lo World!\r\nHello ", segment);
    trim("\r\n 1 next line\r\n 2 line\r\n6. Hello World'''\b\b\b!\r\n", segment);
    trim("\r\n 1 next line\r\n 2 line\r\n7. Hello World'''\b\b\b!\r\n8. Hel", segment);
    trim("lo World!\r\n xxxx Hello ", segment);
    trim("\r\n 9. xxxxx Hello Openwrt! xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx ... [ ]\b\b\b", segment);
    //trim("", segment);

    test(openwrt);

    string tail_return = "ssdftetste t tetet\r\nxxxxxasdfdsf\r\n";
    cout << "rfind test" << tail_return.erase(0, tail_return.rfind("\n", tail_return.size() - 2)) << endl;

    backspace("/dev/mtd9 ... [ ][e][w]", '\b');
    backspace("/dev/mtd3 ... [ ]\b\b\b[e]\b\b\b[w]", '\b');
    backspace("bbb/dev/mtd3 ... [ ]", 'b');
    backspace("bbb/dev/mtd3 ... [ ]bbb[e]", 'b');
    backspace("bbb/dev/mtd3 ... [ ]bbb[e]bbb[w]", 'b');

    int data[] = {3, 1, 909, 33, 999, 9, 0, 1, 3, 18, 35};
    int length =sizeof data/ sizeof data[0];

    //print_array(data, length);
    //insert_sort<int>(data, length);
    //insert<int>(data, length);
    //heap_sort<int>(data, length);
    //bubble(data, length);
    //shell(data, length);
    //mergesort(data, length);
    //quicksort<int>(data, length);
    //print_array(data, length);

    sort_test("insert sort", insert);
    sort_test("select sort", selectsort);
    sort_test("heap sort", heap_sort);
    sort_test("bubble sort", bubble);
    sort_test("shell sort", shell);
    sort_test("merge sort", mergesort);
    sort_test("quicksort", quicksort);

    return 0;     
}  

