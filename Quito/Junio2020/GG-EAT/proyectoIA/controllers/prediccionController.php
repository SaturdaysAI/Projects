<?php

/**
 * Description of prediccionController
 *
 * @author Cristian Yunga
 */
class prediccionController {

    public function __construct($p) {
        switch ($p['accion']) {
            case 'getPrediction':
                $this->getPrediction($p['datos']);
                break;
        }
    }

    protected function getPrediction($p) {
        //print_r($p);
        //echo $p["cedula"];
        $arrFinal = array();
        $arrFinal['id_cliente'] = rand(1000000000,9999999999);
        foreach ($p as $k=>$value) {
            if($k!="nombre") {
                $arrFinal[$k] = intval($value);
            } else {
                $arrFinal[$k] = $value;
            }
        }
        $cadenaJson = json_encode($arrFinal);
        $fp = fopen("/www/proyectoIA/documents/cliente.json", "w");
        //chmod("/www/proyectoIA/documents/cliente.json", 0755);
        if ($fp) {
            fwrite($fp, $cadenaJson);
            fclose($fp);
        }
        chmod("/www/proyectoIA/documents/cliente.json", 0755);
        exec("python3 ../models/lecturaDatos.py 2>&1", $output);
        //print"<pre>";print_r($output);
        exec("python3 ../models/prediccion.py 2>&1", $output);
        //print"<pre>";print_r($output);
        $csvResult = "/www/proyectoIA/results/resutaldo.csv";
        if(file_exists($csvResult)) {
            $readCsvResult = file($csvResult);
            //print_r($readCsvResult);
        }
        unlink($csvResult);
        $csvGeneral = "/www/proyectoIA/dataset/general.csv";
        if(file_exists($csvGeneral)) {
            $readCsvGeneral = file($csvGeneral);
            //print "<pre>";print_r($readCsvGeneral);
        }
        $arrFinal = array();
        if(count($readCsvResult)>0 && count($readCsvGeneral)>0) {
            foreach ($readCsvResult as $k=>$value) {
                if($k!=0) {
                    //print_r($value);
                    list($gustar, $idRestaurante) = explode(";", $value);
                    //echo $idRestaurante."<br/><br/>";
                    foreach ($readCsvGeneral as $k2=>$value2) {
                        if($k2!=0) {
                            list($idR,$tipo,$nombre,$latitud,$longitud,$raiting,$direccion,$status,$price_level) = explode(";", $value2);
                            //echo $idR."<br/>";
                            if(intval($idRestaurante)==intval($idR)) {
                                $arrFinal[] = array("idRestaurante" => $idR, "nombreRestaurante" => $nombre, "lat" => $latitud, "lng" => $longitud, "direccion" => $direccion);
                            }
                        }
                    }
                }
            }
        }
        //print_r($arrFinal);
        echo $this->getTablaResultados($arrFinal)."///////". json_encode($arrFinal);
        //echo $cadenaJson;
    }

    protected function getTablaResultados($arrFinal) {
        $html= '<table border="1" id="gridResultados">';
            $html.= '<thead>';
                $html.= '<tr>';
                    $html.= '<th align="center" style="text-align:center;">No.</th>';
                    $html.= '<th align="center" style="text-align:center;">Nombre Restaurante</th>';
                    $html.= '<th align="center" style="text-align:center;">Direcci&oacute;n</th>';
                    //$html.= '<th></th>';
                $html.= '</tr>';
            $html.= '</thead>';
            $html.= '<tbody>';
                foreach ($arrFinal as $k=>$value) {
                    $html.= '<tr>';
                        $html.= '<td align="center">'.($k+1).'</td>';
                        $html.= '<td>'.$value['nombreRestaurante'].'</td>';
                        $html.= '<td>'.$value['direccion'].'</td>';
                        //$html.= '<td align="center"></td>';
                    $html.= '</tr>';
                }
            $html.= '</tbody>';
        $html.= '</table>';
        return $html;
    }

}

$p = $_REQUEST;
new prediccionController($p);
