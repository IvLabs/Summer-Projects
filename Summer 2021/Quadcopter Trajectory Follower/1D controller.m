function [ u ] = pd_controller(~, s, s_des, params)
%PD_CONTROLLER  PD controller for the height
%
%   s: 2x1 vector containing the current state [z; v_z]
%   s_des: 2x1 vector containing desired state [z; v_z]
%   params: robot parameters
m=params.mass;
g=params.gravity;
zdes_dd=0;
kp=100;
kv=16;
%u = m*g;
% e: 2x1 Vector encompassing the error state and its derivative 
e=s_des-s;
u= m*(zdes_dd+ kp*e(1)+kv*e(2)+g);

end
