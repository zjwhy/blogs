

var tagList = document.getElementsByTagName(arguments[2]);
var rect = arguments[0].getBoundingClientRect();

var ele;
switch (arguments[1].toLowerCase()) {
case "left":
	ele = getLeftElement()[0];
	break;

case "right":
	ele = getRigthElement()[0];
	break;

case "top":
	ele = getTopElement()[0];
	break;

case "bottom":
	ele = geBottomElement()[0];
	break;

default:
	var arr = new Array();
	arr.push(getLeftElement())
	arr.push(getRigthElement())
	arr.push(getTopElement())
	arr.push(geBottomElement())
	arr.sort(function(a, b) {
		return a[1] - b[1];
	});
	ele = arr[0][0];

}
console.info(ele);
return ele;

function getLeftElement() {
	var min = Number.MAX_SAFE_INTEGER;
	var element;
	for(var i=0;i<tagList.length;i++){
		var item = tagList[i];
		var distance = parseFloat(rect.left) - parseFloat(item.getBoundingClientRect().right);
		if (distance < min && distance > 0) {
			element = item;
			min = distance;
		}
	}
	return [ element, min ];
}

function getRigthElement() {
	var min = Number.MAX_SAFE_INTEGER;
	var element;
	for(var i=0;i<tagList.length;i++){
		var item = tagList[i];
		var distance = parseFloat(item.getBoundingClientRect().left) - parseFloat(rect.right);
		if (distance < min && distance > 0) {
			element = item;
			min = distance;
		}
	}
	return [ element, min ];
}

function getTopElement() {
	var min = Number.MAX_SAFE_INTEGER;
	var element;
	for(var i=0;i<tagList.length;i++){
		var item = tagList[i];
		var distance = parseFloat(rect.top) - parseFloat(item.getBoundingClientRect().bottom);
		if (distance < min && distance > 0) {
			element = item;
			min = distance;
		}
	}
	return [ element, min ];

}

function geBottomElement() {
	var min = Number.MAX_SAFE_INTEGER;
	var element;
	for(var i=0;i<tagList.length;i++){
		var item = tagList[i];
		var distance = parseFloat(item.getBoundingClientRect().top) - parseFloat(rect.bottom);
		if (distance < min && distance > 0) {
			element = item;
			min = distance;
		}
	}
	return [ element, min ];
}