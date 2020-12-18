CC = gcc
CFLAGS = -g -pg
# CFLAGS = -g -W -Wall -Wextra -O0 -pg
# CFLAGS = `sdl2-config --cflags` -g -W -Wall -Wextra -pedantic -O0 -I `sdl2-config --prefix`/include/
exe = hello
obj = hello.o


all: $(obj) foo
	$(CC) $(CFLAGS) -o $(exe) $(obj)
	mv foo bar

%.o: %.c
	$(CC) $(CFLAGS) -c $^ -o $@
	@echo "$@ $< $* $?"

foo:
	touch foo


.PHONY:clean
clean:
	@rm -f *.o $(obj) $(exe)

gprof:
	gprof hello gmon.out -b

help:
	@echo "help\r\nfoo"

