### ARM Assembly Language Guide

- B, BL
    - Branch, and Branch with Link.
    - B
        - branch to label or address
        - `PC <- label`
    - BL
        - branch to label
        - `LR <- PC - 4, PC <- label`
- BLX
    - Branch with Link and Exchange.
- BX
    - Branch and Exchange Instruction Set.
    - BX    R0
        - 跳到R0指定的位址，並根據LSB來切換Thumb mode

#### Example
```assembly
    B   lable           ; branch unconditionally to lable
    BCC lable           ; branch to lable if carry flag is clear
    BEQ lable           ; branch to lable if zero flag is set
    BNQ lable           ; branch to lable if zero flag is not set

    MOV PC, #0          ; R15 = 0, branch to location zero
    BL  func            ; subroutine call to function

    LDR r1, [r0]        ; Load r1 from the address in r0
    LDR r11, [r1, r2]   ; Load r11 from the address in r1 + r2
    LDR r11, [r1, #4]   ; Load r11 from the address in r1 + 4
```

##### Sum 1 to 10
```assembly
    MOV r1, #10
    MOV r6, #0
loop
    ADD r6, r6, r1      ; r6 = r6 + r1
    SUB r1, r1, #1      ; r1 = r1 - 1
    BNQ loop            ; jump to loop if zero flag is net set
```
