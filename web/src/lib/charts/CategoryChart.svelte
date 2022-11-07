<script>
    import {
        Chart,
        ArcElement,
        DoughnutController,
        BarController,
        CategoryScale,
        LinearScale,
        Tooltip,
        BarElement,
        Legend
    } from "chart.js";

    import { onDestroy, onMount } from "svelte";
    import { fade } from "svelte/transition";
    import categories from "@/data/categories.json";
    import fetchBackend from "@/lib/backend.js";
    import IconButton from "@smui/icon-button";
    import { getThisWeekArray } from "@/lib/date.js";
    import CircularProgress from "@smui/circular-progress";

    /** @typedef {import("chart.js").ChartConfiguration} ChartConfiguration */

    Chart.register(
        DoughnutController,
        ArcElement,
        Tooltip,
        Legend,
        BarController,
        CategoryScale,
        LinearScale,
        BarElement
    );

    const keys = Object.keys(categories);
    const labels = keys.map((key) => categories[key].title);
    const backgroundColor = keys.map((key) => categories[key].color);

    const chartData = {
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

    const chartDataDaily = {
        labels: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
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
    const dailyChartOptions = {
        type: "bar",
        data: chartDataDaily,
        options: {
            responsive: true,
            plugins: {
                tooltip: {
                    callbacks: {
                        title: (ctx) => "Expense on: " + ctx[0].label
                    },
                    backgroundColor: (item) => item.tooltip.labelColors[0].borderColor,
                    displayColors: false
                }
            }
        }
    };

    let sum;

    /** @type ChartConfiguration */
    const categoryChartOptions = {
        type: "doughnut",
        data: chartData,
        options: {
            responsive: true,
            plugins: {
                tooltip: {
                    callbacks: {
                        title: (ctx) => ctx[0].label,
                        label: (ctx) => "Rs. " + ctx.parsed,
                        afterLabel: (ctx) => {
                            const percentage = (ctx.parsed / sum) * 100;
                            return percentage.toFixed(2) + "% of your total expense";
                        }
                    },
                    backgroundColor: (item) => item.tooltip.labelColors[0].backgroundColor,
                    displayColors: false
                }
            }
        }
    };

    Chart.defaults.font.family = "Montserrat";
    Chart.defaults.font.size = 14;

    let canvas;
    let chart;
    let chartType;
    let loading;

    onMount(() => {
        chartType = "category";
        loading = true;
        reloadChart(true);
    });

    export async function reloadChart(typeChanged = false) {
        if (chartType === "category") {
            if (typeChanged) chart = new Chart(canvas, categoryChartOptions);

            const data = await (await fetchBackend("/expenses/total/per_category/")).json();
            chartData.datasets[0].data = keys.map((category) => data[category] ?? 0);
            sum = data.total;
        } else {
            if (typeChanged) chart = new Chart(canvas, dailyChartOptions);

            const params = getThisWeekArray().reduce(
                (prev, val) => `${prev}timestamp_start=${val.start}&timestamp_end=${val.end}&`,
                "?"
            );
            chartDataDaily.datasets[0].data = await (
                await fetchBackend("/expenses/total/ranges/" + params)
            ).json();
        }
        loading = false;
        chart.update();
    }

    onDestroy(() => {
        chart.destroy?.();
    });

    function swapChart() {
        chart.destroy();
        loading = true;
        chartType = chartType === "category" ? "daily" : "category";
        setTimeout(() => reloadChart(true), 0);
    }
</script>

<div class="chart-header">
    <span class="chart-title">
        {#if chartType === "daily"}
            Weekly Summary
        {:else}
            Category Chart
        {/if}
    </span>
    <IconButton class="material-symbols-rounded" on:click={swapChart}>tune</IconButton>
</div>
<div class="canvas-container" class:wide={chartType === "daily"}>
    <canvas bind:this={canvas} />
    {#if loading}
        <div class="overlay" out:fade>
            <div class="circular-progress" transition:fade>
                <CircularProgress style="height: 32px; width: 32px;" indeterminate />
            </div>
        </div>
    {/if}
</div>

<style>
    .chart-title {
        font-weight: 600;
        font-size: 1.2em;
    }

    .chart-header {
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 500px;
    }

    .canvas-container {
        margin: 0 auto;
        max-height: 425px;
        aspect-ratio: 1;
        position: relative;
    }
    .canvas-container.wide {
        aspect-ratio: 2;
    }

    .overlay {
        z-index: 1;
        position: absolute;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        background-color: #000;
    }
    .circular-progress {
        padding-top: 100px;
    }

    @media (prefers-color-scheme: light) {
        .overlay {
            background-color: #fff;
        }
    }
</style>
