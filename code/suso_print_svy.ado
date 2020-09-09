program define suso_print_svy

	version 16.0
	syntax , path(string) files(string)

	local opath=`"`c(pwd)'"'
	findfile "suso_print_svy.py"
	local script=`"`r(fn)'"'
	cd `"`path'"'
	foreach f in `files' {
	  frame create `f'
	  frame `f': use "`path'/`f'.dta"
	}
	local f `:word 1 of `files''
	frame change `f'
	python script `"`script'"'
	cd `"`opath'"'
end



// END OF FILE