/*

Create a summary file where each row is a city and contains
summary stats for all the natural space metrics 

*/

*loop through city files
foreach city in $c40_cities {

	*open the city file
	use "tmp_$cityBounds/`city'_target1.dta", clear

	*generate a bunch of vars to store summary info
	foreach var of varlist $ns_metrics {
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
		*graph export "output/t1_hist_`var'.png", replace
	}
	
	savesome city ndvi_* ga_* gba_* mndvi_* if _n==1 using "tmp_$cityBounds/`city'_summary_t1.dta", replace
}


clear
foreach city in $c40_cities {
	append using "tmp_$cityBounds/`city'_summary_t1.dta"
}

save "output_$cityBounds/city_summary_t1.dta", replace
outsheet using "output_$cityBounds/city_summary_t1.csv", comma replace

*the number of rows should be equal to the city count
assert _N==$cityCount

*metrics that include water should have more pixels than those that do not
assert mndvi_N>=ndvi_N
assert gba_N>=gba_N

/*list city if ga_N==gba_N
Quito
Amman
Addis Ababa */

count if !inrange(ga_mean, 0.1, 0.8)
assert r(N)/_N<.15
count if !inrange(gba_mean, 0.1, 0.9)
assert r(N)/_N<.10

assert ga_min==0
assert gba_min==0
assert ga_max==1
assert gba_max==1

