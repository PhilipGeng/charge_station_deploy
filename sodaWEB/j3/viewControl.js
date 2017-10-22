data = [];
for (var seriesIndex = 0; seriesIndex < 1; seriesIndex++){
    var seriesData = [];
    for (var i = 0; i < 4; i++) {
        seriesData.push([0.59, 0.53, 0.63, 0.49]);
    }
    data.push(echarts.dataTool.prepareBoxplotData(seriesData));
    console.log(data);
}


option1 = {
    title: {
        text: 'Multiple Categories',
        left: 'center',
    },
    tooltip: {
        trigger: 'item',
        axisPointer: {
            type: 'shadow'
        }
    },
    grid: {
        left: '20%',
        top: '20%',
        right: '10%',
        bottom: '15%'
    },
    xAxis: {
        data: ["2", "4", "6", "8"]
    },
    yAxis: {
    },
    dataZoom: [
        {
            type: 'inside',
            start: 0,
            end: 20
        },
        {
            show: true,
            height: 20,
            type: 'slider',
            top: '100%',
            xAxisIndex: [0],
            start: 1,
            end: 20
        }
    ],
    series: [
        {
            name: '',
            type: 'boxplot',
            data: data[0].boxData,
            //tooltip: {formatter: formatter}
        },
        {
            type: 'line',
            label: {
                normal: {
                    show: true,
                    position: 'top'
                }
            },
            data: [0.59, 0.53, 0.63, 0.49]
        }
    ]
};

var getOption = function(data){
    var timeList = data.map(function (item) {
        return item[0];
    });
    var valueList = data.map(function (item) {
        return item[1];
    });
    return {
        visualMap: [{
            show: false,
            type: 'continuous',
            seriesIndex: 0,
            min: 0,
            max: 100
        }],
        tooltip: {
            trigger: 'axis'
        },
        xAxis: [{
            data: timeList
        }],
        yAxis: [{
            
        }],
        series: [{
            type: 'line',
            label: {
                normal: {
                    show: true,
                    position: 'top'
                }
            },
            data: valueList
        }]
    };
}
function formatter(param) {
    return [
        'Experiment ' + param.name + ': ',
        'upper: ' + param.data[0],
        'Q1: ' + param.data[1],
        'median: ' + param.data[2],
        'Q3: ' + param.data[3],
        'lower: ' + param.data[4]
    ].join('<br/>')
}

var renderOneChart = function(id){
    var myChart = echarts.init(document.getElementById(id));
    myChart.setOption(option1);    
}
for(var i=0;i<5;i++){
    $("body").append("<div><div id=\"id_"+i+"\" class=\"keepline\" style=\"width: 80%;height:700px;\"></div><div class=\"phold1 keepline\"></div></div>");
    renderOneChart("id_"+i);
}
