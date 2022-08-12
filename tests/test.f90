module merger_parameters!{{{
  use amr_commons
  ! Inter galactic gas density contrast factor
  real(dp)::IG_density_factor = 1.0D-5
  INTEGER :: test

  read(1, NML = merger_params, END = 106)
end module merger_parameters!}}}

module merger_commons

  use merger_parameters
  real(dp), dimension(:,:), allocatable::Vcirc_dat1, Vcirc_dat2

end module merger_commons


print*, &
& foo, &
& bar

do idim = 1, ndim
do ipart = 1, npart
     if (xp(ipart, idim) / scale + skip_loc(idim) < 0.0d0) &
          & xp(ipart, idim) = xp(ipart, idim) + (xbound(idim) - skip_loc(idim)) * scale
          if (xp(ipart, idim) / scale + skip_loc(idim) >= xbound(idim)) &
          & xp(ipart, idim) = xp(ipart, idim) - (xbound(idim) - skip_loc(idim)) * scale
     end do
     enddo

do i = 1, 10
print*, &
i,&
 i*2
if (i == 10) then
print*, 'i is larger than 10!&'
else
print*, 'is not larger than 10'
print*, 'let us confuse endif!'
print*,"very ugly"
write(*,*)"also ugly"
end if
end do


foo>=bar.and.bis>bas ! should have spaces around
	bla          ! line started with a tab, should become spaces

a = 2!bar            - missing spaces around '!'
a = 2 !  bar         - too many spaces after '!'

integer*4 :: foo     ! old syntax, should become integer(4)

INTEGER :: a         ! INTEGER -> integer
! trailing ";"
bar = 0; foo = 1;

#endif
endif                ! => end if

(\1, 2, 3\)          ! prefer [] syntax

comp_iamin  ! Shouldn't be changed

module my_module
contains
     subroutine my_subroutine()
          implicit none
          integer :: var
          var= 1
     end subroutine my_subroutine
end module my_module

use omp_lib

var= 1
var =1
var = 1
var=1

do i=1,10,n

x=1+2*3/5

!       "var=0"  ! First spaces should be squashed into one
! "var=1"  ! Shouldn't be changed
!"var=2"  ! Only first space have to be added

x="1+2"
y='do i = 1, 10, n'
y = "Since x=cos(x) and y=sin(x) "" we have x**2+y**2=1"

x=1d-4+1d-4
x=1e-4+1e-4
x=1D-4+1D-4
x=1E-4+1E-4

if(numerator>0)displacement(i)=displacement(i)-numerator/(det+smallreal*numerator)
if (numerator>0) &
 print*, numerator
end do
! This is fine
!$omp parallel

FUNCTION fSig_metals(lambda, f, species, ion_state)
real(kind=8) :: fSig_metals, lambda, f
integer :: species, ion_state
if (species == 1) then ! Oxygen
fSig_metals = f * getCrosssection_oxygen(lambda, ion_state)
else if (species == 2) then ! Nitrogen
fSig_metals = f * getCrosssection_nitrogen(lambda, ion_state)
else if (species == 3) then ! Carbon
fSig_metals = f * getCrosssection_carbon(lambda, ion_state)
else if (species == 4) then ! Magnesium
fSig_metals = f * getCrosssection_magnesium(lambda, ion_state)
else if (species == 5) then ! Silicon
fSig_metals = f * getCrosssection_silicon(lambda, ion_state)
else if (species == 6) then ! Sulfur
fSig_metals = f * getCrosssection_sulfur(lambda, ion_state)
else if (species == 7) then ! Iron
fSig_metals = f * getCrosssection_iron(lambda, ion_state)
else if (species == 8) then ! Neon
fSig_metals = f * getCrosssection_neon(lambda, ion_state)
end if

END FUNCTION fSig_metals


INTERFACE DVODE_F90
! VODE_F90 is the interface subroutine that is actually invoked
! when the user calls DVODE_F90. It in turn calls subroutine
! DVODE which is the driver that directs all the work.
MODULE PROCEDURE VODE_F90

! GET_STATS can be called to gather integration statistics.
MODULE PROCEDURE GET_STATS

! DVINDY can be called to interpolate the solution and derivative.
MODULE PROCEDURE DVINDY

! RELEASE_ARRAYS can be called to release/deallocate the work arrays.
MODULE PROCEDURE RELEASE_ARRAYS

! SET_IAJA can be called to set sparse matrix descriptor arrays.
MODULE PROCEDURE SET_IAJA

! USERSETS_IAJA can be called to set sparse matrix descriptor arrays.
MODULE PROCEDURE USERSETS_IAJA

! CHECK_STAT can be called to stop if a storage allocation or
! deallocation error occurs.
MODULE PROCEDURE CHECK_STAT

! JACSP can be called to calculate a Jacobian using Doug Salane's
! algoritm
MODULE PROCEDURE JACSP

! DVDSM can be called to calculate sparse pointer arrays needed
! by JACSP
MODULE PROCEDURE DVDSM

END INTERFACE

if (.true.) then
     DO 80 I = IBEG, ILEND
          DO 90 J = IBEG, ILEND
               IF (ICN(J) == 0) GOTO 90
               ICN(JNPOS) = ICN(J)
               A(JNPOS) = A(J)
               JNPOS = JNPOS + 1
90     END DO
80     END DO
end if

FUNCTION SET_NORMAL_OPTS(DENSE_J, BANDED_J, SPARSE_J,                &
     USER_SUPPLIED_JACOBIAN, LOWER_BANDWIDTH, UPPER_BANDWIDTH,          &
     RELERR, ABSERR, ABSERR_VECTOR, NEVENTS) RESULT(OPTS)

! FUNCTION SET_NORMAL_OPTS:
! Jacobian
end function SET_NORMAL_OPTS

! Test reformatting of write and print statements
print*,     "should remove the spaces"
print    *   ,   "what is this?"
print * , some_value

write(*,*) "Hello World"
write       (unit_out,"('\"some string\"', I03.d, 3x)")                foo

! Test continuation line indentation
if (foo.and. & ! With a comment
    foo.and. &
    bar.and.     & ! With a comment
    bar.and.     &
    foobar) print*, "foo&foo&bar&bar"
print*, "should not be indented"
