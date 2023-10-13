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
	
	*didnt run full threshold sensitivity analysis for sensitivity analysis
	destring gba mndvi75 pop, replace
	
	*create a city variable so when appended still clear which city
	gen city="`city'"
	
	*save to temp
	save "tmp_c40/`city'_target2.dta", replace
}

