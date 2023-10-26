from functools import partial
from setuptools import setup
from setuptools.command.install import install

import os
import sys


def get_config_dir() -> str:
    if sys.platform == 'linux':
        return os.path.join(os.path.expanduser("~"), ".config", "quickhost")  # XDG
    elif sys.platform in ['win32', 'cygwin']:
        return os.path.join(os.path.expanduser("~"), ".quickhost.conf")  # ???
    elif sys.platform == 'darwin':
        return os.path.join(os.path.expanduser("~"), ".config", "quickhost")  # ...???
    else:
        raise Exception("Unsupported platform '{}'".format(sys.platform))

def write_default_config_file() -> None:
    with open( os.path.join(get_config_dir(), "quickhost.conf"), 'w' ) as f:
        f.write("\n")

class CustomInstaller(install):
    def run(self) -> None:
        """
        create required files for quickhost
        assumes that the program will be run by a human bean with a home directory
        """
        qh_config_dir = get_config_dir()
        qh_config_file = os.path.join(qh_config_dir, "quickhost.conf")
        
        if not os.path.exists(qh_config_file):
            self.mkpath(get_config_dir(), 0o777)
            self.execute(write_default_config_file, (), "writing default config file")

        install.run(self)

setup_quickhost = partial(
    setup,
    cmdclass={'install': CustomInstaller}
)

setup_quickhost()