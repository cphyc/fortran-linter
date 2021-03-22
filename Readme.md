# Fortran syntax checker

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

The original file will be backuped into `myfile.f90.orig`. All the safe fixes will be done and stored in the file `myfile.f90`.

For more help, you can type

	fortran-linter -h

## Rules

Currently, the following things are checked:
  * punctuation should be followed by a space, this include `,`, `;` and `)`..
  * The following special characters are surrounded by at least one space: `::`, `=`.
  * A line should not exceed 120 characters (this is somehow already extreme).
  * One should use `use mpi` instead of `include "mpif.h"`. Note that this is not fixed by default as it may break codes where `include "mpif.h"` follows and `implicit none` statement.
  * Spaces are preferred over tabs, trailing whitespaces are cleaned.
  * Warnings are raised if you use `real(8) :: foo`. One should rather use `integer, parameter :: dp = selected_real_kind(15); real(dp) :: foo` or `use iso_fortran_env; real(real64) :: foo`

# TODO list

 * [ ] TESTS
 * [ ] support for other editor(s), e.g. Atom, Vim, …
 * [ ] add more rules (this one will never end)
 * [x] ship on pip
