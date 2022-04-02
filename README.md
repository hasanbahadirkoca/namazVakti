# NamazVakti for Raspberry Pi with Python

### Step 2 – Create A Unit File

Next we will create a configuration file (aka a unit file) that tells systemd what we want it to do and when:

    sudo nano /lib/systemd/system/namazVakti.service

Add in the following text:

    [Unit]
    Description=NamazVakti Python Service
    After=multi-user.target

    [Service]
    Type=idle
    ExecStart=/usr/bin/python /home/pi/namazVakti/main.py
    #In order to store the script’s text output in a log file you can change the ExecStart line to :
    #ExecStart=/usr/bin/python /home/pi/namazVakti/main.py > /home/pi/namazVakti/main.log 2>&1
    WorkingDirectory=/home/pi/namazVakti/
    User=pi

    [Install]
    WantedBy=multi-user.target

The permission on the unit file needs to be set to 644:

    sudo chmod 644 /lib/systemd/system/namazVakti.service


### Step 3 – Configure systemd

    sudo systemctl daemon-reload
    sudo systemctl enable namazVakti.service
