foo>=bar.and.bis>bas ! should have spaces around
	bla          ! line started with a tab, should become spaces

a = 2!bar            - missing spaces around '!'
a = 2 !  bar         - too many spaces after '!'

integer*4 :: foo     ! old syntax, should become integer(4)

INTEGER :: a         ! INTEGER -> integer
bar = 0; foo = 1;    ! trailing ;

#endif
endif                ! endif => end if

(\1, 2, 3\)          ! prefer [] syntax
