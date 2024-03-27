/*
    Convert date string from backend to dict containing year, month and day.
    Please do not change anything other than dateRegex when using another format.
    Result dict contains numbers if asNumber is true, or strings.
    If regex fails, this returns null.
*/

export default function parseDate(dateStr, asNumber = false) {
    // Format: YYYYmmDD
    const dateRegex = /([1-9][0-9]{3})([0-9]{2})([0-9]{2})/m;
    const regexMatch = dateStr.match(dateRegex);
    if (regexMatch !== null && regexMatch.length == 4) {
        return {
            "year": asNumber ? parseInt(regexMatch[1]) : regexMatch[1],
            "month": asNumber ? parseInt(regexMatch[2]) : regexMatch[2],
            "day": asNumber ? parseInt(regexMatch[3]) : regexMatch[3]
        };
    }
    return null;
}
