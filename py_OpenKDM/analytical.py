"""
Functionality to finds analytical solution for kinetaic and dynamic
analysis of slider crank mechanism

@nimrobotics for OpenKDM, 2020
"""

import numpy as np 

class link(object):
	"""finds parameters like mass, inertia of each link"""
	def __init__(self, dim, rho):
		self.l = dim[0]
		self.b = dim[1]
		self.h = dim[2]
		self.rho = rho

	def mass(self):
		"""
		finds mass of a link
		"""
		return self.l*self.b*self.h*self.rho

	def inertia(self):
		"""
		Calculates inertia of a link by neglecting the rounded edges
		"""
		return (self.mass()/12)*(self.h**2 + self.l**2) + (self.mass()*self.l**2)/4


class Vectors:
    """Stores i,j component of a vector"""
    def __init__(self, i,j,k):
        self.i = i
        self.j = j
        self.k = k


def sliderCrank(link1, link2, m3, Wao, theta, rho, g):
	Lao=link(link1,rho)
	Lab=link(link2,rho)

	# print(np.deg2rad(theta),theta)
	theta=np.deg2rad(theta)
	if theta<=np.pi:
		theta3=np.pi-abs(np.arcsin((Lao.l*np.sin(theta))/Lab.l))
	else:
		theta3=np.pi+abs(np.arcsin((Lao.l*np.sin(theta))/Lab.l))
	# print(theta3,np.rad2deg(theta3))

	Va = Vectors(-Lao.l*Wao*np.sin(theta),Lao.l*Wao*np.cos(theta),0)
	Wba = Vectors(0,0,(Lao.l*Wao*np.cos(theta))/(Lab.l*np.cos(theta3)))
	Vb = Vectors(Lab.l*Wba.k*np.sin(theta3) - Lao.l*Wao*np.sin(theta),0,0)
	Aa = Vectors(-Wao**2*Lao.l*np.cos(theta), -Wao**2*Lao.l*np.sin(theta),0)
	ALPHAba = Vectors(0,0,(Wba.k**2*Lab.l*np.sin(theta3) - Wao**2*Lao.l*np.sin(theta))/(Lab.l*np.cos(theta3)))
	Ab = Vectors((ALPHAba.k*np.sin(theta3) + Wba.k**2*np.cos(theta3))*Lab.l - Lao.l*Wao**2*np.cos(theta),0,0)
	Aba = Vectors((np.sin(theta3)*ALPHAba.k + Wba.k**2*np.cos(theta3))*Lab.l,(-np.cos(theta3)*ALPHAba.k + Wba.k**2*np.sin(theta3))*Lab.l,0)
	Ac1 = Vectors(Aa.i/2,Aa.j/2,Aa.k/2)
	Ac2 = Vectors(Aa.i + Aba.i/2, Aa.j + Aba.j/2, Aa.k + Aba.k/2)

	A = np.array([[1,0,1,0,0,0,0,0],
			  [0,1,0,1,0,0,0,0],
			  [0,0,-1,0,1,0,0,0],
			  [0,0,0,-1,0,1,0,0],
			  [0,0,0,0,1,0,0,0],
			  [0,0,0,0,0,-1,1,0],
			  [0,0,-Lao.l*np.sin(theta),Lao.l*np.cos(theta),0,0,0,1],
			  [0,0,0,0,Lab.l*np.sin(theta3),Lab.l*np.cos(theta3),0,0]])

	B = np.array([[Lao.mass()*Ac1.i],
				  [Lao.mass()*Ac1.j + Lao.mass()*g],
				  [Lab.mass()*Ac2.i],
				  [Lab.mass()*Ac2.j + Lab.mass()*g],
				  [-m3*Ab.i],
				  [m3*g],
				  [Lao.l*0.5*np.cos(theta)*Lao.mass()*(Ac1.j+g)] - Lao.l*0.5*np.sin(theta)*Lao.mass()*Ac1.i,
				  [Lab.inertia()*ALPHAba.k + Lab.l*0.5*np.sin(theta3)*Lab.mass()*Ac2.i - Lab.l*0.5*np.cos(theta3)*Lab.mass()*(Ac2.j+g)]])

	# Fox, Foy, Fax, Fay, Fbx, Fby, N, T
	result = np.dot(np.linalg.inv(A),B)
	Fo = Vectors(result[0][0],result[1][0],0)
	Fa = Vectors(result[2][0],result[3][0],0)
	Fb = Vectors(result[4][0],result[5][0],0)
	N = Vectors(result[6][0],0,0)
	T = Vectors(0,0,result[7][0])

	# print(result)

	resultArr = np.zeros((14,3))
	values = [Va,Wba,Vb,Aa,ALPHAba,Ab,Aba,Ac1,Ac2,Fo,Fa,Fb,N,T]
	for u,value in enumerate(values):
		resultArr[u]=[value.i,value.j,value.k]
		# print(value.i,value.j,value.k,"\n")		
	
	# print(resultArr)
	return(resultArr)


#--------------------------------- INIT --------------------------------------------
# density of aluminum 2,710kg/m3 or 2.7 g/cm³
# Wao is the input angular velcoity
# theta is the position of crank
# [l,b,h] in meters
sliderCrank([0.13,0.03,0.01],[0.395,0.03,0.01],m3=0.25,Wao=2, theta=90,rho=2710,g=9.81)
