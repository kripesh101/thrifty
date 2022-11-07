export function getToday() {
    const date = new Date();
    date.setHours(0, 0, 0, 0);
    const start = date.getTime();

    date.setDate(date.getDate() + 1);
    const end = date.getTime();

    return { start, end };
}

export function getThisWeek() {
    const date = new Date();
    date.setHours(0, 0, 0, 0);
    date.setDate(date.getDate() - date.getDay());
    const start = date.getTime();

    date.setDate(date.getDate() + 7);
    const end = date.getTime();

    return { start, end };
}

/**
 * @returns An array with timestamps for start and end of every day in this week
 */
export function getThisWeekArray() {
    const week = [];

    const date = new Date();
    date.setHours(0, 0, 0, 0);
    date.setDate(date.getDate() - date.getDay());

    for (let i = 0; i < 7; i++) {
        const start = date.getTime();
        date.setDate(date.getDate() + 1);
        const end = date.getTime();
        week.push({ start, end });
    }

    return week;
}
