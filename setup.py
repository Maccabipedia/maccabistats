from setuptools import setup, find_packages
import maccabistats

setup(
    name='maccabistats',
    version=maccabistats.version,
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='Maccabi football team statistics manipulation.',
    long_description=open('README.md').read(),
    install_requires=["setuptools==28.8.0",
                      "requests==2.18.4",
                      "beautifulsoup4==4.6.0"]
)
