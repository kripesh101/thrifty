import {
    Chart,
    BarController,
    BarElement,
    CategoryScale,
    LinearScale,
    Tooltip,
    Legend
} from "chart.js";
import { get } from "svelte/store";
import fetchBackend from "@/lib/backend.js";
import { getWeekArray, getYearNumber, getYearArray } from "@/lib/date.js";
import { loading, type } from "./stores.js";

Chart.register(BarController, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

/** Type Declarations
@typedef {import("chart.js").ChartConfiguration} ChartConfiguration
@typedef {{
    type: "week" | "year",
    timestamp: number | null
}} SummaryChartOptions
*/

/** @type SummaryChartOptions */
const options = {
    type: "week",
    timestamp: null
};
let currentOptions = { ...options };
let title;

let dates = [];

/**
 * Update chart with latest data
 * @param {HTMLCanvasElement} canvas
 */
async function update(canvas) {
    let chart = Chart.getChart(canvas);

    // Whether to remake or not
    const remake = get(type) !== "summary" || !chart;
    type.set("summary");

    // Show loading animation if we are remaking chart or
    // if the chart is changed from weekly to yearly or vice versa
    if (remake || options.type !== currentOptions.type) loading.set(true);
    if (remake && chart) chart.destroy();

    let timestamps;
    if (options.type === "week") {
        timestamps = getWeekArray(options.timestamp);
        data.labels = days;
        dates = timestamps.map((val) => {
            const obj = new Date(val.start);
            return months[obj.getMonth()] + " " + obj.getDate();
        });
        title = "Weekly Summary";
    } else {
        timestamps = getYearArray(options.timestamp);
        data.labels = months;
        title = "Yearly Summary - " + getYearNumber(options.timestamp);
    }

    const params = timestamps.reduce(
        (prev, val) => `${prev}timestamp_start=${val.start}&timestamp_end=${val.end}&`,
        "?"
    );

    data.datasets[0].data = await (await fetchBackend("/expenses/total/ranges/" + params)).json();

    if (remake) chart = new Chart(canvas, config);
    else chart.update();

    currentOptions = { ...options };

    // Hide loading animation
    loading.set(false);

    return chart;
}

function getTitle() {
    return title;
}

const data = {
    labels: [],
    datasets: [
        {
            label: "Expense",
            data: [],
            backgroundColor: ["rgba(255, 132, 99, 0.2)"],
            borderColor: "rgba(255, 99, 132, 1)",
            borderWidth: 1
        }
    ]
};

/** @type ChartConfiguration */
const config = {
    type: "bar",
    data,
    options: {
        responsive: true,
        plugins: {
            tooltip: {
                callbacks: {
                    title: (ctx) => {
                        const index = ctx[0].dataIndex;
                        const label = ctx[0].label;
                        if (currentOptions.type === "week")
                            return `Expense on: ${label}, ${dates[index]}`;
                        else return `Expense in: ${label}`;
                    },
                    label: (ctx) => "Rs. " + ctx.parsed.y
                },
                backgroundColor: (item) => item.tooltip.labelColors[0].borderColor,
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

const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
