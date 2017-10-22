
var getpoints = function(name){
    var temp = [];
    var data = eval(name.split("_").slice(1).join("_"));
    for(var i=0;i < data.length;i++){
        for(var t=0;t < data[i].length;t++){
            if(data[i][t]["count"] != 0){
                temp.push(data[i][t]);
            }
        }
    }
    return temp;
}
var appendPOIchild = function(typeid,val){
    var id = "POI_"+typeid;
    $("#id_poi_list").append("<button id=\""+id+"\"  class=\"rightChildBtn\">" + val + "</button>");
    $("#"+id).css("background",optionColor);
}

var appendHeatmap = function(name){
    appendBlocks();
    var points = getpoints(name);
    heatmapOverlay = new BMapLib.HeatmapOverlay({"radius":25,});
    map.addOverlay(heatmapOverlay);
    heatmapOverlay.setDataSet({data:points,max:dataMax[name]});
    var gradient = {
    0.05:'rgba(0,255,0,0)',
    0.3:'rgba(0,255,0,1)',
    // 0.3:'rgba(124,255,0,1)',
    0.7:'rgba(255,255,0,1)',
    // 0.7:'rgba(255,255,0,1)',
    1:'rgba(255,0,0,1)',
    // 1:'rgba(255,0,0,1)',
  };
    heatmapOverlay.setOptions({"gradient":gradient});
}
var appendBlocks = function(){
    for(var i=0;i < datablocks.length;i++){
        var array = [];
        for(var t=0; t < datablocks[i].length;t++){
            array.push(new BMap.Point(datablocks[i][t]["lng"],datablocks[i][t]["lat"]));
        }
        drawline(array);
    }
}
var drawline = function(array){
    var polyline = new BMap.Polyline(array, {strokeColor:"gray", strokeWeight:1, strokeOpacity:1});   //创建折线
	map.addOverlay(polyline);
}

var appendScripts = function(){
	for(var key in dataNames){
		for(var i=0;i < dataNames[key].length;i++){
            if(dataNames[key][i].split("_")[0]!=""){
                addAnOption(key+"_"+dataNames[key][i],key+"_"+dataNames[key][i]);
                appendOneScript("./heatdata/"+key+"/"+dataNames[key][i]+".js");
            }
		}
	}
}
var appendOneScript = function(path){
	var myScript= document.createElement("script");
	myScript.type = "text/javascript";
	myScript.src = path;
	document.body.appendChild(myScript);
}
var addAnOption = function(id, value){
    $('#poiFather').append($('<option>', {
        value: value,
        text: value,
        id: id,
    }));
}
var appendSelect = function(){
    for(var key in dataNames){
		for(var i=0;i < dataNames[key].length;i++){
			append("./heatdata/"+key+"/"+dataNames[key][i]+".js");
		}
	}
}

var appendPoints = function(){
    for(var i=0;i < topblocks.length;i++){
        appendOnePoint(topblocks[i]);
    }
}
var appendOnePoint = function(item){
    var marker = new BMap.Marker(new BMap.Point(item["lng"], item["lat"])); // 创建点
    map.addOverlay(marker);
    // console.log(marker);
    marker["hideID"] = item["id"];
    marker.addEventListener("click",jump);
    // console.log(marker);
}
var jump = function(e){
    window.open("detail.html?id="+e.target["hideID"]);
}

$('#poiFather').change(function () {
    map.clearOverlays();
    appendPoints();
    var optionSelected = $(this).find("option:selected");
    var val = optionSelected.val();
    var id = optionSelected.attr("id");
    appendHeatmap(id);
});
appendScripts();
appendPoints();

// $("#id_clear").on("click", function(){
//     map.clearOverlays();
//     $("#id_poi_list").html("");
// });
// $("#id_add_blocks").on("click", function(){
//     appendBlocks();
// });
// $("#id_add_heatmap").on("click", function(){
//     appendHeatmap();
// });
// var appendOptions = function(list){
//     for(var i=0; i<list.length ;i++){
//         var id = "type_"+i;
//         addAnOption(id,list[i]["type1"]);
//     }
//     $('#poiFather').change(function () {
//         if(optionColor ==""){
//             alert("请先选择颜色");
//             return;
//         }
//         var optionSelected = $(this).find("option:selected");
//         var val = optionSelected.val();
//         var id = optionSelected.attr("id");
//         getTypeData($("#"+id).text());
//         appendPOIchild(id,val);
//         deleteAnOption(id);
//     });
// }

// var deleteAnOption = function(id){
//     $("#"+id).remove();
// }

// var removeEvent = function(id,val){
//     $("#POI_"+id).on("click", function(){ 
//         $("#POI_"+id).remove();
//         addAnOption(id,val);
//     });
// }

// var initColor = function(){
//     for(var i=1;i<=12;i++){
//         var t = i;
//         $("#pal"+i).on("click", function(){
//             var color = this.name.split("_")[1];
//             optionColor = color;
//             $("[name$=select_color]").css("background",color);
//         });
//     }
// }
// $("#id_charge_station").on("click", function(){
//     if(optionColor ==""){
//         alert("请先选择颜色");
//         return;
//     }
//     getChargeStationData();
// });
// getTypeList();
// initColor();





// var appendLine = function(array){
// 	  var flightPath = new google.maps.Polyline({
// 		path: array,
// 		geodesic: true,
// 		strokeColor: 'gray',
// 		strokeOpacity: 1.0,
// 		strokeWeight: 1
// 	  });
// 	  flightPath.setMap(map);
// }

// var appendBlocks = function(){
//     for(var i=0;i < datablocks.length;i++){
// 		appendLine(datablocks[i]);
//     }
// }
// var appendHeatmap = function(dataname){
// 	heatmap = new google.maps.visualization.HeatmapLayer({
// 		data: getpoints(dataname)
// 	  });
// 	heatmap.setMap(map);
// 	heatmap.set('opacity', 1);
// }

// var getpoints = function(dataname){
//     var temp = [];
//     for(var i=0;i < dataname.length;i++){
//         for(var t=0;t < dataname[i].length;t++){
//             if(dataname[i][t]["count"] != 0){
//                 temp.push({"location":new google.maps.LatLng(dataname[i][t]["lat"],dataname[i][t]["lng"]),"weight":dataname[i][t]["count"]});
//             }
//         }
//     }
//     return temp;
// }
