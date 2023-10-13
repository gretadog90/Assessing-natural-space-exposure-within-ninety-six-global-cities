/*

Create a summary file where each row is a city and contains
summary stats for all the natural space metrics 

*/

*loop through city files
foreach city in $c40_cities {

	*open the city file
	use "tmp_c40/`city'_target2.dta", clear

	*generate a bunch of vars to store summary info
	foreach var of varlist gba mndvi75 pop {
		summ `var', d
		gen `var'_N= r(N) 
		gen `var'_mean= r(mean) 
		gen `var'_sd= r(sd) 
		gen `var'_min= r(min) 
		gen `var'_max= r(max) 
		gen `var'_median= r(p50) 
		
		count if missing(`var')
		gen `var'_missing= r(N) 
		
		*hist `var'
		*graph export "output/t2_hist_`var'.png", replace
	}
	
	*get summary stats for t2
	gen pct_access=pop*gba
	egen pct_access_total=total(pct_access)
	egen pop_total=total(pop)
	gen t2=pct_access_total/pop_total
	
	savesome city gba_* mndvi75_* pop_* t2 if _n==1 using "tmp_c40/`city'_summary_t2.dta", replace
}

clear
foreach city in $c40_cities {
	append using "tmp_$cityBounds/`city'_summary_t2.dta"
}

save "output_$cityBounds/city_summary_t2.dta", replace
outsheet using "output_$cityBounds/city_summary_t2.csv" , comma replace

*the number of rows should be equal to the city count
assert _N==$cityCount
