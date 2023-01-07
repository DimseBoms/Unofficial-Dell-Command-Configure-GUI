# Unofficial Dell Command GUI
Simple, unofficial frontend to control some of the functions from Dell Command Configure. Can be used to change thermal management options, battery charge behaviour as well as battery charge tresholds.

[<img src="https://raw.githubusercontent.com/DimseBoms/Unofficial-Dell-Command-Configure-GUI/main/Screenshot.png">](https://raw.githubusercontent.com/DimseBoms/Unofficial-Dell-Command-Configure-GUI/main/Screenshot.png)

## Requirements
* Requires Dell Command Configure. This can be downloaded from <https://www.dell.com/support/home/products/laptop> by searching for your laptop model.
  * If you are on Ubuntu 22.04 or later there's a missing dependency preventing installation. The missing dependency can be installed with this command:
  ```
  wget http://nz2.archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2.16_amd64.deb && sudo dpkg -i libssl1.1_1.1.1f-1ubuntu2.16_amd64.deb
  ```
 * python-gi

## Installation
* Navigate to where you want the utility to reside
```
cd ~/.local/share
```
* Clone the repo
```
git clone https://github.com/DimseBoms/Unofficial-Dell-Command-Configure-GUI
```
* Add the utility to your application menu
```
python3 ./Unofficial-Dell-Command-Configure-GUI/main.py --install
```
* To make the Dell Command Configure backend accessible without having to use passwords we have to add an entry to the bottom of /etc/sudoers using visudo:
```
sudo visudo
```
```
# Dell CCTK
[YOUR_USERNAME_HERE_WITHOUT_BRACES] ALL = NOPASSWD: /opt/dell/dcc/cctk
```
