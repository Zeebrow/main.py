from setuptools import setup, find_packages

print(f"setup.py=====> {find_packages(where='src/quickhost_aws')}")

setup(
    name='quickhost_aws',
    version='0.0.1',
    package_dir={'quickhost_aws':'aws/src/quickhost_aws'},
    packages=find_packages(where='src/quickhost_aws'),
    install_requires=[
        'boto3'
    ],
    #depends_on=
    entry_points={
        "quickhost_plugin": ['quickhost_aws=quickhost_aws:get_app']
    }
)
