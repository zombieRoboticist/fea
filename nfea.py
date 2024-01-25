import numpy as np;
import math;

class Spring(object):

	def __init__(self, dim, num, node1, node2, k, theta):
		""" theta should be a list of angles (deg) of length dim -1 """
		self.dim=dim;
		self.num=num;
		self.node1=node1;
		self.node2=node2;
		self.k=k;
		self.theta=theta;
		self.type="spring";

	def getLocalStiff(self):

		arr=[];

		if self.dim==1:
			arr=[[1],[-1]];

		elif self.dim >1:
			thing=[];
			c=1;
			for i in self.theta:
				thing.append(c*math.sin(math.radians(i)));
				c*=math.cos(math.radians(i));
			thing.append(c);

			for i in range(len(things)):
				temp=[-things[-(i+1)]];
				arr.append(temp);
			for i in range(len(things)):
				arr.append([-things[-(i+1)]]);

		g=np.array(arr);
		k=self.



