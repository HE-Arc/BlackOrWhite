window.onload = function() {
   //Update user attributes
   $("a").click(function(event) {
      var this_ = $(this);
      //Récupération valeur(url) de l'attribut data-ref du lien cliqué
      var buy_url = this_.attr("data-href");
      //On passe l'url du lien à l'attribut data-ref du modal
      if(parseInt(this_.attr("data-gold")) >= parseInt(this_.attr("data-price"))){
        //Si on a assez d'or on affiche le message correspondant
        $("#myModalLabel").html("Confirmez votre achat!!");
        $('.message').html("Vous êtes sur le point d'effectuer un achat sur boutique bow. Confirmez vous votre achat?");
        if(parseInt(this_.attr("data-cat")) === 1) {
          $('.text-center').html("<img src='/static/assets/images/weapons/" + this_.attr('data-image') +"' alt='"+this_.attr('data-image')+"' style='width: 100px; height: 100px;'>");
        }
        if(parseInt(this_.attr("data-cat")) === 2) {
          $('.text-center').html("<img src='/static/assets/images/shields/" + this_.attr('data-image') +"' alt='"+this_.attr('data-image')+"' style='width: 100px; height: 100px;'>");
        }
        document.getElementById("buy-link").style.display = "inline";
        $('#myModal').show().attr('data-href', buy_url);
      } else if(parseInt(this_.attr("data-gold")) < parseInt(this_.attr("data-price"))){
        //Sinon on change le message du modal
        $("#myModalLabel").html("Attention!!");
        $('.message').html("Désolé! Vous ne disposez pas d'assez d'or pour effectuer cette opération.");
        document.getElementById("buy-link").style.display = "none";
        $('.text-center').html("");
      }
  });

  //Gestion de la validation (envoie de la requête ajax)
  $("#buy-link").click(function(event) {
    //On récupère l'url
    var buy_url = $('#myModal').attr('data-href');
    //Fermeture du modal après validation
    $("#myModal").modal("hide");
    $.ajax({
      method: "POST",
      url: buy_url,
      success: function(data) {
        if(data === "interdit")
          alert("Vous possédez déjà cet item");
        console.log(data);
      },
      error: function(error) {
        console.log("erreur",error);
      }
   });
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
