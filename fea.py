from texttable import Texttable as txtble;
import numpy as np;
import math;

class Force(object):

	def __init__(self, pos, val):

		self.pos=pos;
		self.val=val;

class Spring(object):

	def __init__(self, dim, num, node1, node2, k=0,d=0,theta=0,phi=0):

		self.dim=dim;
		self.num=num;
		self.node1=node1;
		self.node2=node2;
		self.k=k;
		self.d=d;
		self.theta=theta;
		self.phi=phi;
		self.type="spring";

	def getLocalStiff(self):

		if self.dim==1:
			return self.k*np.array([[1,-1],[-1,1]]);
		elif self.dim==2:
			s=math.sin(math.radians(self.theta));
			c=math.cos(math.radians(self.theta));
			return self.k*np.array([[c*c,c*s,-c*c,-s*c],[c*s,s*s,-s*c,-s*s],[-c*c,-c*s,c*c,c*s],[-c*s,-s*s,s*c,s*s]]);
		elif self.dim==3:
			s=math.sin(math.radians(self.theta));
			c=math.cos(math.radians(self.theta));
			a=math.sin(math.radians(self.phi));
			b=math.cos(math.radians(self.phi));
			g=np.array([[-c*b], [-s*b], [-a], [c*b], [s*b], [a]]);
			return self.k*(g*np.transpose(g));


