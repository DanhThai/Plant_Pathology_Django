$(document).ready(function() { 
    console.log(user);
    if ($('#img-card').attr('src') == ""){    
      switchCard(true);
    }
    else{
      switchCard(false); 
    }


    $('#image-upload').change(function () {
      var value = $('#image-upload').val().split('\\').pop();
      $('#image-text').text(value);
      $('#image-text').css({'color':'black', 'font-style':'normal'})
      loadImage($("#image-upload").prop("files")[0]);
      switchCard(false);
    });

});

setImage = function (){
    var value = $('#image-upload').val().split('\\').pop();
    $('#image-text').text(value);
    $('#image-text').css({'color':'black', 'font-style':'normal'})
    loadImage($("#image-upload").prop("files")[0]);
    switchCard(false);
}
loadImage = function(file) {
    var reader = new FileReader();
    reader.onload = function(event) {
      $('#img-card').attr('src', event.target.result);
    }
    reader.readAsDataURL(file); 
}

switchCard = function(isIntroduce) {
  if (isIntroduce === true)
  {
    var result = $('.container__result')
    result.prepend('<div class="introduce"> \
                <p>Bạn hãy upload ảnh lá cây trồng</p> \
                <p>Các cây trồng bao gồm: cà chua, táo, ngô, nho</p></div>');
    console.log(result);
    $('.content').hide();
  }
  else{
    $(".introduce").remove();
    $('.content').show();
  }
}
