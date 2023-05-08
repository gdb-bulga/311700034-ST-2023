# NYCU Software Testing 2023 Lab 7

## PoC
[test.bmp](https://github.com/gdb-bulga/311700034-ST-2023/blob/main/Lab07/test.bmp)

## commands
```bash
$ cd Lab07
$ export CC=~/AFL/afl-gcc
$ export AFL_USE_ASAN=1
$ make
$ mkdir in
$ cp test.bmp in/
$ ~/AFL/afl-fuzz -i in -o out -m none -- ./bmpgrayscale @@ a.bmp

$ ./bmpgrayscale out/crashes/id:000000* a.bmp
```

## AFL Result

![螢幕擷取畫面 2023-05-07 095927](https://user-images.githubusercontent.com/44048482/236720944-a9a84802-ff9f-4283-b02d-3afa345510a2.png)

## ASAN Result!

![螢幕擷取畫面 2023-05-07 100115](https://user-images.githubusercontent.com/44048482/236720986-1f7aee49-b431-4700-998e-58d2d2680690.png)
