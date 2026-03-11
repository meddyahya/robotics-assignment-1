### 1. Make the Node and Launch FileExecutable
Before running, give execution permission to the node script:
```bash
chmod +x ./packages/avoid_duck/src/wheel_control_node.py
chmod +x ./launchers/wheel-control.sh
```
### 2. Run Options

You have two ways to build and run the node:

🔹 Terminal Commands

This allows you to test quickly over the ROS network, but note there can be some delay with the ToF sensor.
```bash
dts devel build -f
dts devel run -R ROBOT_NAME -L wheel-control
```
