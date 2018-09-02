
$(document).ready(function () {
});


$.get('/rrc/cars_info/', function (data) {
     if (data.code == 200) {
            console.log(data.cars);
            var cars_html = template('rrc-car-tmpl', {'cars': data.cars});
            $('.cars-list').html(cars_html);
            console.log(cars_html)
        }
    });








