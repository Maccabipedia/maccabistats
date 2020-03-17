from setuptools import setup, find_packages
from maccabistats.version import version

setup(
    name='maccabistats',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='Maccabi tel-aviv football team statistics manipulation.',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    python_requires='>=3',
    install_requires=["setuptools>=28.*",
                      "requests>=2.20, <3",
                      "beautifulsoup4>=4.6, <5",
                      "lxml>=4.1, <5",
                      "python-dateutil>=2.7, <5",
                      "matplotlib>=2.2.2, <3",
                      "progressbar>=2.5, <3"]
)
