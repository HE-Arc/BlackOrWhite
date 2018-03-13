window.onload = function() {
   var strength = parseInt($('#strength-result').html());
   var defense = parseInt($('#defense-result').html());
   var speed = parseInt($('#speed-result').html());
   var agility = parseInt($('#agility-result').html());
   //Update user attributes
   $(".improve a").click(function(event) {
     //Test quantity of Gold
     if(parseInt($('#gold').html()) < 10){
       $(this).attr('data-target','#myModal');
       event.preventDefault();
     } else {
       var this_ = $(this);
       var improve_url = this_.attr("data-href");
       var id_element = event.target.id;
       $.ajax({
         method: "POST",
         url: improve_url,
         success: function(data) {
           if(id_element === "strength"){
             $('#strength-result').html(parseInt(data));
             $('#gold').html( parseInt($('#gold').html()) - 10)
             $('#strg').attr('title', data + " sur 100");
           }
           else if(id_element === "defense"){
             $('#defense-result').html(parseInt(data));
             $('#gold').html( parseInt($('#gold').html()) - 10)
             $('#defe').attr('title', data + " sur 100");
           }
           else if(id_element === "speed"){
             $('#speed-result').html(parseInt(data));
             $('#gold').html( parseInt($('#gold').html()) - 10)
             $('#spee').attr('title', data + " sur 100");
           }
           else if(id_element === "agility"){
             $('#agility-result').html(parseInt(data));
             $('#gold').html( parseInt($('#gold').html()) - 10)
             $('#agili').attr('title', data + " sur 100");
           }
         },
         error: function(error) {
           console.log("erreur",error);
         }
       });
       event.preventDefault();
      }
     });


     //Ci-dessous le nécessaire pour effectuer de l'ajax en POST
         //https://docs.djangoproject.com/fr/1.11/ref/csrf/
         function getCookie(name) {
           var cookieValue = null;
           if (document.cookie && document.cookie != '') {
               var cookies = document.cookie.split(';');
               for (var i = 0; i < cookies.length; i++) {
                   var cookie = jQuery.trim(cookies[i]);
                   // Does this cookie string begin with the name we want?
                   if (cookie.substring(0, name.length + 1) == (name + '=')) {
                       cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                       break;
                   }
               }
           }
           return cookieValue;
       }
       var csrftoken = getCookie('csrftoken');
       function csrfSafeMethod(method) {
         // these HTTP methods do not require CSRF protection
         return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
       }
       $.ajaxSetup({
           beforeSend: function(xhr, settings) {
               if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                   xhr.setRequestHeader("X-CSRFToken", csrftoken);
               }
           }
       });
  }
