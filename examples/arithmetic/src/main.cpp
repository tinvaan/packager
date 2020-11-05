
#include <string>
#include <iostream>

#include "arithmetic.h"


int main(int argc, char *argv[])
{
    int a, b;
    Arithmetic art = Arithmetic();
    std::string operation;
    std::cin >> a >> b;
    std::cout << art.add(a, b) << std::endl;
    return 0;
}
