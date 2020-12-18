### Menuconfig Setup and Usage
---
#### Source
1. [GitHub](https://github.com/ulfalizer/Kconfiglib)
    - `git clone https://github.com/ulfalizer/Kconfiglib.git`
1. [Python Package Index](https://pypi.org/project/kconfiglib/)

#### Menuconfig interfaces
1. Terminal
    - `python3 menuconfig.py examples/Kmenuconfig`
1. GUI
    - `python3 guiconfig.py examples/Kmenuconfig`
    - install tkinter
        - `sudo apt-get install python3-tk`

#### Kconfig syntax Intro
- [Kconfiglib/kconfiglib.py](https://github.com/ulfalizer/Kconfiglib/blob/master/kconfiglib.py)
- examples/Kmenuconfig

##### Symbol
- bool
    - y or n
- tristate
    - y: set
    - m: module
    - n: not set
- string
- int
- hex

##### keywords
- default
    - bool
        - default y
        - default y if A
        - default y if A && B
    - string
        - default "foo"
    - int
        - default 123
    - hex
        - default 0x123
- depends on A
- optional
- comment "string"
- menu "string"
- choice

##### Examples
```
config FOO
    bool "set or not set CONFIG_FOO"
```

```
menu "String, int, and hex symbols"

config STRING
    string "String symbol"
    default "foo"

config INT
    int "Int symbol"
    default 747

config HEX
    hex "Hex symbol"
    default 0xABC

endmenu
```

```
menu "Various choices"

choice BOOL_CHOICE
    bool "Bool choice"

config BOOL_CHOICE_SYM_1
    bool "Bool choice sym 1"
    default n

config BOOL_CHOICE_SYM_2
    bool "Bool choice sym 2"
    default y

endchoice

endmenu
```
