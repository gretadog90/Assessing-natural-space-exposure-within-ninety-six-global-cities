/*

purpose: 1. import c40 list.
		2. remove inactive members
		3. create column to hold smallest geo unit to match with mortality data
*/


*load in c40 city list
import excel using "raw/c40_cities.xlsx", firstrow case(lower) clear

*drop inactive ciites (Moscow)
drop if city=="Moscow"
assert _N==$cityCount

*create column to use in merging that contains the smallest geo unit that mortality is available for
gen str location_name=country

*manual creating field to match GBD data set
safereplace location_name="Addis Ababa" if city=="Addis Ababa", assert(1)
safereplace location_name="Nairobi" if city=="Nairobi", assert(1)
safereplace location_name="Jakarta" if city=="Jakarta", assert(1)
safereplace location_name="Western Cape" if city=="Cape Town", assert(1)
safereplace location_name="KwaZulu-Natal" if city=="Durban eThekwini", assert(1)
safereplace location_name="Gauteng" if city=="Ekurhuleni", assert(1)
safereplace location_name="Gauteng" if city=="Johannesburg", assert(1)
safereplace location_name="Gauteng" if city=="Tshwane", assert(1)
safereplace location_name="Tokyo" if city=="Tokyo", assert(1)
safereplace location_name="Kanagawa" if city=="Yokohama", assert(1)
safereplace location_name="Stockholm" if city=="Stockholm", assert(1)
safereplace location_name="Greater London" if city=="London", assert(1)
safereplace location_name="Parana" if city=="Curitiba", assert(1)
safereplace location_name="Rio de Janeiro" if city=="Rio de Janeiro", assert(1)
safereplace location_name="Bahia" if city=="Salvador", assert(1)
safereplace location_name="Sao Paulo" if city=="Sao Paulo", assert(1)
safereplace location_name="Jalisco" if city=="Guadalajara", assert(1)
safereplace location_name="Mexico City" if city=="Mexico City", assert(1)
safereplace location_name="Texas" if city=="Austin", assert(1)
safereplace location_name="Massachusetts" if city=="Boston", assert(1)
safereplace location_name="Illinois" if city=="Chicago", assert(1)
safereplace location_name="Texas" if city=="Houston", assert(1)
safereplace location_name="California" if city=="Los Angeles", assert(1)
safereplace location_name="Florida" if city=="Miami", assert(1)
safereplace location_name="Louisiana" if city=="New Orleans", assert(1)
safereplace location_name="New York" if city=="New York City", assert(1)
safereplace location_name="Pennsylvania" if city=="Philadelphia", assert(1)
safereplace location_name="Arizona" if city=="Phoenix", assert(1)
safereplace location_name="Oregon" if city=="Portland", assert(1)
safereplace location_name="California" if city=="San Francisco", assert(1)
safereplace location_name="Washington" if city=="Seattle", assert(1)
safereplace location_name="District of Columbia" if city=="Washington DC", assert(1)
safereplace location_name="Sindh" if city=="Karachi", assert(1)
safereplace location_name="United Republic of Tanzania" if city=="Dar es Salaam", assert(1)
safereplace location_name="Cote d'Ivoire" if city=="Abidjan", assert(1)

assert country==location_name if inlist(country, "Ghana", "Nigeria", "Senegal", ///
	"Sierra Leone", "Zimbabwe", "China", "Australia", "Malaysia")
assert country==location_name if inlist(country, "New Zealand", "Philippines", ///
	"Republic of Korea", "Singapore", "Thailand", "Vietnam", "Denmark", ///
	"France", "Germany")
assert country==location_name if inlist(country, "Greece", "Israel", "Italy", "Norway", ///
	"Poland", "Portugal", "Spain", "Turkey", "Argentina")
assert country==location_name if inlist(country, "Chile", "Colombia", "Ecuador", "Peru", "Canada", ///
	"Bangladesh", "India", "United Arab Emirates")

save "tmp_$cityBounds/c40citylist.dta", replace
