/*

TARGET 1 Models: Quality Total Cover

Purpose: Run OLS models of GA on NDVI by city and store results

*/

************************************************************************
** create one full data set to run models on
************************************************************************
clear
foreach city in $c40_cities {
	append using "tmp_$cityBounds/`city'_target1.dta"
}

save "tmp_$cityBounds/target1_full.dta", replace

************************************************************************
** create variables to store model output
************************************************************************
*output from model
gen b_cons=.
gen b_ga=.
gen se_cons=.
gen se_ga=.
gen adjr2=.
gen rmse=.

*prediction estimates and CIs for target limits
gen ndvip_30= .
gen ndvip_30_lb= .
gen ndvip_30_ub= .

gen ndvip_40= .
gen ndvip_40_lb= .
gen ndvip_40_ub= .	

************************************************************************
** model each city seperately in OLS regression 
************************************************************************	
*city index to subset data
bys city: gen row=_n

*loop through cities
foreach city in $c40_cities {

	*regress ga on ndvi in given city
	reg ndvi ga if city=="`city'"
	
	*store outputs
	replace b_cons=_b[_cons] if city=="`city'"
	replace b_ga=_b[ga] if city=="`city'"
	replace se_cons=_se[_cons] if city=="`city'"
	replace se_ga=_se[ga] if city=="`city'"
	replace adjr2=e(r2) if city=="`city'"
	replace rmse= e(rmse) if city=="`city'"
	
	*predict NDVI level at 30% and at 40%
	margins, at(ga=0.3) 

	matrix estimates=r(table)
	replace ndvip_30= estimates[1,1] if city=="`city'"
	replace ndvip_30_lb= estimates[5,1] if city=="`city'"
	replace ndvip_30_ub= estimates[6,1] if city=="`city'"

	margins, at(ga=0.4) 

	matrix estimates=r(table)
	replace ndvip_40= estimates[1,1] if city=="`city'"
	replace ndvip_40_lb= estimates[5,1] if city=="`city'"
	replace ndvip_40_ub= estimates[6,1] if city=="`city'"
	
	*save summary data set that has model output info
	savesome city b_* se_* adjr2 rmse ndvip* if city=="`city'" & row==1 using "tmp_$cityBounds/ols_`city'_summary_t1.dta", replace
}


************************************************************************
** append all the model output into one file
************************************************************************
clear

foreach city in $c40_cities {
	append using "tmp_$cityBounds/ols_`city'_summary_t1.dta"
}

assert _N==$cityCount


save "output_$cityBounds/ols_summary_t1.dta", replace
outsheet using "output_$cityBounds/ols_summary_t1.csv", comma replace

************************************************************************
** create threshold values from the model output and store
************************************************************************
gen threshold_reg=b_cons+b_ga
gen threshold_reg75=b_cons+b_ga*.75
gen threshold_reg90=b_cons+b_ga*.90
keep city threshold_reg*

outsheet using "output_$cityBounds/thresholds_t1_$cityBounds.csv", comma replace

save "output_$cityBounds/thresholds_t1_$cityBounds.dta", replace
