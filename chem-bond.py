

t = ['H','He',
	 'Li','Be','B','C','N','O','F','Ne',
	 'Na','Mg','Al','Si','P','S','Cl','Ar',
	 'K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr',
	 'Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb','Te','I','Xe',
	 'Cs','Ba']
#table = {'H':1,'He':2,'Li':3,'Be':4,'B':5,'C':6,'N':7,'O':8,'F':9,'Ne':10,'Na':11,'Mg':12,'Al':13,'Si':14,'P':15,'S':16,'Cl':17,'Ar':18}

def get_elem_groups(equation):
	elements = []
	pos = 0
	rep = 0
	secondPos = 0
	numRep = 1
	while pos < len(equation):

		if equation[pos] == '(':
			for i in range(pos,len(equation)):
				if equation[i] == ')':
					secondPos = i+1
					break

			numRep = 1
			if secondPos < len(equation) and equation[secondPos].isdigit(): numRep = int(equation[secondPos])
			for i in range(0, numRep):
					elements.append(equation[pos+1:secondPos-1])

			pos = secondPos+1

		elif pos < len(equation)-1 and equation[pos+1].islower():
			if pos < len(equation)-2 and equation[pos+2].isdigit():
				secondPos = pos+3
				if pos < len(equation)-3 and equation[pos+3].isdigit(): secondPos+=1
				for i in range(0, int(equation[pos+2:secondPos])): elements.append(equation[pos:pos+2])
				pos+=secondPos-pos-2

			else: elements.append(equation[pos:pos+2])
			pos+=2
		else:
			if pos < len(equation)-1 and equation[pos+1].isdigit():
				secondPos = pos+2
				if pos < len(equation)-2 and equation[pos+2].isdigit(): secondPos+=1
				for i in range(0, int(equation[pos+1:secondPos])): elements.append(equation[pos])
				pos+=secondPos-pos-1

			else: elements.append(equation[pos])
			pos+=1

	return elements

def get_elem(equation):
	element_group = []
	for group in get_elem_groups(equation):
		element_group.append(get_elem_groups(group))
	return element_group

def get_indiv_elems(equation):
	elements = get_elem(equation)
	elements = [list(x) for x in set(tuple(x) for x in elements)]
	return elements

def get_indiv_groups(equation):
	elements = []
	pos = 0
	secondPos = 0
	while pos < len(equation):

		if equation[pos] == '(':
			for i in range(pos,len(equation)):
				if equation[i] == ')':
					secondPos = i+1
					break

			elements.append(equation[pos+1:secondPos-1])
			pos = secondPos+1

		elif pos < len(equation)-1 and equation[pos+1].islower():
			if pos < len(equation)-2 and equation[pos+2].isdigit():
				secondPos = pos+3
				if pos < len(equation)-3 and equation[pos+3].isdigit(): secondPos+=1
				elements.append(equation[pos:pos+2])
				pos+=secondPos-pos-2

			else: elements.append(equation[pos:pos+2])
			pos+=2
		else:
			if pos < len(equation)-1 and equation[pos+1].isdigit():
				secondPos = pos+2
				if pos < len(equation)-2 and equation[pos+2].isdigit(): secondPos+=1
				elements.append(equation[pos])
				pos+=secondPos-pos-1

			else: elements.append(equation[pos])
			pos+=1

	return elements

def elec(element_name):
	try:
		return t.index(element_name)+1
	except ValueError:
		return -1

def v_elec(element_name):
	electrons = elec(element_name)-1
	if electrons < 2:
		return electrons+1
	elif electrons < 19:
		return (electrons-2)%8+1
	else:
		if (electrons-18)%18+1 < 12 and electrons != 46:
			return (electrons-18)%18+1
		else:
			return ((electrons-18)%18+1)%10

def orbit(element_name):
	electrons = elec(element_name)
	if electrons < 19:
		return (electrons-3)//8+2
	else:
		return (electrons-19)//18+4

def elec_config(element_name):
	electrons = elec(element_name)-1
	config = ''
	if electrons < 2: config = '1s' + str(electrons+1)
	else:
		electrons-=1
		orbitVal = orbit(element_name)
		for i in range(2,orbitVal+1):
			if electrons <= 2:
				config+=str(i) + 's' + str(electrons)
				break
			config+=str(i)+'s2-'
			electrons-=2
			if i > 3:
				if electrons <= 10:
					if electrons == 4 or electrons == 9:
						config = config[:len(config)-2] + '1' + config[len(config)-1:]
						config+=str(i-1) + 'd' + str(electrons+1)
					else: config+=str(i-1) + 'd' + str(electrons)
					break
				config+=str(i-1) + 'd10-'
				electrons-=10
			if electrons <= 6:
				config+=str(i) + 'p' + str(electrons)
				break
			electrons-=6
			config+=str(i)+'p6-'
		config = '1s2-' + config
	return config


