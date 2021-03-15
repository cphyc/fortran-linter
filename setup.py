import os
from distutils.core import setup

package_name = "fortran_linter"
version = "1.0.5"
README = os.path.join(os.path.dirname(__file__), "Readme.md")
long_description = open(README).read()
setup(
    name=package_name,
    version=version,
    description=("A linter for Fortran files"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cphyc/fortran-syntax",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Fortran",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",  # noqa: E501
        "Topic :: Software Development :: Build Tools",
    ],
    keywords="fortran",
    author="Corentin Cadiou",
    author_email="corentin.cadiou@iap.fr",
    license="GPL",
    package_dir={package_name: package_name},
    packages=[package_name],
    package_data={package_name: ["Readme.md", "LICENSE"]},
    entry_points={
        "console_scripts": [
            "fortran-linter = fortran_linter.cli:main",
        ]
    },
)
