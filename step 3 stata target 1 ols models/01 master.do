/*

File to run all other files. 
Set up file paths and globals to be used throughout.

*/

set more off

*choose whether ot run on ucdb or c40 self defined shape files
global cityBounds "ucdb" //"c40"

*file paths
global importDir "/Users/gretam/Documents/data/$cityBounds/"
global projectDir "/Users/gretam/Documents/Stata/"
cd $projectDir

*create globals that will be used throughout
global us_cities `" "New Orleans" "Chicago" "New York City" "Washington DC" "Portland" "Houston" "Seattle" "Miami" "San Francisco" "Phoenix" "Philadelphia" "Austin" "Los Angeles" "Boston" "'
di $us_cities

*global for full set of c40 cities 
global c40_cities `" "Curitiba" "Kuala Lumpur" "Quito" "New Orleans" "Melbourne" "Copenhagen" "Delhi NCT" "Nairobi" "Seoul" "Karachi" "Tel Aviv Yafo" "Jakarta" "Tshwane" "Milan" "Johannesburg" "Hong Kong" "Dhaka North and South" "Chicago" "Berlin" "Lisbon" "New York City" "Barcelona" "Guangzhou" "Dalian" "Zhenjiang" "Rome" "Durban eThekwini" "Auckland" "Stockholm" "Washington DC" "Portland" "Athens" "Nanjing" "Oslo" "Guadalajara" "London" "Sao Paulo" "Beijing" "Bangkok" "Santiago" "Paris" "Hanoi" "Montreal" "Houston" "Heidelberg" "Seattle" "Dar es Salaam" "Shanghai" "Lima" "Chengdu" "Mexico City" "Ekurhuleni" "Qingdao" "Miami" "Istanbul" "Chennai" "Kolkata" "Venice" "Warsaw" "San Francisco" "Phoenix" "Cape Town" "Medellin" "Mumbai" "Accra" "Dubai" "Madrid" "Philadelphia" "Toronto" "Abidjan" "Austin" "Singapore" "Yokohama" "Lagos" "Rio de Janeiro" "Dakar" "Amman" "Bogota" "Hangzhou" "Quezon City" "Los Angeles" "Vancouver" "Shenzhen" "Ho Chi Minh City" "Freetown" "Buenos Aires" "Rotterdam" "Boston" "Salvador" "Amsterdam" "Sydney" "Tokyo" "Fuzhou" "Bengaluru" "Addis Ababa" "Wuhan" "'

*global c40_cities "Fuzhou"
local num : list sizeof global(us_cities)
assert `num' == 14 
*global cityCount=`num'

local num : list sizeof global(c40_cities)
assert `num' == 96
global cityCount=`num'

global ns_metrics ndvi mndvi ga gba

mkdir tmp_$cityBounds
mkdir output_$cityBounds