def charges(equation, rep, reverse):

	original_charges = []
	charges = []

	elem_list = get_elem(equation)
	# print(elem_list)

	for i in elem_list:
		total = 0
		for j in i:
			if(v_elec(j) > 3): total+=8-v_elec(j)
			elif(elec(j) == 1): 
				if len(i) < 2: total+=v_elec(j)
				else: total-=v_elec(j)
			else: total-=v_elec(j)

		if total > 0:
			if total < 4: charges.append(total)
			else: charges.append(total)
		else: charges.append(total)

	original_charges = charges.copy()
	# print(charges)

	sing = [[],[]]
	doub = [[],[]]
	trip = [[],[]]

	for i in range(0, len(elem_list)):
		for j in range(0, i):
			if abs(charges[i]) != 1 or abs(charges[j]) != 1 or (charges[i] == 1 and charges[j] == 1 and len(elem_list) == 2) or charges[i] * charges[j] < 0:
				sing[0].append(i)
				sing[1].append(j)

			# if charges[i] * charges[j] > 0 and charges[i] > 1 and charges[j] > 1 and (charges[i] > 2 or charges[j] > 2) or (charges[i] == 2 and charges[j] == 2 and len(elem_list) == 2):
			if charges[i] * charges[j] > 0 and charges[i] > 1 and charges[j] > 1 and (charges[i] > 2 or charges[j] > 2) or (charges[i]*charges[j] < 0 and charges[i] == 2 and -charges[i] == charges[j]) or (charges[i] == 2 and charges[j] == 2 and len(elem_list) == 2):
				doub[0].append(i)
				doub[1].append(j)

			if charges[i] * charges[j] > 0 and charges[i] > 1 and charges[j] > 1 and (charges[i] > 3 or charges[j] > 3):
				trip[0].append(i)
				trip[1].append(j)
	
	sing_values = []
	doub_values = []

	for i in range(0, len(elem_list)): sing_values.append([i])
	for i in range(0, len(elem_list)): doub_values.append([i])

	for k in range(0, len(elem_list)):
		for i in range(len(elem_list)-1 if reverse else 0, -1 if reverse else len(elem_list), -1 if reverse else 1):

			index = 0
			bond_type = 0
			num_bonds_made = 0

			if not rep:
				try:
					index = doub[0].index(i)
					bond_loc = 0
					bond_type = 2
				except ValueError: bond_loc = -1
				try:
					index = doub[1].index(i)
					bond_loc = 1
					bond_type = 2
				except ValueError: bond_loc = -1

			if bond_type == 0:
				try:
					index = sing[0].index(i)
					bond_loc = 0
					bond_type = 1
				except ValueError: bond_loc = -1
				try:
					index = sing[1].index(i)
					bond_loc = 1
					bond_type = 1
				except ValueError: bond_loc = -1


			num_bonds = len(sing_values[0])


			if bond_loc != -1:
				if bond_type == 1:
					if charges[sing[0][index]] != 0 and charges[sing[1][index]] != 0:
						charges[sing[0][index]]-= charges[sing[0][index]] / abs(charges[sing[0][index]])
						charges[sing[1][index]]-= charges[sing[1][index]] / abs(charges[sing[1][index]])
						sing_values[i].append(sing[bond_loc*-1 + 1][index])
						sing_values[sing[bond_loc*-1 + 1][index]].append(i)

						for l in range(0, len(doub[0])-1):
							if (doub[0][l] == sing[0][index] and doub[1][l] == sing[1][index]) or (doub[0][l] == sing[1][index] and doub[1][l] == sing[0][index]):
								doub[0].pop(l)
								doub[1].pop(l)



					sing[0].pop(index)
					sing[1].pop(index)

				if bond_type == 2:
					if charges[doub[0][index]] != 0 and charges[doub[0][index]] != 1 and charges[doub[1][index]] != 0 and charges[doub[1][index]] != 1:
						# prevents allense but makes things like benzense possibly work
						if not (elem_list[doub[0][index]] == ['C'] and elem_list[doub[1][index]] == ['C'] and len(doub_values[doub[0][index]]) + len(doub_values[doub[1][index]]) > 2):
							charges[doub[0][index]]-= 2 * charges[doub[0][index]] / abs(charges[doub[0][index]])
							charges[doub[1][index]]-= 2 * charges[doub[1][index]] / abs(charges[doub[1][index]])
							doub_values[i].append(doub[bond_loc*-1 + 1][index])
							doub_values[doub[bond_loc*-1 + 1][index]].append(i)


						for l in range(0, len(sing[0])-1):
							if (sing[0][l] == doub[0][index] and sing[1][l] == doub[1][index]) or (sing[0][l] == doub[1][index] and sing[1][l] == doub[0][index]):
								sing[0].pop(l)
								sing[1].pop(l)


					doub[0].pop(index)
					doub[1].pop(index)
	# print(charges)

	return sum(charges) > 0, sing_values, doub_values, elem_list, original_charges

