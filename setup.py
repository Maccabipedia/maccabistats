from pathlib import Path

from setuptools import setup, find_packages

here = Path(__file__).resolve()


def extract_version_number() -> str:
    version_file = here.parent / 'src' / 'maccabistats' / 'version.py'
    version_file_text = version_file.read_text()

    return str(version_file_text.split()[-1].strip('"'))


setup(
    name='maccabistats',
    version=extract_version_number(),
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    include_package_data=True,
    license='MIT',
    description='Maccabi tel-aviv football team statistics manipulation.',
    long_description=(here.parent / 'README.md').read_text(encoding="utf-8"),
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    url='https://github.com/Maccabipedia/maccabistats',
    project_urls={'MaccabiPedia': 'https://www.maccabipedia.co.il'},
    install_requires=["setuptools>=28.*",
                      "requests>=2.20, <3",
                      "beautifulsoup4>=4.6, <5",
                      "lxml>=4.1, <5",
                      "python-dateutil>=2.7, <5",
                      "matplotlib>=2.2.2, <3",
                      "progressbar>=2.5, <3"]
)
