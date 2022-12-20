# chess-machine
```
sudo apt install git python3-pip -y
git clone https://github.com/Aritj/chess-machine.git
pip3 install -r chess-machine/requirements.txt
python3 chess-machine/app.py
```

# Prerequisites
[Pigpiod](https://abyz.me.uk/rpi/pigpio/download.html)
[Pigpiod.service (RPi)](https://forums.raspberrypi.com/viewtopic.php?t=319761)

## Pigpiod
Download and install pigpiod:
```
wget https://github.com/joan2937/pigpio/archive/master.zip
unzip master.zip
cd pigpio-master
make
sudo make install
```

If the Python part of the install fails it may be because you need the setup tools:
```
sudo apt install python-setuptools python3-setuptools
```

Create the following file (if it does not exist already):
```
sudo nano /lib/systemd/system/pigpiod.service
```

And paste in the following contents:
```
[Unit]
Description=Daemon required to control GPIO pins via pigpio
[Service]
ExecStart=/usr/local/bin/pigpiod
ExecStop=/bin/systemctl kill -s SIGKILL pigpiod
Type=forking
[Install]
WantedBy=multi-user.target
```

And then issue the following commands:
```
sudo systemctl enable pigpiod
sudo systemctl start pigpiod
sudo systemctl status pigpiod
```

