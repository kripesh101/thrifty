<script>
    import Textfield from "@smui/textfield";
    import { onMount } from "svelte";

    let date, time;
    onMount(() => {
        const obj = new Date();
        if (dateTime > 0) obj.setTime(dateTime);

        date.getElement().value = obj.toLocaleDateString("en-CA");
        time.getElement().value = obj.toTimeString().substring(0, 5);
        updateTime();
    });

    export let name = "time";
    export let dateTime = 0;
    export let disabled = false;

    function updateTime() {
        const timeObj = time.getElement().valueAsDate;
        const dateObj = date.getElement().valueAsDate;

        // Offset in milliseconds
        const offsetMS = dateObj.getTimezoneOffset() * 60 * 1000;

        dateTime = dateObj.getTime() + timeObj.getTime() + offsetMS;
    }

    function showPicker(e) {
        if (e.target?.nodeName === "INPUT") {
            e.target.showPicker();
        }
    }

    let dateText = "";
    let timeText = "";
</script>

<input type="hidden" {name} bind:value={dateTime} />
<div>
    <Textfield
        bind:value={dateText}
        bind:input={date}
        {disabled}
        on:change={updateTime}
        on:click$preventDefault={showPicker}
        label="Date"
        type="date"
        variant="outlined"
        style="width: 55%;"
        required
    />
    <Textfield
        bind:value={timeText}
        bind:input={time}
        {disabled}
        on:change={updateTime}
        on:click$preventDefault={showPicker}
        label="Time"
        type="time"
        variant="outlined"
        style="width: 43%;"
        required
    />
</div>
