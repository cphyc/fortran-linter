# Fortran syntax checker

This tool checks for fortran syntax against a few rules. To print a list of all the warnings for a file, run:

    python cleanup.py myfile.f90 --syntax-only

To try to fix the warnings in place, do:

    python cleanup.py myfile.f90 -i

The original file will be backuped into `myfile.f90.orig`. All the safe fixes will be done and stored in the file `myfile.f90`.

Currently, the following things are checked:
  * Ponctuation should be followed by a space, this include `,`, `;` and `)`..
  * The following special characters are surrounded by at least one space: `::`, `=`.
  * A line should not exceed 120 characters (this is somehow already extreme).
  * One should use `use mpi` instead of `include "mpif.h"`. Note that this is not fixed by default as it may break codes where `include "mpif.h"` follows and `implicit none` statement.
  * Spaces are preferred over tabs, trailing whitespaces are cleaned.
  * Warnings are raised if you use `real(8) :: foo` statement as it is better to use `integer, parameter :: dp=selected_real_kind(15); real(dp) :: foo` instead or `use iso_fortran_env, only : real32=>sp, real64=>dp; real(sp)`
