from operator import lt
s=*map(int,open("data/day01.in","r").readlines()),
l=lambda i:sum(map(lt,i[:-1],i[1:]))
print(l(s),l(tuple(map(sum,zip(s,s[1:],s[2:])))))