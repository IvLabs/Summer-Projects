import numpy as np
import gym
import time
import math
import matplotlib
import matplotlib.pyplot as plt
from gym_snake.envs.snake_env import *
from gym_snake.envs.snake.snake import *
from gym_snake.envs.snake.grid import *
from gym_snake.envs.snake.discrete import *


name = 'snake-v0'
#edit below variables to run on different enviornments
y_max = 15
x_max = 15

try:
	q_val = np.load('q_val.npy')
except:
	q_val = np.zeros((4,2,2,2,3))
def policy(epsilon,d,frud,fob,lob,rob):
	'''Policy function helps to determine the suitable action for an agent for a state.State parameters are passed to the 
	function -
	frud - direction of food relative to snake's head
	fob = to check presence of obstacle in immediate Forward block of snake's head
	lob = to check presence of obstacle in immediate Left block of snake's head
	rob = to check presence of obstacle in immediate Right block of snake's head'''
	l = d-1	#defining rule for relative directions
	r = d+1
	f = d
	b = abs(d-2)
	if l == -1:
		l = 3
	if r == 4:
		r = 0
	act = [0,1,2,3]
	act2 = [l,r,f]
	randnum = np.random.rand()
	
	if randnum < epsilon:
		x = int(np.random.choice(act2))
		if x==l:
			return x,"Left"
		if x==r:
			return x,"Right"
		if x==f:
			return x,"Forward"
	else:
		x = int(np.argmax(q_val[frud][fob][lob][rob]))
		if x==0:
			return l,"Left"
		if x==1:
			return f,"Forward"
		if x==2:
			return r,"Right"
			
