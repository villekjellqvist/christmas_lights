// const { Tabulator } = require("tabulator-tables");
addr = "http://127.0.0.1:5000"

async function getPatterns(table) {
    const res = await fetch(addr + "/getPatterns")
    const patterns = await res.json()

    tableData = []
    for (let i = 0; i < patterns["scripts"].length; i++) {
        tableData.push({
            "scriptnr": i,
            "script": patterns["scripts"][i],
            "running": patterns["running"][i]
        })
    }
    table.setData(tableData)
}

async function setPattern(scriptnr) {
    const response = await fetch(addr + "/setPattern", {
        method: "POST",
        body: JSON.stringify({ "scriptnr": scriptnr }),
        headers: {"Content-Type": "application/json"},
    });
}



var runningFormatter = function (cell, formatterParams) {
    s = "style=\"width:20px;height:20px;\""
    if (cell.getValue()) {
        return `<img src=\"img/run.png\" ${s}></img>`
    }
    return `<img src=\"img/stop.png\" ${s}></img>`
}

async function runningClick(e, cell) {
    send = 0
    if (cell.getValue()) {
        send=-1
    }
    else {
        send = cell.getRow().getData()["scriptnr"]
    }
    await setPattern(send)
    getPatterns(table)
}

var table = new Tabulator("#patterns_Table", {
    layout: "fitColumns",
    height: 200,
    rowheight: 25,
    columns: [
        { title: "#", field: "scriptnr", hozAlign: "center", width: 30 },
        { title: "Script Name", field: "script" },
        {
            title: "", field: "running", hozAlign: "center", frozen: true, formatter: runningFormatter, sorter: "boolean", width: 30, cellClick: runningClick
        }

    ]
})
getPatterns(table)