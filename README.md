## Azure configuration

## Stingray Configuration

### Create raspberry pi 4 image on sd card.
- Install ['Raspberry Pi Imager'](https://www.raspberrypi.com/software/)
- Choose OS: Raspberry Pi OS x64
- Choose Storage: selected SD Card.
- host: pi@stingray<number>
- password: stingray

### Azure IoT Hub Device

- Open Azure IoT Hub Service.
- Select 'Devices'.
- Select 'Add Device'.
- Device ID: Stingray<number>.
- Save.
- Select the Stingray<number> created.
- Copy the Primary Connection String.

### SSH connection for VScode
- Install the VScode SSH extension.
- Click on the VScode green SSH button on the bottom.
- Select 'Connect to Host'...
- Select 'Add New SSH Host...'
- Select the host created. Example: stingray30
- Select platform 'Linux'.
- Put the password.
Connection was established.

### Environment

- Check if python version 3.9 (Newer versions may work):
`python3 --version`
#### VScode recomended extensions
- Python

#### Install repository
- Clone repo:
`cd ~`
`git clone <repo_name>`
`cd <repo_name>/server`
`python3 -m venv venv`
`source venv/bin/activate`
`pip install -r requirements.txt`

- Create a .env file with the credentials in server and controller folders. Write the Azure credentials.
```
#-- Azure IoT Hub
CONNECTION_STRING=<AZURE DEVICE PRIMARY CONNECTION STRING>
```

#### Install stingrayd
- Install stingrayd as a system service:
`sudo cp /<repo_name>/server stingrayd.service /usr/lib/systemd/system/`
- Create a symbolic link to git repository folder:
`cd /opt`
`sudo ln -s /home/pi/<repo_name>/server/ stingrayd`
- Check if the symbolic link was successfully:
`ls -lha`
- Enable the service (start automatically when the system starts):
`sudo systemctl enable stingrayd`
`sudo systemctl start stingrayd`
- Check if it starts correctly:
`systemctl status stingrayd`
- If active, press q to exit.
Stingrayd is running and connected to Azure Cloud.

#### Stingray robot configuration
- Install packages. Do not use virtualenv to client packages because pypi do not have the camera libraries.
`sudo apt install python3-pigpio pigpio python3-decouple`
- Enable and start pigpiod
`sudo systemctl enable pigpiod`
`sudo systemctl start pigpiod`
- Open VScode window in client folder.