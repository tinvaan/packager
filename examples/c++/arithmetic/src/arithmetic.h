
#ifndef _ARITHMETIC_H_
#define _ARITHMETIC_H_


class Arithmetic
{
    public:
        Arithmetic();

        int add(int, int );
        int sub(int, int);
        int mul(int, int);
        int div(int, int);

        int get_result();
        void set_result(int);

    private:
        int m_result;
};

#endif // _ARITHMETIC_H_

