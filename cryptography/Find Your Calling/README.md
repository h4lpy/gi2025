# Find Your Calling

I found this really weird message on an online forum. Can you solve it?

13-01-24-09-24-11-11-02-07-09
20-26-24-12-16-02-05-05-01-24
05-09-18-08-14-25-02-07-23-18
08-14-11-22-20-05-05-02-07-26
21-14-13-23-08-07-13-21-24-23
14-09-24-23-22-14-13-23-08-16
07-13-01-24-16-08-08-23-12-13
01-24-18-21-24-24-11-23-08-12

[IMAGE]

124 64 160 130 76 7 34 90 51 96
94 16 2 186 118 66 8 56 70 68
44 88 142 86 3 144 134 6 112 116
17 106 39 100 190 0 162 22 78 119
36 5 20 12 46 72 29 22 10 13








+1

8 4 4

6 20

72 13







Perrin Pages:


```
0, 2, 3, 5, 7, 10, 12, 17, 22, 29, 39, 51, 68, 90, 119, 158
```

Erdos-Woods:

```
16, 22, 34, 36, 46, 56, 64, 66, 70, 76, 78, 86, 88, 92, 94, 96, 100, 106, 112, 116, 118, 120, 124, 130, 134, 142, 144, 146, 154, 160, 162, 186, 190
```



### Wallkthrough

The first part of the message is number->letter substitution which converts to:

```
MAXIXKKBGITZXLPBEEAXEIRHNYBGWRHNKVTEEBGZUNMWHGMUXWNIXWVNMWHPGMAXPHHWLMAXRUXXKWHL
```

Caesar Cipher with shift value of 7 reveals:

```
THEPERRINPAGESWILLHELPYOUFINDYOURCALLINGBUTDONTBEDUPEDCUTDOWNTHEWOODSTHEYBEERDOS

THE PERRIN PAGES WILL HELP YOU FIND YOUR CALLING BUT DONT BE DUPED CUT DOWN THE WOODS THEY BE ERDOS
```

Remove ("cut down") the [Perrin Pages](https://oeis.org/A001608) and [Erdos-Woods numbers](https://oeis.org/A059756) numbers:

```python
erdos_woods = [16, 22, 34, 36, 46, 56, 64, 66, 70, 76, 78, 86, 88, 92, 94, 96, 100, 106, 112, 116, 118, 120, 124, 130, 134, 142, 144, 146, 154, 160, 162, 186, 190]
perrin_pages = [0, 2, 3, 5, 7, 10, 12, 17, 22, 29, 39, 51, 68, 90, 119, 158]

remove_numbers = erdos_woods + perrin_pages

all_numbers = [124,64,160,130,76,7,34,90,51,96,94,16,2,186,118,66,8,56,70,68,44,88,142,86,3,144,134,6,112,116,17,106,39,100,190,0,162,22,78,119,36,5,20,12,46,72,29,22,10,13]
all_numbers = [x for x in all_numbers if x not in remove_numbers]
print(''.join(map(str, all_numbers)))  # 8446207213
```

Reveals phone number: +1 (844) 620 7213

Phoning the number introduces the maze. the sequence of moves which reach the flag are:

```
86848888888688488626222668886266868866662686
```
