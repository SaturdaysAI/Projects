<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="css/bootstrap.min.css"/>
        <style>body {padding-top: 60px;}</style>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    </head>
    <body>
        <div class="navbar navbar-inverse navbar-fixed-top">
            <div class="navbar-inner">
                <img src="images/logoIA2.png" style="width: 75px;height: 50px;float: left;padding-left: 25px;padding-top: 10px;" />
                <!--i class="material-icons" style="padding-left: 25px;padding-top: 10px;color: #FFFFFF;float: left;">where_to_vote</i-->
                <div id="container" style="float: left;color:#FFFFFF;font-size: 20px;font-weight: bolder;padding-left: 10px;padding-top: 15px;">
                    GG-EAT
                </div>
            </div>
        </div>

        <div id="container" style="width: 100%;background: #d3d3d3;margin-top: 1px;height: auto;float:left;">
            <div style="width: 24.5%;margin: 3px;background: #072e35;color:#FFFFFF;float:left;height: 550px;">
                <div id="formulario" style="margin:10px;width: 100%;">
                    <!--div style="width: 95%;margin-top: 5px;"><b>C.I.:</b></div>
                    <input type="text" id="cedulaUsuario" style="width: 50%;color: #000000;" maxlength="10" class="cantidad"/-->
                    <div style="width: 95%;margin-top: 5px;"><b>Nombre:</b></div>
                    <input type="text" id="nombreUsuario" style="width: 95%;color: #000000;" maxlength="50" class="cambio_mayuscula nombre" />
                    <div style="width: 95%;margin-top: 10px;">
                        <b>G&eacute;nero:</b>
                        <input type="radio" name="genero" id="generoH" class="generoClass" value="1" selected />&nbsp;Hombre
                        <input type="radio" name="genero" id="generoH" class="generoClass" value="0"/>&nbsp;Mujer
                    </div>
                    <div style="width: 95%;margin-top: 10px;">
                        <b>Ambiente:</b>
                        <input type="radio" name="ambiente" id="ambienteA" class="ambienteClass" value="1" selected />&nbsp;Abierto
                        <input type="radio" name="ambiente" id="ambienteA" class="ambienteClass" value="0"/>&nbsp;Cerrado
                    </div>
                    <div style="width: 95%;margin-top: 15px;">
                        <div style="width:45%;float: left;">
                            <input type="checkbox" id="menu" class="checkSeleccion" />
                            <b>Men&uacute;</b>
                        </div>
                        <div style="width:45%;float: left;">
                            <input type="checkbox" id="vegetariana" class="checkSeleccion" />
                            <b>Vegetariano</b>
                        </div>
                    </div>
                    <div style="width: 95%;margin-top: 15px;">
                        <div style="width:45%;float: left;">
                            <input type="checkbox" id="pollo" class="checkSeleccion" />
                            <b>Pollo</b>
                        </div>
                        <div style="width:45%;float: left;">
                            <input type="checkbox" id="carne" class="checkSeleccion" />
                            <b>Carne</b>
                        </div>
                    </div>
                    <div style="width: 95%;margin-top: 15px;">
                        <div style="width:45%;float: left;">
                            <input type="checkbox" id="comida_rapida" class="checkSeleccion" />
                            <b>Comida R&aacute;pida</b>
                        </div>
                        <div style="width:45%;float: left;">
                            <input type="checkbox" id="lacteos" class="checkSeleccion" />
                            <b>Lacteos</b>
                        </div>
                    </div>
                    <div style="width: 95%;margin-top: 15px;">
                        <div style="width:45%;float: left;">
                            <input type="checkbox" id="menestra" class="checkSeleccion" />
                            <b>Menestra</b>
                        </div>
                        <div style="width:45%;float: left;">
                            &nbsp;&nbsp;&nbsp;&nbsp;
                        </div>
                    </div>
                    <br/><br/><br/>
                    <div style="width: 95%;margin-top: 100px;text-align: center;">
                        <div style="width:28%;float: left;margin-left: 50px;">
                            <input type="button" id="nuevo" value="Cancelar" style="width: 100%;margin-left: 3px;color: #204d74;font-weight: bolder;" />
                        </div>
                        <!--div style="width:28%;float: left;margin-left: 3px;">
                            <input type="button" id="cancelar" value="Cancelar" style="width: 100%;margin-left: 3px;color: #204d74;font-weight: bolder;" />
                        </div-->
                        <div style="width:28%;float: left;margin-left: 20px;">
                            <input type="button" id="predecir" value="Predecir" style="width: 100%;margin-left: 3px;color: #204d74;font-weight: bolder;" />
                        </div>
                    </div>
                    <div style="width: 95%;margin-top: 150px;text-align: center;">
                        <img src="images/logo.png" style="width: 125px; height: 125px;" />
                    </div>
                </div>
            </div>
            <div style="width: 74.5%;margin: 3px;background: #FFFFFF;float:left;height: 375px;">
                <div id="mapContainer" style="width: 100%;height: 375px;border: 3px groove #ededed;float:left;"></div>
            </div>
            <div style="width: 74.5%;margin: 3px;background: #FFFFFF;float:left;height: 170px;color:#000000;">
                <div id="tablaResultados" style="width: 100%;height: 170px;border: 3px groove #ededed;float:left;display: none;padding: 3px;">
                </div>
            </div>
        </div>
    </body>

    <script src="resources/jquery-1.3.2.min.js"></script>
    <link rel="stylesheet" type="text/css" href="https://js.cit.api.here.com/v3/3.0/mapsjs-ui.css" />
    <script type="text/javascript" src="https://js.cit.api.here.com/v3/3.0/mapsjs-core.js"></script>
    <script type="text/javascript" src="https://js.cit.api.here.com/v3/3.0/mapsjs-service.js"></script>
    <script type="text/javascript" src="https://js.cit.api.here.com/v3/3.0/mapsjs-ui.js"></script>
    <script type="text/javascript" src="https://js.cit.api.here.com/v3/3.0/mapsjs-mapevents.js"></script>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link rel="stylesheet" href="resources/datatable/css/demo_page.css?rand=<?= rand() ?>" type="text/css" media="screen" title="no title" charset="utf-8">
    <link rel="stylesheet" href="resources/datatable/css/estilotabla.css?rand=<?= rand() ?>" type="text/css" media="screen" title="no title" charset="utf-8">
    <link rel="stylesheet" href="resources/datatable/css/proy_post.css?rand=<?= rand() ?>" type="text/css" media="screen" title="no title" charset="utf-8">
    <script type="text/javascript" language="javascript" src="resources/datatable/js/jquery.dataTables.js"></script>
    <script src="js/actionPage.js"></script>
</html>
