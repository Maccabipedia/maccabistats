from setuptools import setup, find_packages
import os


def extract_version_number() -> str:
    version_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'maccabistats', 'version.py')
    with open(version_file_path, 'rb') as version_file:
        return str(version_file.read().split()[-1].strip(b'"'))


setup(
    name='maccabistats',
    version=extract_version_number(),
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
