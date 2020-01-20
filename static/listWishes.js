$(document).ready(function($) {
    GetWishes();

    $("#deleteButton").click(function(){
        $.ajax({
            url: '/deleteWish',
            data: {
                id: localStorage.getItem('deleteId')
            },
            type: 'POST',
            success: function(res) {
                GetWishes();
                $('#deleteModal').modal('hide');
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
    
    $('#btnUpdate').click(function() {
        var title = $('#editTitle').val();
        var description = $('#editDescription').val();
        var id = localStorage.getItem('Id');

        $.ajax({
            url: '/updateWish',
            data: {
                title: title,
                description: description,
                id: id
            },
            type: 'POST',
            success: function(res) {
                $('#editModal').modal('hide');
                GetWishes();
            },
            error: function(error) {
                console.log(error);
            }
        })
    });

    $('#fileupload').fileupload({
        url: 'upload',
        dataType: 'json',
        add: function(e, data) {
            data.submit();
        },
        success: function(response, status) {
            $('#imgUpload').attr('src','static/Uploads/' + response.filename);
        },
        error: function(error) {
            console.log(error);
        }
    });

});

function Edit(elm) {
    var myId = $(elm).attr('data-id');
    $.ajax({
        url: '/getWishById',
        data: {
            id: myId 
        },
        type: 'POST',
        success: function(res) {
            let data = JSON.parse(res);
            $('#editTitle').val(data[0]['Title']);
            $('#editDescription').val(data[0]['Description']);
            localStorage.setItem("Id", data[0]['Id']);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function GetWishes(){
    $.ajax({
        url: '/getWish',
        type: 'POST',
        success: function(res) {
            var wishObj = JSON.parse(res);
            $('#ulist').empty();
            $('#listTemplate').tmpl(wishObj).appendTo('#ulist');
        },
        error: function(error) {
            console.log(error);
        }
    });
}


function ConfirmDelete(elem) {
    localStorage.setItem('deleteId', $(elem).attr('data-id'));
}