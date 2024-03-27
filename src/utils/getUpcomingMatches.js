/*
    Get matches from list of matches that happen in the future.
    Returns list of matches if found, otherwise empty list.
*/

import dateToString from "./dateToString";

export default function getUpcomingMatches(matches) {
    const todayStr = dateToString(new Date());
    const upcomingMatches = matches.filter((match) => {
        return match.match_date >= todayStr;
    });
    return upcomingMatches;
}
