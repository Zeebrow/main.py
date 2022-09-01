# quickhost

Make a publically accessible host, quickly.

## Usage

```
usage: main.py [-h] [-f CONFIG_FILE] {make,describe,update,destroy} ... app_name
```

`quickhost` is still under development. Only aws is supported as a cloud
provider option.

```
git clone https://github.com/zeebrow/quickhost.git
git clone https://github.com/zeebrow/quickhost-plugins.git
python3 -m venv venv && source venv/bin/activate
pip install -e quickhost
pip install -e quickhost-plugins/plugins/aws
```

See the aws plugin [README.md](https://github.com/zeebrow/quickhost-plugins/plugins/aws/README.md) 
for help setting up an aws account and boilerplate cloud resources.


## Build

### pyinstaller

```
pip install requirements.txt
pip install -e .
# we don't have a pip package yet
pip install /path/to/plugin*

# this is the opposite of a 'plugin'
pyinstaller -n quickhost --collect-all boto3 --collect-all quickhost_aws src/scripts/main.py -F

```

