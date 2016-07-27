var check = document.gtElementById("status");
var text = document.gtElementById("task");

function hasClass(element, cls){
	if((element.className).indexOf(cls)>-1){
		return true;
	}
}

check.onclick = strikeThrough(text);

function strikeThrough(text) {
	if (hasClass(check, "Done") != true ){
		$'text'.addClass("Done");
	}else{
		$'text'.removeClass("Done");
	}
}