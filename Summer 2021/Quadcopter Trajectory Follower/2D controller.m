function [ u1, u2 ] = controller(~, state, des_state, params)
%CONTROLLER  Controller for the planar quadrotor
%
%   state: The current state of the robot with the following fields:
%   state.pos = [y; z], state.vel = [y_dot; z_dot], state.rot = [phi],
%   state.omega = [phi_dot]
%
%   des_state: The desired states are:
%   des_state.pos = [y; z], des_state.vel = [y_dot; z_dot], des_state.acc =
%   [y_ddot; z_ddot]
%
%   params: robot parameters

%   Using these current and desired states, the desired has to computed
%   controls
m=params.mass;
g=params.gravity;
Ixx=params.Ixx;
kp1=500;
kd1=100;
y_dd=des_state.acc(1);
z_dd=des_state.acc(2);
% FILL IN YOUR CODE HERE
e_z=des_state.pos(2)-state.pos(2);
e_zdot=des_state.vel(2)-state.vel(2);
e_y=(des_state.pos(1)-state.pos(1));
e_ydot=des_state.vel(1)-state.vel(1);
kp=50;
kv=10;
kp2=1000;
kd2=50;
    
u1 = m*(g+z_dd+kp1*e_z+kd1*e_zdot);
phi_c=-(y_dd+kp*e_y+kv*e_ydot)/g;
u2 = Ixx*(kp2*(phi_c-state.rot(1))+kd2*(0-state.omega(1)));

end

