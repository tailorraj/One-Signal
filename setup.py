from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in onesignal_integration/__init__.py
from onesignal_integration import __version__ as version

setup(
	name="onesignal_integration",
	version=version,
	description="One signal push notification integration",
	author="Akhilam INC",
	author_email="raaj@akhilaminc.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
