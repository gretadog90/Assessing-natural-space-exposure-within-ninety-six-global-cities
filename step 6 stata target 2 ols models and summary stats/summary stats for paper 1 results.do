
**** PARAGRAPH 1 *******

*get city and regional summary stats on ns metrics
use "output_ucdb/city_summary_t1.dta", clear
merge 1:1 city using "tmp_ucdb/c40citylist.dta", assert(3) nogen

summ ndvi_mean ndvi_min ndvi_max ga_mean ga_min ga_max mndvi_mean mndvi_min ///
	mndvi_max gba_mean gba_min gba_max 

sort ndvi_mean
br if _n==1
br if _n==_N

sort ga_mean
br if _n==1
br if _n==_N

br if ndvi_n==mndvi_n

sort gba_mean
br if _n==1
br if _n==_N

sort mndvi_mean
br if _n==1
br if _n==_N


gen water_pct_change=(mndvi_mean-ndvi_mean)/ndvi_mean
sort water_pct
br city region ndvi_mean mndvi_mean water_pct_change


collapse (mean) ndvi_mean ga_mean ndvi_min ndvi_max ga_min ga_max gba_mean ///
	gba_min gba_max mndvi_mean mndvi_min mndvi_max, by(region)

sort ndvi_mean
gen rank_ndvi=_n

sort mndvi_mean
gen rank_mndvi=_n

sort ga_mean
gen rank_ga=_n

sort gba_mean
gen rank_gBa=_n 


***** PARAGRAPH 2 *****
import delimited using "output ucdb/appendixA.csv" , varnames(1) clear
drop in 1 // these are the variable descriptions
destring t1_mean_ndvi t1_mean_ga t1_mean_gba t1_mean_mndvi pct_access_gba t1_yes_30 t1_yes_40 t2_yes, replace
tab1 t1_yes_30 t1_yes_40 t2_yes
bys region: tab1 t1_yes_30 t1_yes_40 t2_yes
**PARAGRAPH 3*****
use "output ucdb/ols_summary_t1.dta", clear
merge 1:1 city using "tmp/c40citylist.dta", assert(3) nogen
merge 1:1 city using "output ucdb/city_summary_t1.dta", assert(3) nogen

*scatter index =(RMSE/average observed value)*100%
gen si_ols=ols_rmse/ndvi_mean
gen si_rols=rols_rmse/ndvi_mean

gen si_ols_eval="excellent" if inrange(si_ols, 0, .10)
replace si_ols_eval="good" if inrange(si_ols, .10, .25)
replace si_ols_eval="bad" if missing(si_ols_eval)

gen si_rols_eval="excellent" if inrange(si_rols, 0, .10)
replace si_rols_eval="good" if inrange(si_rols, .10, .25)
replace si_rols_eval="bad" if missing(si_rols_eval)

tab1 si_ols_eval si_rols_eval

summ ols_adjr2 ols_rmse ols_30_ndvip  ols_40_ndvip
summ rols_adjr2 rols_rmse rols_30_ndvip rols_40_ndvip


fsum  ols_30_ndvip rols_30_ndvip ols_40_ndvip rols_40_ndvip, uselabel stats(mean min max)

estpost tabstat ols_30_ndvip rols_30_ndvip ols_40_ndvip rols_40_ndvip, by(region) ///
	statistics(mean min max) columns(variables) listwise 
esttab  ., cells("ols_30_ndvip rols_30_ndvip ols_40_ndvip rols_40_ndvip") noobs 

use "output ucdb/ols_summary_t2.dta", clear
merge 1:1 city using "tmp/c40citylist.dta", assert(3) nogen
merge 1:1 city using "output ucdb/city_summary_t2.dta", assert(3) nogen

gen si_ols=ols_rmse/mndvi_mean
gen si_rols=rols_rmse/mndvi_mean

gen si_ols_eval="excellent" if inrange(si_ols, 0, .10)
replace si_ols_eval="good" if inrange(si_ols, .10, .25)
replace si_ols_eval="bad" if missing(si_ols_eval)

gen si_rols_eval="excellent" if inrange(si_rols, 0, .10)
replace si_rols_eval="good" if inrange(si_rols, .10, .25)
replace si_rols_eval="bad" if missing(si_rols_eval)

tab1 si_ols_eval si_rols_eval


summ ols_adjr2 ols_rmse ols_70_b  
summ rols_adjr2 rols_rmse rols_70_b 


