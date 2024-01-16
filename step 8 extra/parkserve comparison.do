/*

purpose: pull in Park Serve data to compare with our Target 2 measures

*/

cd "/Users/gretam/Documents/Stata"

global us_cities `" "New Orleans" "Chicago" "New York City" "Washington DC" "Portland" "Houston" "Seattle" "Miami" "San Francisco" "Phoenix" "Philadelphia" "Austin" "Los Angeles" "Boston" "'

*import parkserve 2023 measures as well for urban area based metric
import excel using "raw/2023 parkserve metrics.xlsx", firstrow clear
save "tmp_ucdb/2023 parkserve metrics.dta", replace

*now import 2020 data
import excel using "raw/Acreage & Park System Highlights - WEB DATA TABLES City Park Facts 2020.xlsx", ///
	sheet("Walkable Park Access") cellrange(A2:B102) firstrow clear
	
*get rid of cities that have no data
drop if PercentofResidentswithinHalf=="n.a."
destring PercentofResidentswithinHalf, gen(parkserve)

*parse city variable to seperate city and state
split City, parse(", ")

*keep just vars we need, edit city names and var names to match on merge
rename City1 city
keep city parkserve

safereplace city="New York City" if city=="New York", assert(1)
safereplace city="Washington DC" if city=="Washington", assert(1)

gen keep=0
foreach city in $us_cities {
	replace keep=1 if city=="`city'"
}

count if keep==1
assert r(N)==14

keep if keep==1
drop keep

*merge to ucdb analysis and pick up t2
merge 1:1 city using "output_ucdb/city_summary_t2.dta", assert(2 3) keep(3) nogen keepusing(t2)
rename t2 t2_ucdb
assert _N==14

*merge to c40 analyis and pick up t2
merge 1:1 city using "output_c40/city_summary_t2.dta", assert(2 3) keep(3) nogen keepusing(t2)
rename t2 t2_c40
assert _N==14

*merge to 2023 parksmart metrics
merge 1:1 city using "tmp_ucdb/2023 parkserve metrics.dta", assert(3) nogen 

*rename for reshape
rename (parkserve t2_ucdb t2_c40 parkserve_city_2023 parkserve_urbanarea_2023) ///
		(value1 value2 value3 value4 value5)

*reshape data so there is three rows per city with estimates for the three variations
reshape long value, i(city) j(metric)
tostring metric, replace
safereplace metric="Parkserve 2020 City" if metric=="1", assert(14)
safereplace metric="Equitable Spatial Distribution (UCDB)" if metric=="2", assert(14)
safereplace metric="Target 2 C40" if metric=="3", assert(14)
safereplace metric="Parkserve 2023 City" if metric=="4", assert(14)
safereplace metric="Parkserve (U.S. Census Urban Area)" if metric=="5", assert(14)

outsheet using "output_ucdb/parkserve_compare.csv", replace
