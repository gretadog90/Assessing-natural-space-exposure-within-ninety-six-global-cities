import delimited using "output_c40/appendixB.csv", clear
keep t1_p_ndvi_30 t2_p_mndvi_70 city
rename (t1_p_ndvi_30 t2_p_mndvi_70) (t1_p_ndvi_30_c40 t2_p_mndvi_70_c40)

** pull in c40 data
merge 1:1 city using "output_c40/city_summary_t1.dta"
rename (ndvi_N mndvi_N) (ndvi_n_c40 mndvi_n_c40)

merge 1:1 city using "output_ucdb/city_summary_t1.dta", keepusing(ndvi_N mndvi_N) nogen
rename (ndvi_N mndvi_N) (ndvi_n_ucdb mndvi_n_ucdb)

gen ucdb_bigger_t1=(ndvi_n_ucdb>ndvi_n_c40)
gen ucdb_bigger_t2=(mndvi_n_ucdb>mndvi_n_c40)

merge 1:1 city using "output_ucdb/appendixA.dta", keepusing(t1_p_ndvi_30 t2_p_mndvi_70) nogen
rename (t1_p_ndvi_30 t2_p_mndvi_70) (t1_p_ndvi_30_ucdb t2_p_mndvi_70_ucdb)

 
save "output_ucdb/appendixE.dta", replace
outsheet using "output_ucdb/appendixE.csv" , comma replace
