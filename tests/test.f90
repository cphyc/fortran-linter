module merger_parameters!{{{
  use amr_commons
  ! Inter galactic gas density contrast factor
  real(dp)::IG_density_factor = 1.0D-5

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
