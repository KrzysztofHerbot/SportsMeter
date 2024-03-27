/*
    Convert time string from backend to dict containing hours, minutes and seconds.
    Please do not change anything other than timeRegex when using another format.
    Result dict contains numbers if asNumber is true, or strings.
    If regex fails, this returns null.
*/

export default function parseTime(timeStr, asNumber = false) {
    // Format: YYYYmmDD
    const timeRegex = /([0-9]{2})([0-9]{2})([0-9]{2})/m;
    const regexMatch = timeStr.match(timeRegex);
    if (regexMatch !== null && regexMatch.length == 4) {
        return {
            "hours": asNumber ? parseInt(regexMatch[1]) : regexMatch[1],
            "minutes": asNumber ? parseInt(regexMatch[2]) : regexMatch[2],
            "seconds": asNumber ? parseInt(regexMatch[3]) : regexMatch[3]
        };
    }
    return null;
}
