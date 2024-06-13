
$(document).ready(function(){
    $('#dni').on('input', function(){
        var dni = $(this).val();
        if (dni.length === 8) {
            $.ajax({
                url: '{% url "obtener_nombres_apellidos" %}',
                method: 'POST',
                data: {
                    'dni': dni,
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function(response){
                    $('#nombres').val(response.nombres);
                    $('#apellidos').val(response.apellidos);
                },
                error: function(xhr, errmsg, err){
                    console.log(xhr.status + ": " + xhr.responseText);
                }
            });
        } else {
            $('#nombres').val('');
            $('#apellidos').val('');
        }
    });
});

$(document).ready(function() {
    $('#id_tipo_vehiculo, #id_tiempo').change(function() {
        var tipoVehiculo = $('#id_tipo_vehiculo').val();
        var tiempoSeleccionado = $('#id_tiempo').val();

        $.ajax({
            type: 'POST',
            url: '{% url "obtener_precio" %}',
            data: {
                'tipo_vehiculo': tipoVehiculo,
                'tiempo': tiempoSeleccionado,
                'csrfmiddlewaretoken': '{{ csrf_token }}'
            },
            success: function(response) {
                var precio;
                switch(tiempoSeleccionado) {
                    case 'manana':
                        precio = response.precio.precio_manana;
                        break;
                    case 'tarde':
                        precio = response.precio.precio_tarde;
                        break;
                    case 'noche':
                        precio = response.precio.precio_noche;
                        break;
                    case 'dia_completo':
                        precio = response.precio.precio_dia_completo;
                        break;
                    default:
                        precio = 'Precio no disponible';
                }
                console.log("Precio recibido:", precio);
                $('#id_precio').val(precio);
            },
            error: function(xhr, textStatus, errorThrown) {
                console.log('Error al obtener el precio:', errorThrown);
            }
        });
    });
});

