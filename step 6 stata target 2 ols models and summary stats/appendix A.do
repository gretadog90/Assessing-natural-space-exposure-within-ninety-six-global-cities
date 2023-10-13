/*

Purpose:

create appendix A

*/

*get ndvi, ga (t1), mndvi, gba from t1 summary file
use "output_ucdb/city_summary_t1.dta", clear
assert _N==96

*keep just the variables we need and rename so doesnt match with how labeled in t2 file
keep city ndvi_mean ga_mean mndvi_mean gba_mean
rename (ndvi_mean ga_mean mndvi_mean gba_mean) (t1_mean_ndvi t1_mean_ga t1_mean_mndvi t1_mean_gba)

*merge with t2 summary file to get t2
merge 1:1 city using "output_ucdb/city_summary_t2.dta", assert(3) nogen

rename (t2 pop_total) (pct_access_gba city_adult_pop)

rename (ndvi_mean ga_mean mndvi_mean gba_mean) (t2_mean_ndvi t2_mean_ga t2_mean_mndvi t2_mean_gba)

keep city* t1_* t2_* pct_*

*merge with c40 list to get country region
merge 1:1 city using "tmp_ucdb/c40citylist.dta", assert(3) nogen
drop location_name

*merge with regression results to get predicted NDVI (target 1)
merge 1:1 city using "output_ucdb/ols_summary_t1.dta", assert(3) nogen

rename (ndvip_40 ndvip_30 adjr2 rmse) (t1_p_ndvi_40 t1_p_ndvi_30 t1_adjr2 t1_rmse) 

gen threshold_reg=b_cons+b_ga
gen threshold_reg75=b_cons+b_ga*.75
gen threshold_reg90=b_cons+b_ga*.90

drop ndvip* b* se*

*merge with regression results to get predicted NDVI (target 2)
merge 1:1 city using "output_ucdb/ols_summary_t2.dta", assert(3) nogen

rename (mndvip_70_75 adjr2_75 rmse_75) (t2_p_mndvi_70 t2_adjr2 t2_rmse)
drop mndvip* rmse* adjr2* b* se*

*create t1_yes, t2_yes
gen t1_yes_30=(inrange(t1_mean_ga, .3, 1))
gen t1_yes_40=(inrange(t1_mean_ga, .4, 1))
gen t2_yes=(inrange(pct_access_gba, .7, 1))

order city country region

*simple file
outsheet using "output_ucdb/appendixA.csv", comma replace
save "output_ucdb/appendixA.dta", replace


**TAB 1: paragraph 1, ndvi metrics **
summ t1_mean_ndvi t1_mean_mndvi 

sort t1_mean_ndvi
br if _n==1
br if _n==_N

sort ga_mean
br if _n==1
br if _n==_N

gen ndvi_water_pct_change=((t1_mean_mndvi-t1_mean_ndvi)/t1_mean_ndvi)*100
sort ndvi_water_pct_change
br city region ndvi_mean mndvi_mean water_pct_change

**TAB 2: paragraph 2, landcover metrics **
summ t1_mean_ga t1_mean_gba 
sort t1_mean_ga
br if _n==1
br if _n==_N

gen ga_water_pct_change=((t1_mean_gba-t1_mean_ga)/t1_mean_ga)*100
sort ga_water_pct_change
br city region t1_mean_gba t1_mean_ga ga_water_pct_change

**TAB 3: und target performance **
tab1 t1_yes_30 t1_yes_40 t2_yes 
tab t1_yes_30 t2_yes 

collapse (sum) t1_yes_30 t1_yes_40 t2_yes (count) count=t1_yes_30 , by(region)
foreach v in t1_yes_30 t1_yes_40 t2_yes  {
	gen pct_`v'=`v'/count
}
use "output_ucdb/appendixA.dta", clear


**TAB 4: model 1 results **

summ t1_adjr2 t1_rmse
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


