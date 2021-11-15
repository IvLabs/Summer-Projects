import numpy as np
import gym
import time
import math
import matplotlib
import matplotlib.pyplot as plt
from gym_snake.envs.snake_extrahard_env import SnakeExtraHardEnv
from gym_snake.envs.snake.snake import *
from gym_snake.envs.snake.grid import *
from gym_snake.envs.snake.discrete import *


name = 'snake-plural-v0'
#edit below variables to run on different enviornments
'''For multiple snake, these y_max and x_max values must be greater than 9.'''
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
#defining rule for relative directions
	l = d-1	#Relative left	
	r = d+1	#Relative right
	f = d		#Relative forward
	b = abs(d-2)	#Relative backward(not included in action space)	
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
		'''Function to obtain coordinates of food on grid.Returns list which contains x and y coordinates of each food block.'''
		fru_loc = []
		for j in range(0,y_max*10,10):
			for k in range (0,x_max*10,10):
				if(np.array_equal(obs[j][k],np.array([0,0,255]))):
					y_f = j
					x_f = k
					x_f = int(x_f/10)
					y_f = int(y_f/10)
					fru_loc = fru_loc + [x_f,y_f]
		
				
		return fru_loc
	def get_loc(obs,s):
		'''Fucntion to obtain coordinates of head of snake. returns x,y'''
		for j in range(0,y_max*10,10):
			for k in range (0,x_max*10,10):
				if(np.array_equal(obs[j][k],np.array([255,10*s,0]))):
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
		   1 - free space  
		   frud - direction of food relative to snake's head
		   fob = to check presence of obstacle in immediate Forward block of snake's head
		   lob = to check presence of obstacle in immediate Left block of snake's head
		   rob = to check presence of obstacle in immediate Right block of snake's head''' 
	 
		def inc(ob,x,y,d):
			'''function to determine presence of obstacle while snake's head is facing positive x or y axis.'''
			dis = 1
			if d==2:
				if y< y_max-1:
					if(np.array_equal(ob[10*(y+1)][10*x],np.array([1,0,0]))) or (np.array_equal(ob[10*(y+1)][10*x],np.array([255,10,0]))) or (np.array_equal(ob[10*(y+1)][10*x],np.array([255,20,0]))) or (np.array_equal(ob[10*(y+1)][10*x],np.array([255,30,0]))):
						dis = 0
				if dis==1 and y==(y_max-1):
					dis = 0
			else:
				if x< x_max-1:
					if(np.array_equal(ob[10*y][10*(x+1)],np.array([1,0,0]))) or (np.array_equal(ob[10*y][10*(x+1)],np.array([255,10,0]))) or (np.array_equal(ob[10*y][10*(x+1)],np.array([255,20,0]))) or (np.array_equal(ob[10*y][10*(x+1)],np.array([255,30,0]))):
						dis = 0
				if dis==1 and x==(x_max-1):
					dis=0

			return dis
			
		def dec(ob,x,y,d):
			'''function to determine presence of obstacle while snake's head is facing negative x or y axis.'''
			dis = 1
			if d==0:
				if y>0:
					if(np.array_equal(ob[10*(y-1)][10*x],np.array([1,0,0]))) or (np.array_equal(ob[10*(y-1)][10*x],np.array([255,10,0]))) or (np.array_equal(ob[10*(y-1)][10*x],np.array([255,20,0]))) or (np.array_equal(ob[10*(y-1)][10*x],np.array([255,30,0]))):
						dis = 0
				if dis==1 and y==0:
					dis= 0
			else:
				if x>0:
					if(np.array_equal(ob[10*y][10*(x-1)],np.array([1,0,0]))) or (np.array_equal(ob[10*y][10*(x-1)],np.array([255,10,0]))) or (np.array_equal(ob[10*y][10*(x-1)],np.array([255,10,0]))) or (np.array_equal(ob[10*y][10*(x-1)],np.array([255,30,0]))):
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
	tot_rew = [0,0,0]
	obs = env.reset()
	done = False
	steps = [0,0,0]
	dr1 = 2
	dr2 = 2
	dr3 = 2
	def to_relative(strng):
		if strng=="Left":
			act = 0
		if strng=="Forward":
			act = 1
		if strng=="Right":
			act = 2
		return act

	#loop to play in one episode unitl snake dies. Episode ends when either of 2 snakes dies.
	while not done: 
		x1 ,y1 = get_loc(obs,1)
		x2, y2 = get_loc(obs,2)
		x3, y3 = get_loc(obs,3)
		fru_lis = get_fruit(obs)
		
		x_f1,y_f1,x_f2,y_f2,x_f3,y_f3 = fru_lis[0],fru_lis[1],fru_lis[2],fru_lis[3],fru_lis[4],fru_lis[5]
		
		frud1,fob1,lob1,rob1 = get_state(obs,x1,y1,x_f1,y_f1,dr1)
		frud2,fob2,lob2,rob2 = get_state(obs,x2,y2,x_f2,y_f2,dr2)
		frud3,fob3,lob3,rob3 = get_state(obs,x3,y3,x_f3,y_f3,dr3)
		
		action1,st1 = policy(epsilon,dr1,frud1,fob1,lob1,rob1)
		action2,st2 = policy(epsilon,dr2,frud2,fob2,lob2,rob2)
		action3,st3 = policy(epsilon,dr3,frud3,fob3,lob3,rob3)
		
		dr_new1 = action1
		dr_new2 = action2
		dr_new3 = action3
		
		obs,rew,done, info = env.step([action1,action2,action3])
		
		if rew[0]==1 or rew[1]==1 or rew[2]==1:
			fru_lis = get_fruit(obs)
			x_f1,y_f1,x_f2,y_f2,x_f3,y_f3 = fru_lis[0],fru_lis[1],fru_lis[2],fru_lis[3],fru_lis[4],fru_lis[5]

		action1 = to_relative(st1)
		action2 = to_relative(st2)
		action3 = to_relative(st3)
		
		if rew[0]==-1 or rew[1]==-1 or rew[2]==-1:
			done=True
		else:
			x_new1 ,y_new1 = get_loc(obs,1)
			x_new2 ,y_new2 = get_loc(obs,2)
			x_new3 ,y_new3 = get_loc(obs,3)
	
		frud_new1,fob_new1,lob_new1,rob_new1 = get_state(obs,x_new1,y_new1,x_f1,y_f1,dr_new1)
		frud_new2,fob_new2,lob_new2,rob_new2 = get_state(obs,x_new2,y_new2,x_f2,y_f2,dr_new2)
		frud_new3,fob_new3,lob_new3,rob_new3 = get_state(obs,x_new3,y_new3,x_f3,y_f3,dr_new3)
		
		steps[0] += 1
		steps[1] += 1
		steps[2] += 1
		#uncoment below line to run at slower speed
		#time.sleep(2)
		env.render()
		tot_rew[0] +=rew[0]
		tot_rew[1] +=rew[1]
		tot_rew[2] +=rew[2]
		
		#Comment below two for epsilon =0
		#q_val[frud1,fob1,lob1,rob1,action1] += alpha*(rew[0] + gamma*(np.max(q_val[frud_new1,fob_new1,lob_new1,rob_new1])) - q_val[frud1,fob1,lob1,rob1,action1])
		#q_val[frud2,fob2,lob2,rob2,action2] += alpha*(rew[1] + gamma*(np.max(q_val[frud_new2,fob_new2,lob_new2,rob_new2])) - q_val[frud2,fob2,lob2,rob2,action2])
		#q_val[frud3,fob3,lob3,rob3,action3] += alpha*(rew[2] + gamma*(np.max(q_val[frud_new3,fob_new3,lob_new3,rob_new3])) - q_val[frud3,fob3,lob3,rob3,action3])
		dr1 = dr_new1
		frud1 = frud_new1
		fob1 = fob_new1
		lob1 = lob_new1
		rob1 = rob_new1
		
		dr2 = dr_new2
		frud2 = frud_new2
		fob2 = fob_new2
		lob2 = lob_new2
		rob2 = rob_new2
		
		dr3 = dr_new3
		frud3 = frud_new3
		fob3 = fob_new3
		lob3 = lob_new3
		rob3 = rob_new3
	return tot_rew,steps

