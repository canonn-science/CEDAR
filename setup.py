from setuptools import setup, find_packages
import re
import glob

VERSIONFILE = "src/cedar/conf/Version.py"
verstr      = "unknown"
try:
    verstrline = open(VERSIONFILE, "rt").read()
    VSRE       = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo         = re.search(VSRE, verstrline, re.M)
    if mo:
        verstr = mo.group(1)
except EnvironmentError:
    print "unable to find version in %s" % (VERSIONFILE,)
    raise RuntimeError("if %s exists, it is required to be well-formed" % (VERSIONFILE,))


setup(
    name='cedar',
    version=verstr,
    description='Canonn Elite Dangerous Automated Relay',
    author='Canonn R&D Team',
    author_email='rd@canonn.tech',
    url='https://github.com/Canonn-Science/CEDAR',
    packages=find_packages('src', exclude=["*.tests"]),
    package_dir = {'':'src'},
    data_files=[('cedar/schemas', glob.glob("schemas/*.json"))],
    long_description="""The Canonn Elite Dangerous Data Network allows E:D players to share data. Not affiliated with Frontier Developments.""",
    install_requires=["argparse", "bottle", "enum34", "gevent", "jsonschema", "pyzmq", "simplejson", "mysql-connector-python", "python-dotenv", "strict-rfc3339", "pathlib", "requests"],
    entry_points={
        'console_scripts': [
            'cedar-gateway = cedar.Gateway:main',
            'cedar-relay = cedar.Relay:main',
            'cedar-monitor = cedar.Monitor:main',
            ],
        }
    )
