$(document).ready(function () {
    $('add_to_cart').on('click', function (e) {
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        data = {
            food_id: food_id,
        }
        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            sucess: function (response) {
                console.log(response)
            }
        })
    })
    
})

// need to add the long and latitude. This