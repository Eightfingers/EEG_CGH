% X, Y, Z, W
[0.00706000000000000,-0.0428190000000000,0.00287000000000000,-0.999054000000000]

% W, X , Y ,Z
quat1 = [0.264311000000000, -0.959947000000000,-0.0463460000000000,-0.0805840000000000];
quat1 = quaternion([0.264311000000000, -0.959947000000000,-0.0463460000000000,-0.0805840000000000]);

RPY1 = eulerd(quat1,'XYZ', 'frame' );

eul = [-0.797105000000000,4.91033100000000,-0.295025000000000];

% In optitrack, the quaternion follows q=x*i+y*j+z*k+w; However, In matlab, the quaternion follows q=w+x*i+y*j+z*k.
% As long as I change the quaternion form from optitrack representation into matlab representation, then it works.

% quat = [0.7071 0.7071 0 0];
% eulXYZ = quat2eul(quat,'XYZ')
% quat2 = eul2quat(eulXYZ, 'XYZ');
% 
% 
% quat = quaternion([0.7071 0.7071 0 0]);
% eulerAnglesDegrees = eulerd(quat,'ZYX','frame')


% /* Convert quaternion to Euler angles (in radians). */
% EulerAngles Eul_FromQuat(Quat q, int order)
% {
%     HMatrix M;
%     double Nq = q.x*q.x+q.y*q.y+q.z*q.z+q.w*q.w;
%     double s = (Nq > 0.0) ? (2.0 / Nq) : 0.0;
%     double xs = q.x*s,	  ys = q.y*s,	 zs = q.z*s;
%     double wx = q.w*xs,	  wy = q.w*ys,	 wz = q.w*zs;
%     double xx = q.x*xs,	  xy = q.x*ys,	 xz = q.x*zs;
%     double yy = q.y*ys,	  yz = q.y*zs,	 zz = q.z*zs;
%     M[X][X] = 1.0 - (yy + zz); M[X][Y] = xy - wz; M[X][Z] = xz + wy;
%     M[Y][X] = xy + wz; M[Y][Y] = 1.0 - (xx + zz); M[Y][Z] = yz - wx;
%     M[Z][X] = xz - wy; M[Z][Y] = yz + wx; M[Z][Z] = 1.0 - (xx + yy);
%     M[W][X]=M[W][Y]=M[W][Z]=M[X][W]=M[Y][W]=M[Z][W]=0.0; M[W][W]=1.0;
%     return (Eul_FromHMatrix(M, order));
% }
