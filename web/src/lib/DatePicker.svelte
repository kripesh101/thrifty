<script>
    import Textfield from "@smui/textfield";
    import { onMount } from "svelte";

    let date, time;
    onMount(() => {
        const obj = new Date();
        if (dateTime !== null) obj.setTime(dateTime);

        date.getElement().value = obj.toLocaleDateString("en-CA");
        if (!dateOnly) time.getElement().value = obj.toTimeString().substring(0, 5);
        updateTime();
    });

    export let name = "time";
    export let dateTime = null;
    export let disabled = false;
    export let readonly = false;
    export let dateOnly = false;
    export let fullWidth = true;

    function updateTime() {
        const dateObj = date.getElement().valueAsDate;
        dateTime = dateObj.getTime();
        const offsetMS = dateObj.getTimezoneOffset() * 60 * 1000;
        dateTime += offsetMS;

        if (!dateOnly) {
            const timeObj = time.getElement().valueAsDate;

            // Offset in milliseconds
            dateTime += timeObj.getTime();
        }
    }

    function showPicker(e) {
        if (e.target?.nodeName === "INPUT") {
            e.target.showPicker();
        }
    }

    let dateText = "";
    let timeText = "";

    $: input$readonly = readonly ? true : null;
</script>

<input type="hidden" {name} bind:value={dateTime} />
<div>
    <Textfield
        bind:value={dateText}
        bind:input={date}
        {disabled}
        {input$readonly}
        on:change={updateTime}
        on:click$preventDefault={showPicker}
        label="Date"
        type="date"
        variant="outlined"
        style={fullWidth ? "width: 55%;" : ""}
        required
    />
    {#if !dateOnly}
        <Textfield
            bind:value={timeText}
            bind:input={time}
            {disabled}
            {input$readonly}
            on:change={updateTime}
            on:click$preventDefault={showPicker}
            label="Time"
            type="time"
            variant="outlined"
            style={fullWidth ? "width: 43%;" : ""}
            required
        />
    {/if}
    <!-- 
        <p>{dateTime}</p>
        <p>{new Date(dateTime)}</p>
    -->
</div>
