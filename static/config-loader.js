async function loadControllerEnabled() {
    try {
        const res = await fetch('/config');
        const cfg = await res.json();

        return cfg.controllerEnabled === true;

    } catch (err) {
        console.error(err);
        return false;
    }
}