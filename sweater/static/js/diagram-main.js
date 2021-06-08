let canvas1 = document.querySelector("#chart1")
let canvas2 = document.querySelector("#chart2")
let ctx1 = canvas1.getContext('2d')
let ctx2 = canvas2.getContext('2d')


class DatasetPie {
    constructor(options) {
        this.label = options.label
        this.data = options.data
        this.backgroundColor = ['#4b67d7', '#FF1207']
    }
}

class DatasetBar {
    constructor(options) {
        this.label = options.label
        this.data = options.data
        this.backgroundColor = '#'+Math.floor(Math.random()*16777215).toString(16)
    }
}

let chart1 = new Chart(ctx1, {
    type: 'bar',
    data: {
        labels: [],
        datasets: []
    },
    options: {
        responsive: true
    }
})

let chart2 = new Chart(ctx2, {
    type: 'pie',
    data: {
        labels: [],
        datasets: []
    },
    options: {
        responsive: true,
        legend: {
            display: false
        }
    }
})

async function getData(url) {
    const response = await fetch(url)
    return await response.json()
}

function refreshData(ctx, canvas, chart, url) {
    ctx.font = "30px Arial"
    ctx.fillStyle = "blue"
    ctx.textAlign = "center"
    ctx.fillText('Загрузка...', (canvas.width / 2), (canvas.height / 2))

    getData(`/api/stat/${url}`).then(data => {
        chart.data.labels = []
        chart.data.datasets = []
        data['datasets'].forEach(value => {
            if (chart.config._config.type === 'pie') {
                chart.data.datasets.push(new DatasetPie({
                    label: value['dataName'],
                    data: value['data']
                }))
            }
            if (chart.config._config.type === 'bar') {
                chart.data.datasets.push(new DatasetBar({
                    label: value['dataName'],
                    data: value['data']
                }))
            }
        })

        data['dataCols'].forEach(value => {
            chart.data.labels = data['dataCols']
        })

        chart.update()
    })
}

$(document).ready(() => {
    document.querySelector("#chart-refresh1").addEventListener("click", () => {
        refreshData(ctx1, canvas1, chart1, 'count')
    })
    document.querySelector("#chart-refresh2").addEventListener("click", () => {
        refreshData(ctx2, canvas2, chart2, 'nation')
    })
    refreshData(ctx1, canvas1, chart1, 'count')
    refreshData(ctx2, canvas2, chart2, 'nation')
})
