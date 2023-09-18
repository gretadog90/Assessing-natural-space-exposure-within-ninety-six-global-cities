/*

see how our measures align or don't with Kinney paper

*/
 cd "/Users/gretam/Documents/Stata"

import delimited using "raw/greenspace_data_share.csv", varnames(1) clear

* matching 18 manually that didn't match on city name
replace city="Barcelona" if city=="Barcelona [Spain]"
//the names listed don't match the country/region. went with name because closer to our values
replace city="Dhaka North and South" if city=="Dhaka"  //Dhaka
replace city="Delhi NCT" if city=="Delhi [New Delhi]" //Delhi [New Delhi]
replace city="Durban eThekwini" if city=="Durban" //Durban
replace city="Ekurhuleni" if city=="Johannesburg" //Johannesburg

replace city="Medellin" if city=="Medellín" // Medellín
replace city="New York City" if city=="New York" //New York
replace city="Quezon City" if city=="Quezon City [Manila]" //Quezon City [Manila]
replace city="Rotterdam" if city=="Rotterdam [The Hague]" //Rotterdam [The Hague]
replace city="Sao Paulo" if city=="São Paulo" //São Paulo

replace city="Tel Aviv Yafo" if city=="Tel Aviv" //Tel Aviv
replace city="Washington DC" if city=="Washington D.C." //Washington D.C.

///unmatched (6):
//Heidelberg
//San Francisco
//Shenzhen
//Tshwane
//Venice
//Yokohama

merge 1:1 city using "output ucdb/city_summary_t1.dta", keep(2 3)

corr peak_ndvi_2020 ndvi_mean

gen diff=ndvi_mean-peak_ndvi_2020
summ diff




