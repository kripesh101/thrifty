import { Chart, DoughnutController, ArcElement, Tooltip, Legend } from "chart.js";
import { get } from "svelte/store";
import fetchBackend from "@/lib/backend.js";
import categories from "@/data/categories.json";
import { loading, type } from "./stores.js";
import { getThisMonth, getThisWeek, getThisYear, getToday } from "../date.js";

Chart.register(DoughnutController, ArcElement, Tooltip, Legend);

const keys = Object.keys(categories);
const labels = keys.map((key) => categories[key].title);
const backgroundColor = keys.map((key) => categories[key].color);

/** Type Declarations
@typedef {import("chart.js").ChartConfiguration} ChartConfiguration
@typedef {{
    type: "overall" | "year" | "month" | "week" | "today"
}} CategoryChartOptions
*/

/** @type CategoryChartOptions */
const options = {
    type: "overall"
};

let title, sum, tooltipPostfix;

/**
 * Update chart with latest data
 * @param {HTMLCanvasElement} canvas
 */
async function update(canvas) {
    let chart = Chart.getChart(canvas);

    // Whether to remake or not
    const remake = get(type) !== "category" || !chart;
    type.set("category");
    title = "Categories";

    if (remake) {
        loading.set(true);
        if (chart) chart.destroy();
    }

    const params = resolveType();

    const fetchedData = await (await fetchBackend("/expenses/total/per_category/" + params)).json();
    data.datasets[0].data = keys.map((category) => fetchedData[category] ?? 0);
    sum = fetchedData.total;

    if (remake) chart = new Chart(canvas, config);
    else chart.update();

    // Hide loading animation
    loading.set(false);

    return chart;
}

function getTitle() {
    return title;
}

function resolveType() {
    const obj = getTypeInfo();

    title += " - " + obj[1];
    tooltipPostfix = obj[2];

    // @ts-ignore
    return obj[0] !== null ? `?timestamp_start=${obj[0].start}&timestamp_end=${obj[0].end}` : "";
}

function getTypeInfo() {
    switch (options.type) {
        case "overall":
            return [null, "Overall", ""];
        case "today":
            return [getToday(), "Today", " today"];
        case "week":
            return [getThisWeek(), "This Week", " this week"];
        case "month":
            return [getThisMonth(), "This Month", " this month"];
        case "year":
            return [getThisYear(), "This Year", " this year"];
    }
}

const data = {
    labels,
    datasets: [
        {
            label: "Expense",
            data: [],
            backgroundColor,
            borderColor: "rgba(0, 0, 0, 0.8)",
            borderWidth: 0.5
        }
    ]
};

/** @type ChartConfiguration */
const config = {
    type: "doughnut",
    data,
    options: {
        responsive: true,
        plugins: {
            tooltip: {
                callbacks: {
                    title: (ctx) => ctx[0].label,
                    label: (ctx) => "Rs. " + ctx.parsed,
                    afterLabel: (ctx) => {
                        const percentage = (ctx.parsed / sum) * 100;
                        return percentage.toFixed(2) + "% of your total expense" + tooltipPostfix;
                    }
                },
                backgroundColor: (item) => item.tooltip.labelColors[0].backgroundColor,
                displayColors: false
            }
        }
    }
};

export default {
    update,
    options,
    getTitle
};
