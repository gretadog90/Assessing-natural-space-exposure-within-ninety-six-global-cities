/*

Purpose: Load in city specific .csv files and save as stata files

*/

* loop through each of the 96 cities
foreach city in $c40_cities {

	*import the file that has ndvi, ga, mndvi, gba, and total pop for each pixel
	import delimited using "$importDir/t2_output/`city'.csv", stringcols(_all) clear

	*clean up
	rename v1 index
	order index coords
	
	*destring the natural space and pop vars
	destring $ns_metrics mndvi75 mndvi90 pop, replace
	
	*create a city variable so when appended still clear which city
	gen city="`city'"
	
	*save to temp
	save "tmp_$cityBounds/`city'_target2.dta", replace
}

