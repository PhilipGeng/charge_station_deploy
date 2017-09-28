var colset1 = ["blue","blue"];
var colset2 = ["red","red"];
var getOption = function(data,boxdata,daytype,colorSet){
    var timeList = data.map(function (item) {
        return item[0];
    });
    var valueList = data.map(function (item) {
        return item[1];
    });
    var boxtemp = [];
    for(var i=0;i < boxdata.length;i++){
        boxtemp.push([valueList[i]-boxdata[i][1]/2,valueList[i],valueList[i],valueList[i],valueList[i]+boxdata[i][1]/2]);
    }
    var seriesData = {};
    seriesData.axisData = ["0", "1", "2", "3"];
    seriesData.boxData = boxtemp;
    seriesData.outliers = [];
    return {
        visualMap: [{
            show: false,
            type: 'continuous',
            seriesIndex: 0,
            min: 0,
            max: 100
        }],
        title:{
            text:daytype,
            left:'center',
            textStyle:{
                color:colorSet[0],
            }
        },
        grid: {
            top: '8%',
            left: '50px'
        },
        tooltip: {
            trigger: 'axis'
        },
        dataZoom: [
        ],
        xAxis: [{
            data: timeList,
            name: '新增的充电桩数目',
            nameLocation: 'middle',
            nameGap: 30,
        }],
        yAxis: [{
            name: '预测的充电桩使用率',
            nameLocation: 'middle',
            nameGap: 30,
        }],
        color: colorSet,
        series: [            
            {
                type: 'line',
                data: []
            },
            {
                type: 'line',
                normal: {
                    show: true,
                    position: 'left'
                },
                data: valueList
            },            {
                name: '',
                type: 'boxplot',
                boxWidth: [10,20],
                data: seriesData.boxData,
            },]
    };
}
var renderOneChart = function(id,data,boxdata,daytype,clr){
    var myChart = echarts.init(document.getElementById(id));
    // console.log(getOption(data));
    myChart.setOption(getOption(data,boxdata,daytype,clr));    
}
var renderTwoChart = function(id, data){
    var myChart = echarts.init(document.getElementById(id));
    myChart.setOption(getOption2(data));    
}
var getOption2 = function(data){
    var timeList = data["workday"].map(function (item) {
        return item[0];
    });
    var valueList = data["workday"].map(function (item) {
        return item[1];
    });
    var valueList2 = data["holiday"].map(function (item) {
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
        title: [{
            left: 'center',
            text: ''
        }],
        tooltip: {
            trigger: 'axis'
        },
        xAxis: [{
            data: timeList
        },{
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
        },
        {
            type: 'line',
            label: {
                normal: {
                    show: true,
                    position: 'top'
                }
            },
            data: valueList2
        }
        ]
    };
}

var ID = getQueryString("id");
$("#id_title").text(blockdatalist[ID]["title"]);
$("#id_description").text(blockdatalist[ID]["description"]);
for(var i=0; i < blockdatalist[ID]["data"].length;i++){
    $("body").append(`
    <div>
        <div class="keepline" style="width: 26%;padding-top: 5px;padding-left: 20px">
            <table border="1">
              <tr>
                 <th>停车场ID</th>
                 <th>`+blockdatalist[ID]["data"][i]["id"]+`</th>
              </tr>
              <tr>
              <th>停车场名称</th>
                <th>`+blockdatalist[ID]["data"][i]["name"]+`</th>
              </tr>
              <tr>
                 <th>现有充电桩数目</th>
                  <th>`+blockdatalist[ID]["data"][i]["charge_num"]+`</th>
              </tr>
              <tr>
                <th>工作日平均占用率</th>
                <th>`+blockdatalist[ID]["data"][i]["avg_rate_weekday"]+`</th>
              </tr>
              <tr>
                <th>周末平均占用率</th>
                <th>`+blockdatalist[ID]["data"][i]["avg_rate_holiday"]+`</th>
            </tr>
            </table>
            <div id="map_a_`+i+`" class="keepline" style="margin-top: 10px;height: 300px;width: 100%;"></div>
        </div>
        <div id="id_work_`+i+`" class="keepline" style="width: 35%;height:500px;"></div>
        <div id="id_holi_`+i+`" class="keepline" style="width: 35%;height:500px;"></div>
        <div class="phold1 keepline"></div>
        </div>
        `);
        renderOneChart("id_work_"+i,blockdatalist[ID]["data"][i]["workday"],blockdatalist[ID]["data"][i]["workday_sd"],"Workday",colset1);
        renderOneChart("id_holi_"+i,blockdatalist[ID]["data"][i]["holiday"],blockdatalist[ID]["data"][i]["holiday_sd"],"Holiday",colset2);
        var map = new BMap.Map("map_a_"+i, {});                        // 创建Map实例
        map.centerAndZoom(new BMap.Point(blockdatalist[ID]["data"][i]["latlng"][1],blockdatalist[ID]["data"][i]["latlng"][0]), 18);     // 初始化地图,设置中心点坐标和地图级别
        map.enableScrollWheelZoom();                        //启用滚轮放大缩小
        var marker = new BMap.Marker(new BMap.Point(blockdatalist[ID]["data"][i]["latlng"][1],blockdatalist[ID]["data"][i]["latlng"][0])); // 创建点
        map.addOverlay(marker);
        map.addTileLayer(new BMap.PanoramaCoverageLayer());
        var stCtrl = new BMap.PanoramaControl(); //构造全景控件
        stCtrl.setOffset(new BMap.Size(20, 10));
        map.addControl(stCtrl);
        var navigationControl = new BMap.NavigationControl({
            // 靠左上角位置
            anchor: BMAP_ANCHOR_BOTTOM_RIGHT,
            // LARGE类型
        });
        map.addControl(navigationControl);
}


// var map = new BMap.Map("map", {});                        // 创建Map实例
// map.centerAndZoom("上海", 13);     // 初始化地图,设置中心点坐标和地图级别
// map.enableScrollWheelZoom();                        //启用滚轮放大缩小
// map.addEventListener("click",function(e){
//    alert(e.point.lng + "," + e.point.lat);
// });



// renderTwoChart("id_comp_"+i,blockdatalist[ID][i]);    
// <div>停车场ID:<div id="id_ID_`+i+`">AAA</div></div>
// <div>现有充电桩数目:<div id="id_number_`+i+`">CCC</div></div>
// <div>现在平均占用率:<div id="id_avg_`+i+`">BBB</div></div>
// <div id="id_comp_`+i+`" class="keepline" style="width: 40%;height:400px;"></div>
// renderOneChart("id_comp_1");
// var appendOneScript = function(){
//     var name = getQueryString("id");
//     var myScript= document.createElement("script");
// 	myScript.type = "text/javascript";
// 	myScript.src = "./topdata/"+name+".js";
// 	document.body.appendChild(myScript);
// }
// appendOneScript();



/*


// Generate data.
data = [];
for (var seriesIndex = 0; seriesIndex < 1; seriesIndex++) {
    var seriesData = [];
    for (var i = 0; i < 17; i++) {
        var cate = [];
        for (var j = 0; j < 100; j++) {
            cate.push(Math.random() * 10);
        }
        seriesData.push(cate);
    }
    console.log(seriesData);
    data.push(echarts.dataTool.prepareBoxplotData(seriesData));
}


option = {
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
        left: '10%',
        top: '20%',
        right: '10%',
        bottom: '15%'
    },
    xAxis: {
        type: 'category',
        data: data[0].axisData,
        boundaryGap: true,
        nameGap: 30,
        axisLabel: {
            formatter: '{value}'
        },
    },
    yAxis: {
        type: 'value',
        name: 'Value',
        min: -10,
        max: 20,
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
            tooltip: {formatter: formatter}
        },
    ]
};

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

*/