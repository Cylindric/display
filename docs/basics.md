# Waveshare 7.5" e-Paper Display

## Hardware

* Waveshare 7.5" e-Paper Display, V2, 800x480
* e-Paper Driver HAT, Rev 2.2 [Manual](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_Manual)
* ~~RaspberryPi 3 Model B+ (2017)~~
* RaspberryPi 3 Model B V1.2 (2015)

```bash
sudo apt update
sudo apt full-upgrade
sudo raspi-config
# Interface Options -> SPI -> Yes Enable
sudo reboot

sudo pip3 install virtualenv
sudo pip3 install virtualenvwrapper
echo "export VIRTUALENVWRAPPER_PYTHON='/usr/bin/python3'" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
source ~/.bashrc

mkdir -p ~/dev/display
cd ~/dev/display
mkvenv display
workon display

git clone https://github.com/waveshare/e-Paper.git ~/dev/e-Paper
pip install ~/dev/e-Paper/RaspberryPi_JetsonNano/python
```