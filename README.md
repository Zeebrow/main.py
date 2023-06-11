# quickhost

Make a publically accessible host, quickly.

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

### ~~pyinstaller~~

#### do this
```
git clone https://github.com/zeebrow/quickhost.git
git clone https://github.com/zeebrow/quickhost-aws.git plugins/aws
python3 -m venv venv && source venv/bin/activate
pip install -e quickhost
pip install -e quickhost-plugins/plugins/aws
```

