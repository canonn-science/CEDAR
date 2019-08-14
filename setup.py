from setuptools import setup, find_packages
import re
import glob


VERSIONFILE = "src/eddn/conf/Version.py"
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
    name='eddn',
    version=verstr,
    description='Elite: Dangerous Data Network',
    author='Anthor (EDSM)',
    author_email='contact@edsm.net',
    url='https://github.com/EDSM-NET/EDDN',
    packages=find_packages('src', exclude=["*.tests"]),
    package_dir = {'':'src'},
    data_files=[('eddn/schemas', glob.glob("schemas/*.json"))],
    long_description="""\
      The Elite: Dangerous Data Network allows E:D players to share data. Not affiliated with Frontier Developments.
      """,
    install_requires=["argparse", "bottle", "enum34", "gevent", "jsonschema", "pyzmq", "simplejson", "mysql-connector-python"],
    entry_points={
        'console_scripts': [
            'eddn-gateway = ceddn.Gateway:main',
            'eddn-relay = ceddn.Relay:main',
            'eddn-monitor = ceddn.Monitor:main',
            ],
        }
      )