def bond(equation):
	#true false to try and get certain bonds working
	repeat, sing_values, doub_values, elem_list, charge = charges(equation, False, False)
	if repeat:
		repeat, sing_values, doub_values, elem_list, charge = charges(equation, True, False)
	if repeat:
		repeat, sing_values, doub_values, elem_list, charge = charges(equation, False, True)
	if repeat:
		repeat, sing_values, doub_values, elem_list, charge = charges(equation, True, True)
	if repeat:
		print('more methods to get exact structure')

	bonds = []
	for i in range(0, len(sing_values)):
		bonds.append([sing_values[i][0]])
		for j in range(1,len(sing_values[i])): bonds[i].append([sing_values[i][j],1])
		for j in range(1,len(doub_values[i])): bonds[i].append([doub_values[i][j],2])

	print(bonds)

	for i in bonds:
		print('bond')
		if len(i) > 1:
			print('      ' + str(elem_list[i[1][0]]))
			print('        ' + ('||' if i[1][1] == 2 else '|'))

		output = ''
		if len(i) > 2:
			output+= str(elem_list[i[2][0]]) + ('=' if i[2][1] == 2 else '-')
		else:
			output+='      '

		output+= str(elem_list[i[0]])

		if len(i) > 3:
			output+= ('=' if i[3][1] == 2 else '-') + str(elem_list[i[3][0]])

		print(output)

		if len(i) > 4:
			print('        '  + ('||' if i[4][1] == 2 else '|'))
			print('      ' + str(elem_list[i[3][0]]))


	x = [5]
	y = [5]
	z = [5]

	# import math

	# bond_charge = v_elec(elem_list[bonds[0][0]][0])

	# for i in range(1, len(bonds[0])): bond_charge-= bonds[0][i][1]

	# print(len(bonds[0]))
	# print(bond_charge)

	# if len(bonds[0]) == 5 and bond_charge == 0:
	# 	for i in range(1, len(bonds[0])-1):
	# 		x.append(5 + (math.cos((i-1) * math.pi * 2 / 3)) * math.cos(math.pi/6))
	# 		y.append(5 + (math.sin((i-1) * math.pi * 2 / 3)) * math.cos(math.pi/6))
	# 		z.append(5 - math.sin(math.pi/6))

	# 	x.append(5)
	# 	y.append(5)
	# 	z.append(6)

	# elif len(bonds[0]) == 4 and bond_charge == 2:
	# 	for i in range(1, len(bonds[0])):
	# 		x.append(5 + (math.cos((i-1) * math.pi * 2 / 3)) * math.cos(math.pi/5))
	# 		y.append(5 + (math.sin((i-1) * math.pi * 2 / 3)) * math.cos(math.pi/5))
	# 		z.append(5 - math.sin(math.pi/5))

	# elif len(bonds[0]) == 4 and bond_charge == 0:
	# 	for i in range(1, len(bonds[0])):
	# 		x.append(5 + (math.cos((i-1) * math.pi * 2 / 3)))
	# 		y.append(5 + (math.sin((i-1) * math.pi * 2 / 3)))
	# 		z.append(5)

	# elif len(bonds[0]) == 4 and bond_charge == 0:
	# 	for i in range(1, len(bonds[0])):
	# 		x.append(5 + (math.cos((i-1) * math.pi * 2 / 3)))
	# 		y.append(5 + (math.sin((i-1) * math.pi * 2 / 3)))
	# 		z.append(5)

	# elif len(bonds[0]) == 3 and bond_charge == 4:
	# 	for i in range(1, len(bonds[0])):
	# 		x.append(5 + (math.cos((i-1) * math.pi * 2 / 3.45)))
	# 		y.append(5 + (math.sin((i-1) * math.pi * 2 / 3.45)))
	# 		z.append(5)

	# elif len(bonds[0]) == 3 and bond_charge == 2:
	# 	for i in range(1, len(bonds[0])):
	# 		x.append(5 + (math.cos((i-1) * math.pi * 2 / 3.1)))
	# 		y.append(5 + (math.sin((i-1) * math.pi * 2 / 3.1)))
	# 		z.append(5)

	# elif len(bonds[0]) == 3 and bond_charge == 0:
	# 	for i in range(1, len(bonds[0])):
	# 		x.append(6)
	# 		y.append(5)
	# 		z.append(5)

	# 		x.append(4)
	# 		y.append(5)
	# 		z.append(5)

	# elif len(bonds[0]) == 2:
	# 	x.append(6)
	# 	y.append(5)
	# 	z.append(5)
		

	# import matplotlib.pyplot as plt
	# from mpl_toolkits.mplot3d import Axes3D

	# fig = plt.figure()
	# ax = fig.add_subplot(projection='3d')
	# ax.scatter(x, y, z, c='g', marker='o', s=50)

	# ax.set_yticklabels([])
	# ax.set_xticklabels([])
	# ax.set_zticklabels([])

	# ax.set_xlim(2,8)
	# ax.set_ylim(2,8)
	# ax.set_zlim(2,8)
	# plt.show()




# bond('H2O')
# bond('CO2')
# bond('NaOH')
# bond('BaCl2')
# bond('H2O2')
bond('HCOOH')
# bond('HONO')
# bond('H2NOH')
# bond('BH3')
# bond('CO2')
