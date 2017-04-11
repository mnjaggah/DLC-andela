$(function () {
    $(document).ready(function(){
        $('.nested-replies-form').hide();
    })

    $('.show-hide-form').click(function(){
        var box = $(this).parent().next();
        if ( box.is(":hidden")){

             box.show();
        }
        else{
            box.hide();
        }
    })

})