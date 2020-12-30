### Linux command

----

##### size
- list section sizes and total size of binary file
- size of library
```
$ size -t lib/axtls.a
   text    data     bss     dec     hex filename
   2228       0       0    2228     8b4 asn1.o (ex lib/axtls.a)
   1347       0       0    1347     543 loader.o (ex lib/axtls.a)
      0       0       0       0       0 p12.o (ex lib/axtls.a)
   5365       0       0    5365    14f5 tls1.o (ex lib/axtls.a)
   1394       0       0    1394     572 tls1_clnt.o (ex lib/axtls.a)
   1444       0       0    1444     5a4 x509.o (ex lib/axtls.a)
    194       0       0     194      c2 os_port.o (ex lib/axtls.a)
   2244       0       0    2244     8c4 aes.o (ex lib/axtls.a)
   2800       0       0    2800     af0 bigint.o (ex lib/axtls.a)
    178       0       0     178      b2 hmac.o (ex lib/axtls.a)
      0       0       0       0       0 rc4.o (ex lib/axtls.a)
    530       0       0     530     212 rsa.o (ex lib/axtls.a)
    389       0       0     389     185 sha256.o (ex lib/axtls.a)
    509       0      32     541     21d crypto_misc.o (ex lib/axtls.a)
    150       0       0     150      96 _muldi3.o (ex lib/axtls.a)
   1005       0       0    1005     3ed _udivdi3.o (ex lib/axtls.a)
    961       0       0     961     3c1 _umoddi3.o (ex lib/axtls.a)
  20738       0      32   20770    5122 (TOTALS)
```
##### df
- report file system disk space usage
- Options
    - -h, --human-readable
```
$ df -h
檔案系統        容量  已用  可用 已用% 掛載點
udev            1.5G     0  1.5G    0% /dev
tmpfs           299M  1.3M  298M    1% /run
/dev/sda1        40G   14G   24G   37% /
work            932G   56G  876G    6% /media/sf_work
tmpfs           299M   28K  299M    1% /run/user/1000
```

##### nm
- list symbols from object files
```
$ nm -n Debug/et760-2.0.adx
00000000 A MEM_BEGIN
00000000 A NDS_SAG_LMA_MEM
00000000 a _RELAX_END_
00000000 T reset_vector
00000000 A __text_lmastart
00000000 B __text_start
0000000c T _start
00000020 a irqno
00000054 T trap_entry
...
00007c30 B _end
00008000 A _stack
```

##### strings

- 列出檔案中任何可印出的字串