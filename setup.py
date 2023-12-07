from setuptools import setup

# architecture
pkg=[
    "bimms",
    "bimms._misc",
    "bimms._misc.calibrations",
    "bimms._misc.configs",
    "bimms.backend",
    "bimms.calibration",
    "bimms.measure",
    "bimms.results",
    "bimms.system",
    "bimms.utils",
]
# non python data to keep
pkg_data={
    "bimms._misc.calibrations": ["*.json"],
    "bimms._misc.configs": ["*.json"],
}

setup(
   name='bimms',
   version='1.1.1',
   description='BIMMS python API',
   long_description = 'file: README.md',
   author='Louis Regnacq - Florian Kolbl - Thomas Couppey',
   packages=pkg,
   package_data=pkg_data,
   include_package_data=True,
   url = 'https://github.com/fkolbl/BIMMS',
   classifiers =[
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent'
     ],
    install_requires=['numpy','andi-py','matplotlib','scipy'], #external packages as dependencies
    python_requires = '>=3.6',
)
