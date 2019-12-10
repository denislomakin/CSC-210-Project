var draggedSelect = false;
var draggedUnselect = false;
var availability = {};

$(document).mouseup(function(e){
  draggedUnselect = false;
  draggedSelect = false;
});

function clickHandler(e) {
	let jq = $(e.target);
	if (jq.hasClass('not-selected')) {
		jq.removeClass('not-selected');
		jq.addClass('selected');
	} else if (jq.hasClass('selected')) {
		jq.removeClass('selected');
		jq.addClass('not-selected');
	}
}

function moveHandler(e) {
	let jq = $(e.target);
	e.preventDefault()
	if (draggedSelect) {
		jq.addClass('selected');
		jq.removeClass('not-selected');
	} else if (draggedUnselect) {
		jq.addClass('not-selected');
		jq.removeClass('selected');
	}
}

function downHandler(e) {
	let jq = $(e.target);
	e.preventDefault()
	if (jq.hasClass('not-selected')) {
			draggedSelect = true;
	} else if (jq.hasClass('selected')) {
			draggedUnselect = true;
	}
}

function unloadHandler(e) {
	document.querySelectorAll('.select-times .timeRow').forEach(e => {
		e.removeEventListener("click", clickHandler);
		e.removeEventListener("mousemove", moveHandler);
		e.removeEventListener("mousedown", downHandler);
		e.removeEventListener("touch", clickHandler);
		e.removeEventListener("touchmove", moveHandler);
		e.removeEventListener("touchstart", downHandler);
	});
}

window.onload = function() {
	document.querySelectorAll('.select-times .timeRow').forEach(e => {
		e.addEventListener("click", clickHandler);
		e.addEventListener("mousemove", moveHandler);
		e.addEventListener("mousedown", downHandler);
		e.addEventListener("touch", clickHandler);
		e.addEventListener("touchmove", moveHandler);
		e.addEventListener("touchstart", downHandler);
	});
	window.addEventListener('beforeunload', unloadHandler);
	$('#esSubmit').click(function(e) {
	    e.preventDefault();
	    calculateSchedule();
	    $('#availability').val(JSON.stringify(availability));
	    $('#eSchedule').submit();
    })
}

function calculateSchedule() {
	document.querySelectorAll('.select-times .timeRow').forEach( e => {
		availability[e.id] = ($(e).hasClass('selected'));
	});
}


