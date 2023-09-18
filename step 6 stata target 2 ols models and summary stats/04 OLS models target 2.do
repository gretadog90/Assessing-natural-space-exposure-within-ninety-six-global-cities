/*

TARGET 2 models. Equitable Spatial Distribution

Purpose: Run OLS models of GBA on (m)NDVI within a 15min walk by city and store results

*/

************************************************************************
** create one full data set to run models on
************************************************************************
clear
foreach city in $c40_cities {
	append using "tmp_$cityBounds/`city'_target2.dta"
}

save "tmp_$cityBounds/target2_full.dta", replace

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

gen b_cons_75=.
gen b_ga_75=.
gen se_cons_75=.
gen se_ga_75=.
gen adjr2_75=.
gen rmse_75=.

gen b_cons_90=.
gen b_ga_90=.
gen se_cons_90=.
gen se_ga_90=.
gen adjr2_90=.
gen rmse_90=.

*prediction estimates and CIs for target limits
gen mndvip_70= .
gen mndvip_70_lb= .
gen mndvip_70_ub= .

gen mndvip_70_75= .
gen mndvip_70_lb_75= .
gen mndvip_70_ub_75= .

gen mndvip_70_90= .
gen mndvip_70_lb_90= .
gen mndvip_70_ub_90= .

************************************************************************
** model each city seperately in OLS regression 
************************************************************************	
*city index to subset data
bys city: gen row=_n

*loop through cities
foreach city in "Toronto" {

	*regress ga on ndvi in given city
	reg mndvi gba if city=="`city'"
	
	*store outputs
	replace b_cons=_b[_cons] if city=="`city'"
	replace b_ga=_b[gba] if city=="`city'"
	replace se_cons=_se[_cons] if city=="`city'"
	replace se_ga=_se[gba] if city=="`city'"
	replace adjr2=e(r2) if city=="`city'"
	replace rmse= e(rmse) if city=="`city'"
	
	*predict modified NDVI level at 70% 
	margins, at(gba=0.7) 

	matrix estimates=r(table)
	replace mndvip_70= estimates[1,1] if city=="`city'"
	replace mndvip_70_lb= estimates[5,1] if city=="`city'"
	replace mndvip_70_ub= estimates[6,1] if city=="`city'"
	
	*regress ga on ndvi in given city
	reg mndvi75 gba if city=="`city'"
	
	*store outputs
	replace b_cons_75=_b[_cons] if city=="`city'"
	replace b_ga_75=_b[gba] if city=="`city'"
	replace se_cons_75=_se[_cons] if city=="`city'"
	replace se_ga_75=_se[gba] if city=="`city'"
	replace adjr2_75=e(r2) if city=="`city'"
	replace rmse_75= e(rmse) if city=="`city'"
	
	*predict modified NDVI level at 70% 
	margins, at(gba=0.7) 

	matrix estimates=r(table)
	replace mndvip_70_75= estimates[1,1] if city=="`city'"
	replace mndvip_70_lb_75= estimates[5,1] if city=="`city'"
	replace mndvip_70_ub_75= estimates[6,1] if city=="`city'"
	
	*regress ga on ndvi in given city
	reg mndvi90 gba if city=="`city'"
	
	*store outputs
	replace b_cons_90=_b[_cons] if city=="`city'"
	replace b_ga_90=_b[gba] if city=="`city'"
	replace se_cons_90=_se[_cons] if city=="`city'"
	replace se_ga_90=_se[gba] if city=="`city'"
	replace adjr2_90=e(r2) if city=="`city'"
	replace rmse_90= e(rmse) if city=="`city'"
	
	*predict modified NDVI level at 70% 
	margins, at(gba=0.7) 

	matrix estimates=r(table)
	replace mndvip_70_90= estimates[1,1] if city=="`city'"
	replace mndvip_70_lb_90= estimates[5,1] if city=="`city'"
	replace mndvip_70_ub_90= estimates[6,1] if city=="`city'"
	
	*save summary data set that has model output info
	savesome city b_* se_* adjr2* rmse* mndvip* if city=="`city'" & row==1 using "tmp_$cityBounds/ols_`city'_summary_t2.dta", replace
}


************************************************************************
** append all the model output into one file
************************************************************************
clear
foreach city in $c40_cities {
	append using "tmp_$cityBounds/ols_`city'_summary_t2.dta"
}

assert _N==$cityCount


save "output_$cityBounds/ols_summary_t2.dta", replace
outsheet using "output_$cityBounds/ols_summary_t2.csv", comma replace
