#### Compile and Run a C Program on Ubuntu Linux
1. [reference](http://akira.ruc.dk/~keld/teaching/CAN_e14/Readings/How%20to%20Compile%20and%20Run%20a%20C%20Program%20on%20Ubuntu%20Linux.pdf)
1. `vim hello.c`
    ``` c
    #include <stdio.h>

    int main(void)
    {
        printf("Hello World\n");
    }
    ```
1. Compile and link
    - `gcc -o hello hello.c`
    - `gcc -O1 -o hello hello.c` 
1. `./hello`

- Online IDE
    - [geeksforgeeks](https://ide.geeksforgeeks.org/)
    - [ideone](http://ideone.com/)
