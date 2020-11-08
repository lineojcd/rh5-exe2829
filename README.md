# rh5-exe2829
rh5-exe2829: Duckietown RH5 exe 27, 28 and 29

## How to use it

### 1. Fork and go to this repository

Use the fork button in the top-right corner of the github page to fork this template repository.

### 2. Open another terminal and run
```bash
dts duckiebot keyboard_control MY_ROBOT_NAME
```

### 3. In your original terminal
In your code folder run,
```bash
dts devel build -f --arch amd64
```

### 4. Run your code
In your code folder run,
```bash
docker run -it --rm -e ROS_MASTER_URI=http://[DUCKIE_BOT_IP]:11311/ -e ROS_IP=http://[LAPTOP_IP]:11311/ --net host duckietown/rh5-exe2829:latest-amd64
```

### 5. In another terminal run:
```bash
docker run -v [PATH_TO_BAG_FOLDER]:/home  -it --rm --net host -e ROS_MASTER_URI="http://[DUCKIE_BOT_IP]:11311" -e ROS_IP=[LAPTOP_IP] duckietown/dt-ros-commons:daffy-amd64 /bin/bash
rosbag record /MY_ROBOT_NAME/right_wheel_encoder_node/tick /MY_ROBOT_NAME/left_wheel_encoder_node/tick /MY_ROBOT_NAME/wheels_driver_node/wheels_cmd /MY_ROBOT_NAME/my_left_travel_dist /MY_ROBOT_NAME/my_right_travel_dist
```

Now you can use the keyboard to control the duckitbot and the rosbad is recording the topic that you are subscribing.
