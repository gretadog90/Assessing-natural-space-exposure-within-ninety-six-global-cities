keep city p_ndvi_ols_30 p_ndvi_ols_40 p_ndvi_rols_30 p_ndvi_rols_40 p_ndvi_ols_70 p_ndvi_rols_70

rename p_* *_c40

merge 1:1 city using "output/city_summary_t1.dta", keepusing(ndvi_n mndvi_n) assert(3) nogen

rename (ndvi_n mndvi_n) (ndvi_n_c40 mndvi_n_c40)

save "output/appendixE.dta", replace

import delimited using "output ucdb/appendixA.csv" , varnames(1) clear
drop in 1 // these are the variable descriptions
keep city country region p_ndvi_ols_30 p_ndvi_ols_40 p_ndvi_rols_30 p_ndvi_rols_40 p_ndvi_ols_70 p_ndvi_rols_70
destring p_*, replace

merge 1:1 city using "output ucdb/city_summary_t1.dta", keepusing(ndvi_N mndvi_N) assert(3) nogen

rename (ndvi_N mndvi_N) (ndvi_n_ucdb mndvi_n_ucdb)

merge 1:1 city using "output/appendixE.dta", assert(3) nogen

gen ucdb_bigger_t1=(ndvi_n_ucdb>ndvi_n_c40)
gen ucdb_bigger_t2=(mndvi_n_ucdb>mndvi_n_c40)

 

save "output/appendixE.dta", replace

export delimited using "output/appendixE.csv", replace
