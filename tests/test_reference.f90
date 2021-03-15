foo >= bar .and. bis > bas ! should have spaces around
  bla          ! line started with a tab, should become spaces

a = 2 ! bar            - missing spaces around '!'
a = 2 ! bar         - too many spaces after '!'

integer(4) :: foo     ! old syntax, should become integer(4)

integer :: a         ! INTEGER -> integer
! trailing ";"
bar = 0; foo = 1

#endif
end if                ! => end if

[1, 2, 3]          ! prefer [] syntax

comp_iamin  ! Shouldn't be changed
