/*

Purpose: Load in city specific .csv files and save as stata files

*/

* loop through each of the 96 cities
foreach city in $c40_cities {

	*import the file that has ndvi, ga, mndvi, gba for each pixel
	import delimited using "$importDir/`city'.csv", stringcols(_all) clear
	
	*clean up
	rename v1 index
	order index coords
	
	*destring the natural space vars
	destring $ns_metrics, replace
	
	*create a city variable so when appended still clear which city
	gen city="`city'"
	
	*save to temp
	save "tmp/`city'_target1.dta", replace
}

