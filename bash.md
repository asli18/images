# Bash script

### Commands

#### shopt
- `-s` set option
- `-u` unset option

- options
    - autocd
        - change directory without `cd` command
    - expand_aliases
        - make alias command work in bash script

---
### Difference between return and exit in Bash script

- Source script (`source foo.sh` or `. foo.sh`)
    - Use `return` command to leave the script
    - When I use `exit` command in a sourced shell script, the script will terminate the terminal (the prompt).

- Execute script (`./foo.sh`)
    - Use `exit` command to leave the script
    - Use `return` command in function only

- Detect bash script source vs. direct execution
    ```bash
    [[ $0 != $BASH_SOURCE ]] && echo "Script is being sourced" || echo "Script is being run"
    ```
    or
    ```bash
    if [ $0 != $BASH_SOURCE ]; then
        echo "Script is being sourced"
        return 0
    else
        echo "Script is being run"
        exit 0
    fi
    ```

- Compatible solution for Sourcing and Executing
    ```bash
    shopt -s expand_aliases # make alias command work in bash script
    [[ $0 != $BASH_SOURCE ]] && alias exit_cmd='return' || alias exit_cmd='exit'

    exit_cmd 0
    ```

- Reference
    - [What is the difference between executing a Bash script vs sourcing it?
    ](https://superuser.com/questions/176783/what-is-the-difference-between-executing-a-bash-script-vs-sourcing-it)
    - [Any way to exit bash script, but not quitting the terminal
    ](https://stackoverflow.com/questions/9640660/any-way-to-exit-bash-script-but-not-quitting-the-terminal)
    - [determining path to sourced shell script
    ](https://unix.stackexchange.com/questions/4650/determining-path-to-sourced-shell-script)

---
