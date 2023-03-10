# quickhost

Make a publically accessible host, quickly.

## Usage

```
$ main.py -h
usage: main.py [-h] [-f CONFIG_FILE] {aws,null} ...

positional arguments:
  {aws,null}

options:
  -h, --help            show this help message and exit
  -f CONFIG_FILE, --config-file CONFIG_FILE
                        Use an alternative configuration file to override the default.
```


## ~~Build~~

### ~~pyinstaller~~

#### do this
```
git clone https://github.com/zeebrow/quickhost.git
git clone https://github.com/zeebrow/quickhost-plugins.git
python3 -m venv venv && source venv/bin/activate
pip install -e quickhost
pip install -e quickhost-plugins/plugins/aws
```

