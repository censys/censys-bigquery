import setuptools
from setuptools import find_packages

from os import path

current_dir = path.abspath(path.dirname(__file__))

with open(path.join(current_dir, 'README.md')) as f:
    long_desc = f.read()

setuptools.setup(
    name="censys_bigquery_cli",
    version="1.0.0",
    author="art@censys.io",
    author_email="support@censys.io",
    description="A Command line tool for Censys Enterprise Customers that allows BQ access via the command line.",
    long_description=long_desc,
    long_description_content_type='text/markdown',
    install_requires=['censys', 'google-cloud-bigquery', 'google-cloud-core'],
    packages=find_packages(),
    py_modules=['censys_bigquery_cli'],
    python_requires='>=3',
    scripts=['censys_bigquery_cli/censys_bq.py'],
    entry_points={
        'console_scripts': ['censys_bq=censys_bigquery_cli.censys_bq:main'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='censys threat hunting osint ports scan'
)