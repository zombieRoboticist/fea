from fea import FEA;
from texttable import Texttable as txtble;
import math;

table=txtble();
stuff=FEA(2);

k=210*(10**9)*4*(10**-4);


stuff.addSpring(1,1,2, k=k,theta=0);
stuff.addSpring(2,1,3, k=k,theta=90);
stuff.addSpring(3,2,4, k=k,theta=90);
stuff.addSpring(4,1,4, k=k/(2**.5),theta=45);
stuff.addSpring(5,3,4, k=k,theta=0);
stuff.addSpring(6,3,5, k=k/(2**.5),theta=45);
stuff.addSpring(7,4,5, k=k,theta=90);
stuff.addSpring(8,5,6, k=k/2,theta=-30);
stuff.addSpring(9,4,6, k=k/(3**.5),theta=0);

stuff.addForce(6,'y',-105000);

stuff.addDisp(1,'x',0);
stuff.addDisp(1,'y',0);
stuff.addDisp(2,'y',0);
stuff.addDisp(3,'x',0);


print(stuff.nodeElementChart());
print(stuff.localStiffnessMatrix());
print(stuff.printK(6));
a,b,c=stuff.splitK(6);
print(stuff.disppos);

table.add_rows(a);
print('reduced k \n'+ table.draw());
print(stuff.solve(6))

print();
print('**'*20);
print();

suff2=FEA(2);
e=68*10**6;
a=1;
suff2.addSpring(1,1,2,k=e*a/(10*(1-math.cos(math.radians(60))/math.sin(math.radians(60)))),theta=0);
suff2.addSpring(2,1,3,k=e*a/10*math.sin(math.radians(60)),theta=120);
suff2.addSpring(3,2,3,k=e*a/(10*2**.5),theta=135);

suff2.addForce(1,'x',-2000);

suff2.addDisp(1,'y',0);
suff2.addDisp(2,'y',0);
suff2.addDisp(3,'x',0);
suff2.addDisp(3,'y',0);


table=txtble();
print(suff2.nodeElementChart());
print(suff2.localStiffnessMatrix());
print(suff2.printK(3));
a,b,c=suff2.splitK(3);
print(suff2.disppos);

table.add_rows(a);
print('reduced k \n'+ table.draw());
print(suff2.solve(3))
