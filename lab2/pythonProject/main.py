import math
p0 = 0.5*pow(10 , -6)
e0 = 8.85*pow(10 , -12)
d = 0.1
pi = 3.14

x = (p0*d*d)/(e0*pi*pi)
print(x)
r = 0
for r in range(0 , 21):
    E = x*cos((pi(math.*r*pow(10 , -2))/d)-1)
    print('{} -> {}'.format(r , E))