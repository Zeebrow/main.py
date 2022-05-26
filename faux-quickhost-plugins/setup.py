from setuptools import setup, find_packages

setup(
    name='quickhost-aws',
    version='0.0.1',
    package_dir={'':'aws'},
    packages=find_packages(where='aws/src'),
    install_requires=[
        'boto3'
    ],
    #scripts=['src/scripts/main.py']
)
