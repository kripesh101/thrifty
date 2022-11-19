function getDateObj(timestamp) {
    return new Date(timestamp ?? Date.now());
}

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

export function getThisMonth() {
    const date = new Date();
    date.setHours(0, 0, 0, 0);
    date.setDate(1);
    const start = date.getTime();

    date.setMonth(date.getMonth() + 1);
    const end = date.getTime();

    return { start, end };
}

export function getThisYear() {
    const date = new Date();
    date.setHours(0, 0, 0, 0);
    date.setMonth(0, 1);
    const start = date.getTime();

    date.setFullYear(date.getFullYear() + 1);
    const end = date.getTime();

    return { start, end };
}

export function getYearArray(timestamp) {
    const year = [];

    const date = getDateObj(timestamp);
    date.setHours(0, 0, 0, 0);
    date.setMonth(0, 1);

    for (let i = 0; i < 12; i++) {
        const start = date.getTime();
        date.setMonth(date.getMonth() + 1);
        const end = date.getTime();
        year.push({ start, end });
    }

    return year;
}

export function getWeekArray(timestamp) {
    const week = [];

    const date = getDateObj(timestamp);
    date.setHours(0, 0, 0, 0);

    // Set date to start of week
    date.setDate(date.getDate() - date.getDay());

    for (let i = 0; i < 7; i++) {
        const start = date.getTime();
        date.setDate(date.getDate() + 1);
        const end = date.getTime();
        week.push({ start, end });
    }

    return week;
}

export function getYearNumber(timestamp) {
    const date = getDateObj(timestamp);
    return date.getFullYear();
}
