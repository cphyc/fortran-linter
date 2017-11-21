import os
from distutils.core import setup

package_name = "fortran_linter"
version = '0.1'
README = os.path.join(os.path.dirname(__file__), 'Readme.md')
long_description = open(README).read()
setup(name=package_name,
      version=version,
      description=("Linter for Fortran files"),
      long_description=long_description,
      classifiers=[
          "Programming Language :: Python",
          ("Topic :: Software Development :: Fortran :: Linter"),
      ],
      keywords='fortran',
      author='Corentin Cadiou',
      author_email='corentin.cadiou@iap.fr',
      license='GPL',
      package_dir={package_name: package_name},
      packages=[package_name],
      install_requires=[],
      scripts=['bin/fortran-linter']
)
