/*
    Convert Date object to format supported by backend.
    In our case : a string in format YYYYmmDD
    Where:
    YYYY - full year
    mm - month (01-12)
    DD - day (01-31)
*/

export default function dateToString(date) {
    const yearStr = `${date.getFullYear()}`;
    const monthStr = `${date.getMonth()}`.padStart(2, "0");
    const dayStr = `${date.getDay()}`.padStart(2, "0");
    return `${yearStr}${monthStr}${dayStr}`;
}
