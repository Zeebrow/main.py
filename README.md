# quickhost

## 



## Usage

```
$ main.py null -h
usage: main.py null [-h] {init,make,describe,update,destroy,list-all,destroy-all} ...

positional arguments:
  {init,make,describe,update,destroy,list-all,destroy-all}
    init                plugin initialization help
    make                make an app help
    describe            show details about an app help
    update              change an app help
    destroy             destroy an app help
    list-all            list all running apps
    destroy-all         remove the plugin help

options:
  -h, --help            show this help message and exit

```


## ~~Build~~

### Python 3.7, 3.8

i dunno tox :( 


install Python, e.g.

`sudo apt-get install python3.8`

install pip

```
sudo apt install python3.8-distutils
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.8 get-pip.py
```

and your choice of venv

```
sudo apt install python3.8-venv
```

### ~~pyinstaller~~

#### do this
```
git clone https://github.com/zeebrow/quickhost.git
git clone https://github.com/zeebrow/quickhost-aws.git plugins/aws
python3 -m venv venv && source venv/bin/activate
pip install -e quickhost
pip install -e quickhost-plugins/plugins/aws
```
