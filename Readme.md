# Fortran linter

This linter works on a line-by-line basis to enforce some rules regarding the format of Fortran files.

The linter does not ship with any grammar and is solely based on regular expressions. This allows
to easily add new rules, but this implies some limitations. For example, continued lines (using `&`)
cannot be parsed or nested parenthesis are a nightmare to fix.

## Installation

There are 2 ways of installing the linter. The recommended one is through pip

	pip install fortran-linter

The other way is to clone this repository and install it from the local copy:

	git clone https://github.com/cphyc/fortran-syntax.git
	pip install .

Please note that depending on your installation, you may have to add `sudo` to the `pip install` line. This is due to the fact that the package is shipped with a script `fortran-linter`. For some installation, the creation of this file may require root access.

## Usage

This tool checks for fortran syntax against a few rules. To print a list of all the warnings for a file, run:

    fortran-linter myfile.f90 --syntax-only

To try to fix the warnings in place, do:

    fortran-linter myfile.f90 -i

The original file will be backup'ed into `myfile.f90.orig`. All the safe fixes will be done and stored in the file `myfile.f90`.

For more help, you can type

	fortran-linter -h

## Rules

Currently, the following things are enforced:
  * Punctuation should be followed by a space, this include `,`, `;` and `)`.
  * Binary operators (`==`, `+`, ...) should be surrounded by spaces
  * The following special characters are surrounded by at least one space: `::`, `=`.
  * A line should not exceed 120 characters (this is somehow already extreme). The maximum line length can be controlled from the CLI.
  * One should use `use mpi` instead of `include "mpif.h"`. Note that this is not fixed by default as it may break codes where `include "mpif.h"` follows and `implicit none` statement.
  * Spaces are preferred over tabs, trailing whitespaces are cleaned.
  * Warnings are raised if you use `real(8) :: foo`. One should rather use `integer, parameter :: dp = selected_real_kind(15); real(dp) :: foo` or `use iso_fortran_env; real(real64) :: foo`

# TODO list

 * [x] ship on pip
 * [ ] add more rules (this one will never end)
