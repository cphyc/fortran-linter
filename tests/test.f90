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
