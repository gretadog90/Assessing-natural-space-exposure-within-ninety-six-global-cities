/*

compare shapefile results

*/


import delimited using "output/appendixE.csv", varnames(1) clear
keep ucdb_bigger_t1 ucdb_bigger_t2 city country region

merge 1:1 city using "output/city_summary_t1.dta", assert(3) nogen
keep ucdb_bigger_t1 ucdb_bigger_t2 city country region *_mean

rename *_mean *_c40

merge 1:1 city using "output ucdb/city_summary_t1.dta", assert(3) nogen keepusing(ndvi_mean ga_mean gba_mean mndvi_mean)
rename *_mean *_ucdb

outsheet using "output/shapefile_compare.csv", comma replace
