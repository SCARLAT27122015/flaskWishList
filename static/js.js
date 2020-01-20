$(document).ready(function(){
    $('#btnSignUp').click(function() {
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                let data = JSON.parse(response);
                $('#flash').show().text(data.message);
                setTimeout(()=>{$('#flash').fadeOut(1000);},3000);
                $(".form-control").val('');
                $("#inputName").focus();
            },
            error: function(error) {
                console.log(error);
            }
        });
    });    
});