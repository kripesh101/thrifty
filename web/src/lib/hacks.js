export function fakeFocusIOS(mode = "decimal") {
    if (!isIOS()) return;

    // create invisible dummy input to receive the focus first
    const fakeInput = document.createElement("input");
    fakeInput.setAttribute("type", "text");
    fakeInput.setAttribute("inputmode", mode);
    fakeInput.style.position = "absolute";
    fakeInput.style.opacity = "0";
    fakeInput.style.height = "0";
    fakeInput.style.width = "0";
    fakeInput.style.fontSize = "16px"; // disable auto zoom

    document.body.prepend(fakeInput);

    fakeInput.focus();

    setTimeout(() => {
        fakeInput.remove();
    }, 1000);
}

function isIOS() {
    return (
        ["iPad Simulator", "iPhone Simulator", "iPod Simulator", "iPad", "iPhone", "iPod"].includes(
            navigator.platform
        ) ||
        // iPad on iOS 13 detection
        (navigator.userAgent.includes("Mac") && "ontouchend" in document)
    );
}
