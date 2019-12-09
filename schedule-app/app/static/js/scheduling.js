var draggedSelect = false;
var draggedUnselect = false;
var availability = {};

$(document).mouseup(function(e){
  draggedUnselect = false;
  draggedSelect = false;
});

function clickHandler(e) {
	if (e.target.className === "not-selected") {
		e.target.className = "selected";
	} else if (e.target.className === "selected") {
		e.target.className = "not-selected";
	}
}

function moveHandler(e) {
	e.preventDefault()
	if (draggedSelect) {
		e.target.className = "selected";
	} else if (draggedUnselect) {
		e.target.className = "not-selected";
	}
}

function downHandler(e) {
	e.preventDefault()
	if (e.target.className === "not-selected") {
			draggedSelect = true;
	} else if (e.target.className === "selected") {
			draggedUnselect = true;
	}
}

function unloadHandler(e) {
	document.querySelectorAll('#select-times td').forEach(e => {
		if (e.className === "not-selected" || e.className === "selected") {
			e.removeEventListener("click", clickHandler);
			e.removeEventListener("mousemove", moveHandler);
			e.removeEventListener("mousedown", downHandler);
			e.removeEventListener("touch", clickHandler);
			e.removeEventListener("touchmove", moveHandler);
			e.removeEventListener("touchstart", downHandler);
		} 
	});
}

window.onload = function() {
	document.querySelectorAll('#select-times td').forEach(e => {
		if (e.className === "not-selected" || e.className === "selected") {
			e.addEventListener("click", clickHandler);
			e.addEventListener("mousemove", moveHandler);
			e.addEventListener("mousedown", downHandler);
			e.addEventListener("touch", clickHandler);
			e.addEventListener("touchmove", moveHandler);
			e.addEventListener("touchstart", downHandler);
		} 
	})
	window.addEventListener('beforeunload', unloadHandler);
	$('#esSubmit').click(function(e) {
	    e.preventDefault();
	    calculateSchedule();
	    $('#availability').val(JSON.stringify(availability));
	    $('#eSchedule').submit();
    })
}

function calculateSchedule() {
	document.querySelectorAll('#select-times td').forEach( e => {
	    if (e.className === "not-selected" || e.className === "selected")
		    availability[e.id] = (e.className == "selected");
	});
}


