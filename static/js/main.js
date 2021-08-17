window.setTimeout(function() {
    $(".fadeAlert").fadeTo(500, 0).slideUp(500, function(){
        $(this).remove(); 
    });
}, 4000)

$(document).ready(function() {
    $("#btnFetch").click(function() {
      // disable button
    //   $(this).prop("disabled", true);
      // add spinner to button
      $(this).html(
        `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Generating...`
      );
    });
});