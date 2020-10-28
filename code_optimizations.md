### Code Optimizations

- Data alignment
    - struct and array
        - making the length of each element a power of 2 simplifies the offset calculation when accessing an individual element
    - Global data access
        - If a function accesses a number of external globals,
        the compiler must assume that they are in separate compilation units and therefore not guaranteed to be co-located at run-time.
        **A separate base pointer is required for each one.**
        - **The most common solution** is to place globals, or more usually groups of related globals, into **structures**.
        These structures are then guaranteed to be placed as a single unit at link-time and can be accessed using a single base pointer.
    - **Aligning data structures to cache line boundaries in memory** can make better use of the pre-loading effect of cache line fills,
    making it more likely that wanted data is loaded as part of the line and unwanted data is not.
    The compiler provides a data attribute for doing this
        - `int myarray[16] __attribute__((aligned(64)));`
- Efficient parameter passing
    - keep parameters to four or fewer
        - 當參數超過4個，就都會都放在stack，增加額外的開銷(overhead)
    - return value can be passed back in a register and a doubleword value in two registers
    - Further, there are “alignment” restrictions on the use of registers when passing doublewords as parameters
      In essence, a doubleword is passed in two register and those registers must be an even-odd pair i.e. `r0 and r1`,
      or `r2 and r3`. The following function call will pass `a` in `r0`, `b` in `r2:r3` and `c` on the `stack`.
      `r1` cannot be used due to the alignment restrictions which apply to passing the doubleword.
        - `fx(int a, long long b, int c)`
    - Re-declaring the function as shown below is functionally identical but passes all the parameters in registers.
        - `fx(int a, int c, long long b)`
- Prefer int to char or short, 變數用 int 類型，可提高性能減少程式碼
    - 當使用 char, short 當記數值時，每次運算都要判斷結果是否超過範圍
    - return value 用 int 也會有一樣的效果
- 有號數 & 無號數 在 **加減乘法** 並沒有太大差異，但有號數 **除法** 就會差很多
    - `x / 2` 當 x 為負值，除2 就不是只是單純的右移
        - `-3 >> 1 = -2`, but `-3 / 2 = -1`
- 善用 const & static
    - static function
        - compiler會視情況而決定是否編譯成inline 
    - inline function
        - 並不會一定編譯成inline, 只是建議compiler
- 使用 unsigned 類型作為迴圈記數值，迴圈繼續的條件用 `i != 0` 取代 `i > 0`
- 如果確定迴圈至少執行一次，用 `do-while` 取代 `for`
- 迴圈內如果有 array  data 要累加，換成 pointer 效率較高
    - `sum += data[i];`, two instructions
    - `sum += *(data++);`, one instruction
- [**Optimizations in loop**](https://www.geeksforgeeks.org/basic-code-optimizations-in-c/)
    - Unroll small loops
    - Use Register variables as counters of inner loops
        - `register int i = 0;`
- Avoid unnecessary Integer Division
    - `d = (a / b / c) -> d = (a / (b * c))`
- Simplifying Expressions
    - `(a * b) + (a * b * c) + (a * b * c * d) -> (a * b) * (1 + c * (1 + d))`
- Order of Expression Evaluation
    * `A || B`<br>
    Here first A will be evaluated, if it’s true then there is no need of evaluation of expression B.
    So We should prefer to have an expression which evaluates to true most of the times, at the A’s place.
    * `A && B`<br>
    Here first A will be evaluated, if it’s false then there is no need of evaluation of expresinon B.
    So We should prefer to have an expression which evaluates to false most of the times, at the A’s place.

#### Reference
- [Efficient C Code for ARM Devices](https://m.eet.com/media/1157397/atc-152paper_shore_v4.pdf)