def gen_episode (env,alpha,gamma,epsilon): 
	'''To generate one episode. Returns episodic reward and total steps taken.'''
	def get_fruit(obs):
		'''Function to obtain coordinates of food on grid.Returns x,y'''
		for j in range(0,y_max*10,10):
			for k in range (0,x_max*10,10):
				if(np.array_equal(obs[j][k],np.array([0,0,255]))):
					y_f = j
					x_f = k
		x_f = int(x_f/10)
		y_f = int(y_f/10)
				
		return x_f,y_f
	def get_loc(obs):
		'''Fucntion to obtain coordinates of head of snake. returns x,y'''
		for j in range(0,y_max*10,10):
			for k in range (0,x_max*10,10):
				if(np.array_equal(obs[j][k],np.array([255,10,0]))):
					y = j
					x = k
					x = int(x/10)
					y = int(y/10)
		return x,y
	def get_state(ob,x,y,xf,yf,d):
		'''Function to get current state of the snake. Takes input of coordinates of snake and food
		   and direction of head. Returns direction of fruit relative to snake and information related
		   to obstacles(including wall and sbody of snake) in form of 0 & 1 in for immediate left,right,forward of snake's head.
		   0 - presence of obstacle(wall or body)
		   1 - free space  ''' 
	 
		def inc(ob,x,y,d):
			'''function to determine presence of obstacle while snake's head is facing positive x or y axis.'''
			dis = 1
			if d==2:
				if y< y_max-1:
					if(np.array_equal(ob[10*(y+1)][10*x],np.array([1,0,0]))):
						dis = 0
				if dis==1 and y==(y_max-1):
					dis = 0
			else:
				if x< x_max-1:
					if(np.array_equal(ob[10*y][10*(x+1)],np.array([1,0,0]))):
						dis = 0
				if dis==1 and x==(x_max-1):
					dis=0

			return dis
			
		def dec(ob,x,y,d):
			'''function to determine presence of obstacle while snake's head is facing negative x or y axis.'''
			dis = 1
			if d==0:
				if y>0:
					if(np.array_equal(ob[10*(y-1)][10*x],np.array([1,0,0]))):
						dis = 0
				if dis==1 and y==0:
					dis= 0
			else:
				if x>0:
					if(np.array_equal(ob[10*y][10*(x-1)],np.array([1,0,0]))):
						dis = 0
				if dis==1 and x==0:
					dis=0
			return dis
		fd = 0
		x_diff = xf-x
		y_diff = yf-y
		l = d-1
		r = d+1
		f = d
		b = abs(d-2)
		if d==1:
			b=3
		if l == -1:
			l = 3
		if r == 4:
			r = 0
		if f==1 or f==2:
			fob = inc(ob,x,y,f)
		if f==3 or f==0:
			fob =dec(ob,x,y,f)
		if l==1 or l==2:
			lob = inc(ob,x,y,l)
		if l==0 or l==3:
			lob =dec(ob,x,y,l)
		if r==1 or r==2:
			rob = inc(ob,x,y,r)
		if r==0 or r==3:
			rob =dec(ob,x,y,r)

		if x_diff >=0 and y_diff >=0:
			if d==0 or d==1:
				fd = r

			if d==2 or d==3:
				fd = l
			if x_diff==0:
				if d==0:
					fd = b
				if d==2:
					fd = f
			if y_diff ==0:
				if d==1:
					fd = f
				if d==3:
					fd =b
		if x_diff >=0 and y_diff <0:
			if d==0 or d==3:
				fd = r
			if d==2 or d==1:
				fd = l
			if x_diff==0:
				if d==0:
					fd = f
				if d==2:
					fd = b
		if x_diff <0 and y_diff >=0:
			if d==1 or d==2:
				fd = r
			if d==0 or d==3:
				fd = l
			if y_diff==0:
				if d==3:
					fd = f
				if d==1:
					fd = b
		if x_diff <0 and y_diff <0:
			if d==2 or d==3:
				fd = r
			if d==0 or d==1:
				fd = l
		if fd==l:
			fd=0
			return fd,fob,lob,rob
		if fd==r:
			fd=2
			return fd,fob,lob,rob
		if fd==f:
			fd=1
			return fd,fob,lob,rob
		if fd==b:
			fd=3
			return fd,fob,lob,rob
	tot_rew = 0
	good = 0
	obs = env.reset()
	done = False
	steps = 0
	dr = 2
	x_f, y_f = get_fruit(obs)
	
	#loop to play in one episode unitl snake dies. Episode ends when snake dies.
	while not done: 
		x ,y = get_loc(obs)
		x_f, y_f = get_fruit(obs)
		frud,fob,lob,rob = get_state(obs,x,y,x_f,y_f,dr)
		action,st = policy(epsilon,dr,frud,fob,lob,rob)
		dr_new = action
		obs,rew,done, info = env.step(action)
		if rew==1:
			x_f, y_f = get_fruit(obs)
		if st=="Left":
			action = 0
		if st=="Forward":
			action = 1
		if st=="Right":
			action = 2
		if rew==-1:
			done=True
			print(x_new,y_new)
		else:
			x_new ,y_new = get_loc(obs)
		frud_new,fob_new,lob_new,rob_new = get_state(obs,x_new,y_new,x_f,y_f,dr_new)
		steps += 1
		#uncoment below line to run at slower speed
		#time.sleep(2)
		env.render()
		tot_rew +=rew
		#Comment below for epsilon greedy
		#q_val[frud,fob,lob,rob,action] += alpha*(rew + gamma*(np.max(q_val[frud_new,fob_new,lob_new,rob_new])) - q_val[frud,fob,lob,rob,action])
		dr = dr_new
		frud = frud_new
		fob = fob_new
		lob = lob_new
		rob = rob_new
	return tot_rew,steps

if __name__ =="__main__":
	rew_list = []
	step_list = []
	#In windows uncomment below line.In linux use next 7 lines and comment below line. 
	env = gym.make(id=name,grid_size=[y_max,x_max], unit_size=10, unit_gap=1, snake_size=3, n_snakes=1, n_foods=1, random_init=True)

# 	env = gym.make(name)
# 	env.grid_size = [y_max,x_max]
# 	env.unit_size = 10
# 	env.unit_gap = 1
# 	env.snake_size = 3
# 	env.n_snakes = 1
# 	env.n_foods = 1
		
	alpha = 0.1
	gamma = 0.2
	ep = 5000
	for i in range(0,ep):
		#To train the agent uncomment and use below line
		#rew,steps = gen_episode(env,alpha,gamma,(200/(200+i)))
		'''for epsilon =0. Uncomment below line'''
		rew,steps = gen_episode(env,alpha,gamma,0) 
		print("episode "+str(i+1)+" ended.Reward = "+str(rew))
		rew_list.append(rew)
		step_list.append(steps)
		
	np.save('q_val.npy',q_val)
	
	plt.clf()
	plt.plot(rew_list)
	plt.savefig('qrew.png')
	plt.clf()
	plt.plot(step_list)
	plt.savefig('q_steps.png')
	np.save('q_rewards',np.array(rew_list))
	np.save('q_steps',np.array(step_list))