class FEA (object):

	ele=np.array([Spring(0,0,0,0)]);
	have = False;
	fpos=[];
	disppos=[];
	force=[];
	disp=[];

	def __init__(self, dim):
		self.dim =dim;

	def addSpring(self, num, node1, node2, k=0,d=0,theta=0,phi=0):
		x= Spring(self.dim, num, node1, node2, k=k,d=d,theta=theta,phi=phi);
		if not self.have:
			self.ele[0]=x;
			# print (self.ele)

			self.have=True;
		else:
			self.ele=np.append(self.ele,x);
		return x;

	def nodeElementChart(self):

		table =txtble();
		things=[];
		if self.have:
			if self.dim ==1:
				things.append((["Element", "Node 1", "Node 2", "K","Type"]));
				for i in self.ele:
					things.append(([i.num,i.node1,i.node2,i.k,i.type]));
					# print(i);
			elif self.dim==2:
				things.append((["Element", "Node 1", "Node 2", "K","Theta","Type"]));
				for i in self.ele:
					things.append(([i.num,i.node1,i.node2,i.k,i.theta, i.type]));	
			elif self.dim==3:
				things.append((["Element", "Node 1", "Node 2", "K", "Theta", "Phi", "Type"]));
				for i in self.ele:
					things.append(([i.num,i.node1,i.node2,i.k,i.theta,i.phi,i.type]));			

			table.add_rows(things)
			print(table.draw());
			return things;

	def localStiffnessMatrix(self):

		if self.have:
			for i in self.ele:
				table = txtble();
				things=[];
				if self.dim==1:
					things.append(["Element "+ str(i.num), "Node "+str(i.node1),"Node "+ str(i.node2)]);
					x=i.getLocalStiff();
					things.append(["Node "+str(i.node1),x[0,0],x[0,1]]);
					things.append(["Node "+str(i.node2),x[1,0],x[1,1]]);
				elif self.dim==2:
					things.append(["Element "+ str(i.num), "Node "+str(i.node1)+" x","Node "+ str(i.node1)+ " y","Node "+str(i.node2)+" x","Node "+ str(i.node2)+ " y"]);
					x=i.getLocalStiff();
					things.append(["Node "+str(i.node1) +" x",x[0,0],x[0,1],x[0,2],x[0,3]]);
					things.append(["Node "+str(i.node1)+" y",x[1,0],x[1,1],x[1,2],x[1,3]]);
					things.append(["Node "+str(i.node2) +" x",x[2,0],x[2,1],x[2,2],x[2,3]]);
					things.append(["Node "+str(i.node2)+" y",x[3,0],x[3,1],x[3,2],x[3,3]]);
				elif self.dim==3:
					things.append(["Element "+ str(i.num), "Node "+str(i.node1)+" x","Node "+ str(i.node1)+ " y","Node "+ str(i.node1)+ " z","Node "+str(i.node2)+" x","Node "+ str(i.node2)+ " y","Node "+ str(i.node2)+ " z"]);
					x=i.getLocalStiff();
					things.append(["Node "+str(i.node1) +" x",x[0,0],x[0,1],x[0,2],x[0,3],x[0,4],x[0,5]]);
					things.append(["Node "+str(i.node1)+" y",x[1,0],x[1,1],x[1,2],x[1,3],x[1,4],x[1,5]]);
					things.append(["Node "+str(i.node1) +" z",x[2,0],x[2,1],x[2,2],x[2,3],x[2,4],x[2,5]]);
					things.append(["Node "+str(i.node2) +" x",x[3,0],x[3,1],x[3,2],x[3,3],x[3,4],x[3,5]]);
					things.append(["Node "+str(i.node2) +" y",x[4,0],x[4,1],x[4,2],x[4,3],x[4,4],x[4,5]]);
					things.append(["Node "+str(i.node2) +" z",x[5,0],x[5,1],x[5,2],x[5,3],x[5,4],x[5,5]]);

				table.add_rows(things);
				print(table.draw());
				print();


	def getK(self, numNodes):

		things=np.zeros((numNodes*self.dim, numNodes*self.dim));

		for i in self.ele:
			x=i.getLocalStiff();
			n1=i.node1;
			n2=i.node2;

			for j in range(self.dim):
				for k in range(self.dim):
					things[(n1-1)*self.dim+j,(n1-1)*self.dim+k]+=x[j,k];
					things[(n1-1)*self.dim+j,(n2-1)*self.dim+k]+= x[self.dim+j,k];
					things[(n2-1)*self.dim+j,(n1-1)*self.dim+k]+= x[j,self.dim+k];
					things[(n2-1)*self.dim+j,(n2-1)*self.dim+k]+= x[self.dim+j,self.dim+k];
		return things;

	def printK(self,numNodes):
		k=self.getK(numNodes);

		things=[];
		temp1=[];
		for i in range (numNodes):
			temp ="";
			for j in range (self.dim):
				if j==0:
					temp= "Node "+str(i+1)+" x";
				elif j==1:
					temp= "Node "+str(i+1)+" y";
				elif j==2:
					temp= "Node "+str(i+1)+" z";
				else :
					temp= "Node "+str(i+1)+", "+str(j+1);
				temp1.append(temp);
		things.append(temp1);
		for i in k:
			things.append(i);
		# print(things);
		table=txtble();
		table.add_rows(things);
		print(table.draw());

	def addForce(self, node, dire, val):

		off=0;
		if dire=='x':
			off=0;
		elif dire=='y':
			off=1;
		elif dire=='z':
			off=3;
		else:
			off = int(dire);

		self.force.append( Force(off+(node-1)*self.dim,val));
		self.fpos.append(off+(node-1)*self.dim);
		return;

	def addDisp(self,node,dire,val):

		off=0;
		if dire=='x':
			off=0;
		elif dire=='y':
			off=1;
		elif dire=='z':
			off=3;
		else:
			off = int(dire);

		self.disp.append(Force(off+(node-1)*self.dim,val));
		self.disppos.append(off+(node-1)*self.dim);
		return;

	def splitK(self, numNodes):

		k=self.getK(numNodes);

		smk=[];
		gtf=[];
		inpk=[];

		for i in range(self.dim*numNodes):
			rwsmk=[];
			rwgtf=[];
			rwinpk=[];
			for j in range(self.dim*numNodes):

				if i in self.disppos:
					
					rwgtf=k[i];
					continue;

				else:

					if j in self.disppos:
						rwinpk.append(k[i,j]);

					else:
						rwsmk.append(k[i,j]);
			if i in self.disppos:
				gtf.append(rwgtf);
			else:
				inpk.append(rwinpk);
				smk.append(rwsmk);
		return np.array(smk), np.array(inpk), np.array(gtf);


	def solve(self, numNodes):
		smk,inpk,gtf=self.splitK(numNodes);

		fr=np.zeros((numNodes*self.dim,1));
		dp=np.zeros((len(self.disp),1));
		c=0;
		for i in self.force:
			fr[i.pos]=[i.val];
		for i in self.disp:
			dp[c]=[i.val];
			fr=np.delete(fr,i.pos-c,0);
			c+=1;

		unknx = np.linalg.inv(smk)@(fr-inpk@dp);

		x=np.zeros((numNodes*self.dim,1));
		c=0;
		n=0;
		for i in range(numNodes*self.dim):

			if i in self.disppos:
				x[i,0]= self.disp[n].val;
				n+=1;
			else:
				x[i,0]=unknx[c,0];
				c+=1;

		uknf=gtf@x;

		return unknx, uknf;









# table = txtble();
# # table.add_rows(['test','test','test'], [1,2,3]);
# print(table.draw());
# table.add_rows([["test","test","test"], [1,2,3]]);
# print(table.draw());