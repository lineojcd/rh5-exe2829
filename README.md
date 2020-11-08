# rh5-exe2829
rh5-exe28_29: Duckie Town RH5 exe 27, 28 and 29

## How to use it

### 2. Fork and go to this repository

Use the fork button in the top-right corner of the github page to fork this template repository.

### 3. Build your code
In your code folder run,
```bash
dts devel build -f
```

### 4. Run your code
In your code folder run,
```bash
dts devel run
```

### 5. In another terminal run:
```bash
dts start_gui_tools
rqt_image_view
choose to subscribe /fakebot/camera_node/image/compressed
```

### 6. In another terminal run:
```bash
dts duckiebot keyboard_control fakebot
```

Now you can use the virtual joystick to control the duckie bot in the simulation world.
