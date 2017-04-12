  $(function () {

    $(".input input").focus(function () {

      $(this).parent(".input").each(function () {
        $("label", this).css({
          "line-height": "18px",
          "font-size": "18px",
          "font-weight": "100",
          "top": "0px"
        })
        $(".spin", this).css({
          "width": "100%"
        })
      });
    }).blur(function () {
      $(".spin").css({
        "width": "0px"
      })
      if ($(this).val() == "") {
        $(this).parent(".input").each(function () {
          $("label", this).css({
            "line-height": "60px",
            "font-size": "24px",
            "font-weight": "300",
            "top": "10px"
          })
        });

      }
    });

    $(".button").click(function (e) {
      var pX = e.pageX,
        pY = e.pageY,
        oX = parseInt($(this).offset().left),
        oY = parseInt($(this).offset().top);

      $(this).append('<span class="click-efect x-' + oX + ' y-' + oY + '" style="margin-left:' + (pX - oX) + 'px;margin-top:' + (pY - oY) + 'px;"></span>')
      $('.x-' + oX + '.y-' + oY + '').animate({
        "width": "500px",
        "height": "500px",
        "top": "-250px",
        "left": "-250px",

      }, 600);
      $("button", this).addClass('active');
    })

    $(".alt-2").click(function () {
      if (!$(this).hasClass('material-button')) {
        $(".shape").css({
          "width": "100%",
          "height": "100%",
          "transform": "rotate(0deg)"
        })

        setTimeout(function () {
          $(".overbox").css({
            "overflow": "initial"
          })
        }, 600)

        $(this).animate({
          "width": "140px",
          "height": "140px"
        }, 500, function () {
          $(".box").removeClass("back");

          $(this).removeClass('active')
        });

        $(".overbox .title").fadeOut(300);
        $(".overbox .input").fadeOut(300);
        $(".overbox .button").fadeOut(300);

        $(".alt-2").addClass('material-buton');
      }

    })

    $(".material-button").click(function () {

      if ($(this).hasClass('material-button')) {
        setTimeout(function () {
          $(".overbox").css({
            "overflow": "hidden"
          })
          $(".box").addClass("back");
        }, 200)
        $(this).addClass('active').animate({
          "width": "700px",
          "height": "700px"
        });

        setTimeout(function () {
          $(".shape").css({
            "width": "50%",
            "height": "50%",
            "transform": "rotate(45deg)"
          })

          $(".overbox .title").fadeIn(300);
          $(".overbox .input").fadeIn(300);
          $(".overbox .button").fadeIn(300);
        }, 700)

        $(this).removeClass('material-button');

      }

      if ($(".alt-2").hasClass('material-buton')) {
        $(".alt-2").removeClass('material-buton');
        $(".alt-2").addClass('material-button');
      }

    });

  });







  $('.button-collapse').sideNav({
    menuWidth: 250, // Default is 300
    edge: 'left', // Choose the horizontal origin
    closeOnClick: false, // Closes side-nav on <a> clicks, useful for Angular/Meteor
    draggable: true // Choose whether you can drag to open on touch screens
  });
  $(document).ready(function () {
    $('.parallax').parallax();
  });


  // Materialize.toast(message, displayLength, className, completeCallback);
  Materialize.toast('', 4000) // 4000 is the duration of the toast


  $(document).ready(function () {
    $('.tooltipped').tooltip({
      delay: 50
    });
  });
    $(document).ready(function(){
    $('.collapsible').collapsible();
  });
    $(document).ready(function(){
    $('.tooltipped').tooltip({delay: 50});
  });
  
  document.addEventListener("DOMContentLoaded", function(){
	$('.preloader-background').delay(1700).fadeOut('slow');
	
	$('.preloader-wrapper')
		.delay(1700)
		.fadeOut();
});
  $(document).ready(function(){
    $('ul.tabs').tabs();
  });
    $(document).ready(function(){
    $('ul.tabs').tabs('select_tab', 'tab_id');
  });
  
    $(document).ready(function(){
    // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
    $('.modal').modal();
  });

    $('.modal').modal({
      dismissible: true, // Modal can be dismissed by clicking outside of the modal
      opacity: .5, // Opacity of modal background
      inDuration: 300, // Transition in duration
      outDuration: 200, // Transition out duration
      startingTop: '4%', // Starting top style attribute
      endingTop: '10%', // Ending top style attribute
      ready: function(modal, trigger) { // Callback for Modal open. Modal and trigger parameters available.
        alert("Ready");
        console.log(modal, trigger);
      },
      complete: function() { alert('Closed'); } // Callback for Modal close
    }
  );