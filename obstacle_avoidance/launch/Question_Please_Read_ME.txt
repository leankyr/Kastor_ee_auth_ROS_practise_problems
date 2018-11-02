I suppose it is normal for the (x,y) = (0,0) of occupancy grid map to be at the initial pose (x =1,y=2)
of the robot at the stdr_simulator.
As a result there is always a fixed distance (x=1,y=2)between the robot0 frame and the base_footprint frame introduced by crsm node. 
Should I make the two frames match with tf?? robot0 frame to be always in accordance to base_footprint frame??
or should I assume that the map is uknown and we don't care the coordinate system of the "real" world STDR simulator world is that case?  
Should I change the initial pose of crsm from x,y = (0,0) to x,y = (1,2)?? 
or somehow make the (0,0) of the static map match the (0,0) of the occupancy grid map like some ppl do in the gazebo simulator?
The expected tf tree of the task is as in the picture??

However I have a feeling that everything is quite normal
