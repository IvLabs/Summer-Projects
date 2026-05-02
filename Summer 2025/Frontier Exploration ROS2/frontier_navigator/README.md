# The Frontier Exploration Algorithm

This folder contains the frontier-based exploration algorithm used by the bot to autonomously navigate it's path using occupancy grid maps. The algorithm extracts frontier edges, computes centroids, and sends navigation goals to Nav2, highlighting points of interest using ROS2 markers in RViz.

Sequence to implement autonomous exploration algorithm on your system:

- Launch Gazebo, SLAM Toolbox and Nav2 Stack on seperate terminals in this exact order.
- Launch the frontier_navigator node.
- Launch RViz2 in another terminal to visualize map generation and autonomous navigation by the bot.
