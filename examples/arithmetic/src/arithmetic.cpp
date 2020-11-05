
#include "arithmetic.h"


Arithmetic::Arithmetic()
    : m_result(0)
{}

void Arithmetic::set_result(int val)
{
    m_result = val;
}

int Arithmetic::get_result()
{
    return m_result;
}

int Arithmetic::add(int a, int b)
{
    m_result = a + b;
    return m_result;
}

int Arithmetic::sub(int a, int b)
{
    m_result = a - b;
    return m_result;
}

int Arithmetic::mul(int a, int b)
{
    m_result = a * b;
    return m_result;
}

int Arithmetic::div(int a, int b)
{
    m_result = a / b;
    return m_result;
}