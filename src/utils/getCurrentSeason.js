/*
    Get season whose start and end date are between current date.
    Returns season data if found, null otherwise.
*/

import dateToString from "./dateToString";

export default function getCurrentSeason(seasons) {
    const todayStr = dateToString(new Date());
    const currentSeason =  seasons.filter((season) => {
        return season.season_start_date <= todayStr && season.season_end_date >= todayStr;
    });
    return currentSeason.length > 0 ? currentSeason[0] : null;
}
