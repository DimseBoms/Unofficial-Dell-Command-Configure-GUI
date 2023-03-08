# If you have trouble installing DCC
* You can try another version of basically the same program, except that it exists in the system tray (https://github.com/DimseBoms/dell-power-tray). This version uses libsmbios (https://github.com/dell/libsmbios) as a backend which is less complex, faster and open-source.

# Unofficial Dell Command GUI
Simple, unofficial frontend to control some of the functions from Dell Command Configure. Can be used to change thermal management options, battery charge behaviour and keyboard backlight.

Pull requests are welcome

[<img src="https://raw.githubusercontent.com/DimseBoms/Unofficial-Dell-Command-Configure-GUI/main/Screenshot.png">](https://raw.githubusercontent.com/DimseBoms/Unofficial-Dell-Command-Configure-GUI/main/Screenshot.png)

## Requirements
* Requires Dell Command Configure. This can be downloaded from <https://www.dell.com/support/home/products/laptop> by searching for your laptop model.
  * If you are on Ubuntu 22.04 or later there's a missing dependency preventing installation. The missing dependency can be installed with this command:
  ```
  wget http://nz2.archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2.16_amd64.deb && sudo dpkg -i libssl1.1_1.1.1f-1ubuntu2.16_amd64.deb
  ```
 * python-gi
 * gtk4
 * libadwaita

## Installation
* Navigate to where you want the utility to reside
```
cd ~/.local/share
```
* Clone the repo
```
git clone https://github.com/DimseBoms/Unofficial-Dell-Command-Configure-GUI
```
* Navigate to the newly downloaded repo
```
cd ./Unofficial-Dell-Command-Configure-GUI
```
* Add the utility to your application menu
```
python3 main.py --install
```
* To make the Dell Command Configure backend accessible without having to use passwords we have to add an entry to the bottom of /etc/sudoers using visudo:
```
sudo visudo
```
```
# Dell CCTK
[YOUR_USERNAME_HERE_WITHOUT_BRACES] ALL = NOPASSWD: /opt/dell/dcc/cctk
```
