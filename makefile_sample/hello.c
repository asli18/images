#include <stdio.h>


void foo(void)
{
    printf("%s\n", __func__);
}


int main(void)
{
    printf("Hello World\n");

    foo();

    return 0;
}
