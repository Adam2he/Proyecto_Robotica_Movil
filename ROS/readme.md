# Instructions to set up RViz: #

1. Enter in a console window:
~~~
roscore
~~~

2. Enter in another console window:
~~~
rosrun tf static_transform_publisher 0 0 0 0 0 0 1 map base_link 100
~~~

3. Enter in another console window:
~~~
rosrun rviz rviz
~~~

4. Load the custom.rviz file in the RViz workspace.

5. Install planner.py and launch it with the following command and the number of obstacles to add:
~~~
rosrun planner planner.py 1000
~~~
