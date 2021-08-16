window.setTimeout(function() {
    $(".fadeAlert").fadeTo(500, 0).slideUp(500, function(){
        $(this).remove(); 
    });
}, 4000)