if __name__ =="__main__":
	rew_list = [[],[],[]]
	step_list = [[],[],[]]
	#In windows uncomment below line.In linux use next 7 lines and comment below line. 
	env = gym.make(id=name,grid_size=[y_max,x_max], unit_size=10, unit_gap=1, snake_size=3, n_snakes=3, n_foods=3, random_init=True)
	
	# env = gym.make(id=name)
	# env.grid_size = [y_max,x_max]
	# env.unit_size = 10
	# env.unit_gap = 1
	# env.snake_size = 3
	# env.n_snakes = 3
	# env.n_foods = 3
		
	alpha = 0.1
	gamma = 0.2
	ep = 40
	for i in range(0,ep):
		#rew,steps = gen_episode(env,alpha,gamma,(500/(500+i)))
		'''For epsilon =0. Uncomment below line'''
		rew,steps = gen_episode(env,alpha,gamma,0) 
		print("episode "+str(i+1)+" ended.Reward = "+str(rew))
		rew_list[0].append(rew[0])
		rew_list[1].append(rew[1])
		rew_list[2].append(rew[2])
		step_list[0].append(steps[0])
		step_list[1].append(steps[1])
		step_list[2].append(steps[2])
		
	
	plt.clf()
	plt.plot(rew_list[0])
	plt.plot(rew_list[1])
	plt.plot(rew_list[2])
	plt.legend(['Snake 1','Snake 2','Snake 3'])
	plt.savefig('qrew_mul3.png')
	plt.clf()
	plt.plot(step_list[0])
	plt.plot(step_list[1])
	plt.plot(step_list[2])
	plt.legend(['Snake 1','Snake 2','Snake 3'])
	plt.savefig('q_steps_mul3.png')
	plt.clf()
	#np.save('q_rewards',np.array(rew_list))
	#np.save('q_steps',np.array(step_list))
