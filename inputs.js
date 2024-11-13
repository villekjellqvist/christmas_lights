var GPIO = document.getElementById("GPIO")
addr = "http://127.0.0.1:5000"

async function getSettings(){
    const res = await fetch(addr + "/getSettings")
    const settings = await res.json()
    return settings
}

async function updateSettingsClient(){
    settings = await getSettings()
    GPIO.checked = settings["GPIO_enabled"]
}

async function setSettings(newSettings){
    settings = await getSettings()
    for (let key in newSettings){
        settings[key] = newSettings[key]
    }
    const response = await fetch(addr + "/setSettings", {
        method: "POST",
        body: JSON.stringify(settings),
        headers: {"Content-Type": "application/json"},
    });
}

GPIO.onchange = function(){
    setSettings({"GPIO_enabled":GPIO.checked})
}

updateSettingsClient()