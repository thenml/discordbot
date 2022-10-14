import base64

with open("src\\_hidden\\codes.txt",'r',encoding="utf-8") as f:
    string = "".join(f.readlines()).replace("\n"," ")
print(string)

strbytes = string.encode('utf-8')
str64 = base64.a85encode(strbytes)
string = str64.decode("ascii")
print(string)

a,b='',''
for i,x in enumerate(string):
    if i%4:b+=x
    else:a+=x

print(f'\n{a}\n{b}\n')


#decode
a="d1)@O[+_q=dR\p@JYq2(+I`R(Y$WBTds:e^+"
b="(Rfd>-Qd(Z=+P_dEu5\Bq3^<HR13]g'>F\^70^+hYK%3W3%:@:ri@6cFdRf1OIAd=TTd(f?d1@HgBWYgB$YgW$YV>F=]hd'5OZ-3OJK&m9"
string=''
for i in range(len(a)):
    string+=a[i]+b[i*3:i*3+3]
print(string)
str64 = string.encode("utf-8")
strbytes = base64.a85decode(str64)
string = strbytes.decode("utf-8")
print(string)