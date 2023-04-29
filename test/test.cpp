#include <iostream>
#include "../HaiBinQiangJia/include/ff/FFProcess.h"

template<typename T>
void set_each_byte(T& data, char* values, int len) {
    char* p = (char*)&data;
    for (int i = 0; i < len; i++) {
        *(p + i) = values[i];
    }
}
int main()
{
    std::cout << "HaiBinQiangJia\n";
    FFProcess& ff = FFProcess::get_instance();

    struct OpCall {
        char op1;
        char offset[4];
    };

    int offset = 0x5aef67;
    OpCall buf;
    ReadProcessMemory(ff.hProcess, (LPCVOID)(ff.baseAdd + offset), &buf, sizeof(OpCall), nullptr);
    
    int offset_bit;
    set_each_byte(offset_bit, buf.offset, sizeof(buf.offset));

    int next_offset = offset + sizeof(OpCall);

    int target = next_offset + offset_bit;

    cout << hex << target << endl;
   
}
