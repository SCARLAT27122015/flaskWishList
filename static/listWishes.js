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
        var filePath = $("#imgUpload").attr('src');
        var Private= $('#chkPrivate').is(':checked');
        var Done = $('#chkDone').is(':checked');
        var isPrivate, isDone;

        if (Private) {
            isPrivate = 1;
        }else{
            isPrivate = 0;
        }

        if (Done) {
            isDone = 1;
        }else{
            isDone = 0;
        }

        $.ajax({
            url: '/updateWish',
            data: {
                title: title,
                description: description,
                id: id,
                filePath: filePath,
                isPrivate: isPrivate,
                isDone: isDone       
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

    fileUpload();

});

function fileUpload(){
    $('#fileupload').fileupload({
        url: 'upload',
        dataType: 'json',
        add: function(e, data) {
            data.submit();
        },
        success: function(response, status) {
            var filePath = 'static/Uploads/' + response.filename;
            $('#imgUpload').attr('src', filePath);
            $('#filePath').val(filePath);
            $("#myImage").fadeIn(2000);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

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
            var image = data[0]['FilePath'];

            $('#editTitle').val(data[0]['Title']);
            $('#editDescription').val(data[0]['Description']);
            localStorage.setItem("Id", data[0]['Id']);
            
            if (image != '') {
                $('#imgUpload').attr(
                    {
                        'src': image, 
                        'alt': data[0]['Title']
                    });
            }

            if (data[0]['Private'] == "1") {
                $('#chkPrivate').prop('checked', true);
            }
           
            if (data[0]['Done'] == "1") {
                $('#chkDone').prop('checked', true);
            }
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

