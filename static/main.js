$('.check_button').click(function() {
	console.log("Clicked!");
	$.ajax({
		url: '/check',
		data: {'task_id': $('.task_id').val()},
		type: 'POST',
		success: function(response) {
            console.log(response);
		},
        error: function(error) {
	        console.log(error);
        }
	});
	var c = $(this).attr('class').split(" ");
	if(c[1] == 'notDone'){
		$(this).removeClass('notDone');
		$(this).addClass('Done');
		$(this).text('Uncheck');
		$('#task').addClass('taskdone')
	}
	else if(c[1] == 'Done'){
		$(this).removeClass('Done');
		$(this).addClass('notDone');
		$(this).text('Check');
		$('#task').removeClass('taskdone')
	}
});


$( document ).ready(function() {
    console.log( "ready!" );
    /*
    Assings a class to the check button on the basis of status;
    as the page initializes.
    */
    $('.check_button').each(function() {
    	if("{{ i.is_Done }}" == true){
    		$(this).addClass('Done');
			$(this).text('Uncheck');
			$('#task').addClass('taskdone')

    	}
    	else
    		$(this).addClass('notDone');
			$(this).text('Check');
			$('#task').removeClass('taskdone')
    });
});