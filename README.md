TP3
===

To install ROS goto:

http://wiki.ros.org/hydro/Installation/Ubuntu

And install ROS-hydro

To install Clopema software goto:

http://clopema.felk.cvut.cz/redmine/projects/clopema/wiki/Packages_instalation_%28hydro%29_

And follow those instructions except when it says to install ROS hydro (you should already have it installed) and when it says to do wstool init. Instead of using wstool init just go to the bitbucket repo and clone it into your src folder.
Also make sure you set up your environment variables before you try to catkin_make. The package installer tutorial has the environment variable step after the catkin_make step but it should be performed first. Use CLOPEMA_PARTNER=LOCAL.

