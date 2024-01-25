from fea import FEA;

num = input('number of dimensions: ');
stuff = FEA(int(num));
nodes=0;
while True:

	want =input('\n What would you like to do?:\n 1) start new project\n 2) add new spring\n 3) display node-element conectivity chart\n 4) display local stiffness matricies\n 5) quit\n');
	if int(want) ==1:
		num = input('number of dimensions');
		stuff = FEA(int(num));
		nodes=0;
	elif int(want)==2:
		# num, node1, node2, k=0,d=0,theta=0,phi=0

		num= int(input('What element number is this: '));
		node1=int(input('What is the first node it connects to: '));
		node2=int(input('What is the second node it connects to: '));
		k=float(input('What is the spring constant: '));
		d=float(input('What is the dampning constant: '));
		nodes=max(nodes,max(node1,node2));
		theta=0;
		phi=0;
		if stuff.dim >1:
			theta= float(input('What is theta (deg): '));
			if stuff.dim>2:
				phi=float(input('What is phi (deg): '));
		stuff.addSpring(num,node1,node2, k=k,d=d,theta=theta,phi=phi);

	elif int(want)==3:

		stuff.nodeElementChart();

	elif int(want)==4:

		stuff.localStiffnessMatrix();

	elif int(want)==5:
		break;

	elif int(want)==6:
		# num=input("How many nodes: ");
		stuff.printK(int(nodes));






