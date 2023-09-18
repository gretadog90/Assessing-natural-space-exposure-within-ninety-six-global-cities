/*

Purpose:

create appendix B:

city, country, region, ndvi, ga (t1), mndvi, gba, t2, ndvi_t1, ndvi_t2, t1_yes, t2_yes

*/

*get ndvi, ga (t1), mndvi, gba from t1 summary file
use "output/city_summary_t1.dta", clear
assert _N==96

*keep just the variables we need and rename so doesnt match with how labeled in t2 file
keep city ndvi_mean ga_mean mndvi_mean gba_mean
rename (ndvi_mean ga_mean mndvi_mean gba_mean) (t1_mean_ndvi t1_mean_ga t1_mean_mndvi t1_mean_gba)

*merge with t2 summary file to get t2
merge 1:1 city using "output/city_summary_t2.dta", assert(3) nogen

rename (t2 pop_total) (pct_access_gba city_adult_pop)

rename (ndvi_mean ga_mean mndvi_mean gba_mean) (t2_mean_ndvi t2_mean_ga t2_mean_mndvi t2_mean_gba)

keep city* t1_* t2_* pct_*

*merge with c40 list to get country region
merge 1:1 city using "tmp/c40citylist.dta", assert(3) nogen
drop location_name

*merge with regression results to get predicted NDVI (target 1)
merge 1:1 city using "output/ols_summary_t1.dta", assert(3) nogen

rename (rols_40_ndvip rols_30_ndvip ols_40_ndvip ols_30_ndvip) ///
	(p_ndvi_rols_40 p_ndvi_rols_30 p_ndvi_ols_40 p_ndvi_ols_30) 
drop ols* rols*

*merge with regression results to get predicted NDVI (target 2)
merge 1:1 city using "output/ols_summary_t2.dta", assert(3) nogen

rename (ols_70_b rols_70_b) (p_ndvi_ols_70 p_ndvi_rols_70)
drop ols* rols*

*create t1_yes, t2_yes
gen t1_yes_30=(inrange(t1_mean_ga, .3, 1))
gen t1_yes_40=(inrange(t1_mean_ga, .4, 1))
gen t2_yes=(inrange(pct_access_gba, .7, 1))

order city country region

outsheet using "output/appendixB.csv" , comma replace
