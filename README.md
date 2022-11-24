## Laptop configuration

### Required software
- [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
- [Visual Studio Code (VS Code)](https://code.visualstudio.com/download)
- [Python](https://www.python.org/downloads/)
- [Node.js 12](https://nodejs.org/en/download/)

### Required VS Code extensions
- `Python`
- `Remote - SSH`
- `Remote Development`

## Network Configuration
- Ask the professor
- Add a static DHCP lease for each robot
- Add all IP addresses as DNS A records for `stingrayXX` hostnames

## Stingray Configuration

- If you have more than one robot, repeat this section for each robot.

### Materials needed
- Stingray robot
- SD card
- Keyboard with battery charged
- Two Stingray batteries (Lithium Ion 7.4V, 7000mAh)
- Optional: AC adapter for Stingray

### Hardware preparation

#### General recommendations
- Never plug in the robot batteries with different levels of charge, as it may cause fire instantaneously
- When on the workbench, always leave the robot on the puck, so it doesn't run away
- if the robot is without batteries, you will need to use two pucks or a 120mm fan as support
- Do not discharge the battery below 6.0V (7.0V recommended), or you may damage the batteries

#### Robot battery charging
- Read the DuraTrax Onyx 245 charger manual: `Documentation/dtxp4245-manual-v2.pdf`
- Select `LiIon` battery type
- Set the charging current to `1.50A`
- Start charging the batteries
- The charger will beep in case of error or when it finishes

### Install operating system
- To avoid accidents, unplug all the removable storages from your computer
- Plug the SDHC card from the stingray into your computer
- Open Raspberry Pi Imager on your laptop
- Choose OS: `Raspberry Pi OS (64-bit)`
- Choose Storage: Select the SDHC card
- Click the gear icon to configure
- Set hostname: `stingrayXX`, where XX is the robot number with two digits
- Enable SSH with password authentication
- Set username and password: username = `pi`, password = `stingray`
- Configure wireless LAN: Ask the professor for credentials, country = `CA`
- Set locale settings: Timezone = `America/Toronto`

### Turn on the robot
- Insert the SD card into the robot Raspberry Pi SD slot
- Plug the AC adapter or the batteries on the robot
- Flip the switch to the `On` or `Bat` position
- Wait for the operating system to boot until desktop shows on LCD

### Connect VS Code to robot
- Open VS Code on the laptop
- Click on the green icon on bottom left corner to connect to remote
- Click on `Connect to Host...` on the `Remote - SSH` extension drop down menu
- Click `Add New SSH Host...`
- Type `pi@stingrayXX` as the SSH command
- Select `C:\Users\<username>\.ssh\config` as the configuration file
- Click on the green icon on bottom left corner again
- Click on `Connect to Host...` again
- Select the newly created `stingrayXX` SSH host
- VS Code will open a new window and ask for the operation system. Select `Linux`
- Select `Continue` if it asks for a confirmation about the SSH fingerprint
- Type the password `stingray`, created when flashing the image to the SD card
- Click on `Terminal` on the top of the VS Code window
- Select the `New Terminal` option on the drop down menu
- The stingray operating system terminal will open on the bottom of the VS Code window

### Prepare the Stingray operating system
- Run the following commands on the stingray terminal
- Update installed packages  
`sudo apt update`  
`sudo apt upgrade`  
- Install required libraries  
`sudo apt install python3-pigpio pigpio python3-decouple python3-opencv`  
`pip install tflite-runtime`  
- Enable and start pigpiod  
`sudo systemctl enable pigpiod`  
`sudo systemctl start pigpiod`  
- Check if python version is 3.9 (Newer versions may work):  
`python3 --version`  
- Clone the Stingray2 ncctlab repository  
`cd ~`  
`git clone https://github.com/ncctlab/ncct-stingray2`  
`cd ncct-stingray2`  
- Prepare the `stingrayd` Python virtual environment (venv)  
`cd stingrayd`  
`python3 -m venv venv`  
`source venv/bin/activate`  
`pip install -r requirements.txt`  
`deactivate`  
- Create a .env file with the stingrayd IoT Hub credentials  
`code .env`   
- Give VS Code authorization if it asks and put this content into the file  
```
#-- Azure IoT Hub
CONNECTION_STRING=
```
- Save the file and minimize the window

### Add robot as Azure IoT Device
- Go to [Azure Portal](https://portal.azure.com/#home)
- Open your Azure IoT Hub resource.
- Select `Devices`.
- Select `Add Device`.
- Device ID: StingrayXX.
- IoT Edge Device: False
- Authentication type: Symmetric key
- Auto-generate keys: True
- Connect this device to an IoT Hub: Enable
- Parent device: No parent device
- Click `Save`.
- Back to the `Devices` screen. Click `Refresh`.
- Click on the the `StingrayXX` created.
- Copy the Primary Connection String.

### Set the Azure Connection String on the robot
- Go back to the VS Code window with stingrayd .env file open
- Paste the Primary Connection String after the equal sign in the line that starts with `CONNECTION_STRING=`
- Save the file and close it clicking on the X sign next to its name on VS Code

### Install stingrayd
- Install stingrayd as a system service  
`sudo cp stingrayd.service /usr/lib/systemd/system/`  
- Create a symbolic link to git repository folder  
`cd /opt`  
`sudo ln -s /home/pi/ncct-stingray2/stingrayd/ stingrayd`  
- Check if the symbolic link was successfully  
`ls -lha`  
- Enable the service (start automatically when the system starts)  
`sudo systemctl enable stingrayd`  
`sudo systemctl start stingrayd`  
- Check if it starts correctly  
`systemctl status stingrayd`  
- Press q to exit the command

### Prepare VS Code to run the stingray code
- Go to the stingray code folder
`cd ~/ncct-stingray2/stingray`  
`code .`  
- VS Code will open a new window and ask for the SSH password again
- Give permission for VS Code to trust the folder authors if it asks
- You can now close the window that you were working before
- VSCode will now have `stingray` as the root folder
#### Install the Python extension on VSCode remote
- On the new VSCode window, click on extensions icon
- Search for the Python extension and click on `Install in SSH: stingrayXX`

### Create a new YouTube live stream
- Refer to the [YouTube live stream documentation](https://www.youtube.com/howyoutubeworks/product-features/live/#youtube-live) for more information
- Go to [YouTube Studio](https://studio.youtube.com/)
- Click on the live stream icon
- On the `Select transmission key` combo box, select `Create a new streaming key`
- Name it `StingrayXX`
- Click on `Create`
- Select your new stream key on the same combo box to check if it was created correctly
- There you can see the stream key and the streaming URL
- Minimize the web browser

### Create the `.env` configuration file for the stingray code
- On VSCode root folder, copy `.env_example` as `.env`
- Open the new `.env` file and change the contents as needed
- The `STREAM_LINK` shoud be "stream link"/"stream key" (follow the example)

### Run the stingray code
- Open `main.py`
- Click `F5` on your keyboard
- If everything goes well, the code will run and the camera should stream to the YouTube live interface
- You can stop the code by clicking on the red stop button

### Power off the robot
- Issue a `sudo poweroff` command on the terminal or use the GUI on robot LCD
