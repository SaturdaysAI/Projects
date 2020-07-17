/*
 *@autor: Cristian Yunga
 */

ini = function(){
    
    var oTable;
    var map;
    var ui;
    
    getMapa();
    
    /**** FUNCIONES *****/
    
    function getMapa() {
        // Initialize thelatform object:
        var platform = new H.service.Platform({
            'app_id': 'dWLSVkANV5FN71UWWvGI',
            'app_code': 'i_8mtoms477HrLSfkUHr4Q',
            'useCIT': true,
            'useHTTPS': true
        });

        // Obtain the default map types from the platform object
        var maptypes = platform.createDefaultLayers();

        // Instantiate (and display) a map object:
        map = new H.Map(
            document.getElementById('mapContainer'),
            maptypes.normal.map,
            {
                zoom: 10,
                center: {lat: -0.165308, lng: -78.471064}
            });
        // Create the default UI:
        ui = H.ui.UI.createDefault(map, maptypes, 'es-ES');
        // MapEvents enables the event system
        // Behavior implements default interactions for pan/zoom (also on mobile touch environments)
        var behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(map));
    }
    
    function clearMaps(){
        var arr_obj = map.getObjects();
        console.log(arr_obj);
        try {
            map.removeObjects(map.getObjects ());
            map.setCenter({lat:-0.165308,lng:-78.471064});
        } catch(err){
            console.log(err.message);
        }
    }
    
    function getTabla() {
        oTable = $('#gridResultados').dataTable({
            "bJQueryUI" : true,
            "bPaginate": true,
            "bAutoWidth": false,
            "bSortable": false,
            "bSort": true,
            'bInfo': true,
            "sPaginationType" : "full_numbers",
            "oLanguage": {
                "sLengthMenu": "Mostrar _MENU_ registros por pagina",
                "sZeroRecords": "No se encotraron registros",
                "sInfo": "Esta viendo _START_ de _END_ de un total de _TOTAL_ registros",
                "sInfoEmtpy": "Esta viendo 0 de 0 de un total de 0 registros",
                "sSearch": "Buscar",
                "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
                "oPaginate": {
                    "sFirst":    "Inicio",
                    "sPrevious": "Anterior",
                    "sNext":     "Siguiente",
                    "sLast":     "Fin"
                }
            }
        });
        $("#tablaResultados").fadeIn(1000);
    }
    
    function setPointOnMap(group, coordinate, html) {
        var marker = new H.map.Marker(coordinate);
        marker.setData(html);
        group.addObject(marker);
    }
    
    /****** EVENTOS  *********/
    
    $(".cambio_mayuscula").die("keyup");
    $(".cambio_mayuscula").live("keyup",function cambio_mayuscula(){
        txt = $(this).val();
        txt = txt.substr(0,txt.length).toUpperCase();
        $(this).val(txt);
    });
    
    $('.cantidad').live("keyup",function(event){
        ruc_shipper=$(this).val();
        texto="";
        for(i=0;i<ruc_shipper.length;i++){
            if(!((/[0-9]/.test(ruc_shipper[i])))){
            // nada
            }else{
                texto=texto+ruc_shipper[i];
            }
        }
        $(this).val(texto);
    });

    $('.cantidad').live("change",function(event){
        ruc_shipper=$(this).val();
        texto="";
        for(i=0;i<ruc_shipper.length;i++){
            if(!((/[0-9]/.test(ruc_shipper[i])))){
            // nada
            }else{
                texto=texto+ruc_shipper[i];
            }
        }
        $(this).val(texto);
    });
    
    $('.nombre').live("keyup",function(event){
        ruc_shipper=$(this).val();
        texto="";
        for(i=0;i<ruc_shipper.length;i++){
            if(!((/[A-Za-z ]/.test(ruc_shipper[i])))){
            // nada
            }else{
                texto=texto+ruc_shipper[i];
            }
        }
        $(this).val(texto);
    });

    $('.nombre').live("change",function(event){
        ruc_shipper=$(this).val();
        texto="";
        for(i=0;i<ruc_shipper.length;i++){
            if(!((/[A-Za-z ]/.test(ruc_shipper[i])))){
            // nada
            }else{
                texto=texto+ruc_shipper[i];
            }
        }
        $(this).val(texto);
    });

    $("#nuevo").die("click");
    $("#nuevo").live("click", function() {
        //$("#cedulaUsuario").val("");
        $("#nombreUsuario").val("");
        $("#menu").attr("checked",false);
        $("#vegetariano").attr("checked",false);
        $("#menestra").attr("checked",false);
        $("#comida_rapida").attr("checked",false);
        $("#pollo").attr("checked",false);
        $("#carne").attr("checked",false);
        $("#lacteos").attr("checked",false);
        //$("#cedulaUsuario").focus();
        $("#nombreUsuario").focus();
        $("#tablaResultados").html("");
        $("#tablaResultados").fadeOut(1000);
        clearMaps();
    });
    
    $("#predecir").die("click");
    $("#predecir").live("click", function() {
        //$("#tablaResultados").fadeOut(700);
        clearMaps();
        //id_cliente: "", 
        var tipo = {nombre: "", genero: 0, ambiente: 0, menu: 0, vegetariana: 0, pollo: 0, carne: 0, comida_rapida: 0, lacteos: 0, menestra: 0};
        /*var cedula = $("#cedulaUsuario").val();
        if(!cedula.trim()) {
            alert("Ingrese una Cedula Valida");
            return;
        }
        tipo.id_cliente = cedula;*/
        var nombre = $("#nombreUsuario").val();
        if(!nombre.trim()) {
            alert("El campo Nombre no puede ir Vacio");
            return;
        }
        tipo.nombre = nombre;
        var genero = $("#generoH:checked").val();
        if(!genero) {
            alert("Seleccione su Genero");
            return;
        }
        tipo.genero = parseInt(genero);
        var ambiente = $("#ambienteA:checked").val();
        if(!ambiente) {
            alert("Seleccione el Ambiente");
            return;
        }
        tipo.ambiente = parseInt(ambiente);
        $("#tablaResultados").fadeIn(500);
        $("#predecir").attr("disabled",true);
        $("#nuevo").attr("disabled",true);
        $("#tablaResultados").html("<div style='width:100%;'><img src='images/load_wait.gif' style='height:25px;width:75px;margin-left: 100px;' /></div>");
        
        var menu = $("#menu").is(":checked")?1:0;
        var vegetariana = $("#vegetariana").is(":checked")?1:0;
        var pollo = $("#pollo").is(":checked")?1:0;
        var carne = $("#carne").is(":checked")?1:0;
        var comida_rapida = $("#comida_rapida").is(":checked")?1:0;
        var lacteos = $("#lacteos").is(":checked")?1:0;
        var menestra = $("#menestra").is(":checked")?1:0;
        
        tipo.menu = parseInt(menu);
        tipo.vegetariana = parseInt(vegetariana);
        tipo.pollo = parseInt(pollo);
        tipo.carne = parseInt(carne);
        tipo.comida_rapida = parseInt(comida_rapida);
        tipo.lacteos = parseInt(lacteos);
        tipo.menestra = parseInt(menestra);
        /*$('.checkSeleccion').each(function(){
            tipo[$(this).attr("id")] = $(this).is(":checked")?1:0;
        });*/
        console.log(tipo);
        $.post("controllers/prediccionController.php",{
            accion: "getPrediction", datos: tipo
        },function(data){
            $("#predecir").attr("disabled",false);
            $("#nuevo").attr("disabled",false);
            $("#tablaResultados").html(data.split("///////")[0]);
            var cadJson = jQuery.parseJSON(data.split("///////")[1]);
            var group = new H.map.Group();
            //add a group objets
            map.addObject(group);
            // add 'tap' event listener, that opens info bubble, to the group
            group.addEventListener('tap', function (evt) {
                // event target is the marker itself, group is a parent event target
                // for all objects that it contains
                var bubble =  new H.ui.InfoBubble(evt.target.getPosition(), {
                    // read custom data
                    content: evt.target.getData()
                });
                // show info bubble
                ui.addBubble(bubble);
            }, false);
            $.each(cadJson, function(i, item) {
                setPointOnMap(group,{lat:parseFloat(item.lat), lng: parseFloat(item.lng)},'<div style="width:300px;"><div><b>Restaurante '+(i+1)+': </b><br/>'+ item.nombreRestaurante+'</div><div><b>Direccion '+(i+1)+': </b><br/>'+ item.direccion+'</div></div>');
                //console.log(item.lat);
            });
            map.setViewBounds(group.getBounds());
            getTabla();
        });
    });
	
};
$(document).ready(function() {
    obj = new ini();
});