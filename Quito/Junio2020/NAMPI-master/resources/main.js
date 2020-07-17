function initMap() {
  var directionsService = new google.maps.DirectionsService();
  var directionsRenderer = new google.maps.DirectionsRenderer();
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 12,
    center: {
      lat: -0.1865938,
      lng: -78.570625
    }
  });
  directionsRenderer.setMap(map);

  var onChangeHandler = function(event) {
    calculateAndDisplayRoute(directionsService, directionsRenderer, event);
  };
  document.getElementById('upload').addEventListener('change', onChangeHandler);
}

function calculateAndDisplayRoute(directionsService, directionsRenderer, event) {
  var files = event.target.files; // FileList object
  excelToJSON(files[0], directionsService, directionsRenderer);
}

let excelToJSON = async function(file, directionsService, directionsRenderer) {

  let json_object;
  var reader = new FileReader();

  reader.onload = function(e) {
    var data = e.target.result;
    let points;
    let wp;
    var workbook = XLSX.read(data, {
      type: 'binary'
    });
    workbook.SheetNames.forEach(function(sheetName) {
      // Here is your object
      var XL_row_object = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[sheetName]);
      json_object = JSON.stringify(XL_row_object);
      points = JSON.parse(json_object);
      points = points.map((point)=>({ Lat:point.Lat,Long:point.Long}))
      console.log(points);
      points = points.map((point)=>(point.Lat + ',' +point.Long));
      console.log(points);
      wp = points.map((point)=>({location:point, stopover:true}));
      wp.shift();
      wp.pop();
    })
    //display the map
    directionsService.route({
        origin: points[0],
        destination: points[points.length -1],
        waypoints: wp ,
        optimizeWaypoints: true,
        travelMode: 'DRIVING'
      },
      function(response, status) {
        if (status === 'OK') {
          directionsRenderer.setDirections(response);
        } else {
          window.alert('Directions request failed due to ' + status);
        }
      });
    //display groups of users 
    // existing user
    const sortedUsers = {
    1:["Usuario A","Usuario B", "Usuario C"], 
    2:["Usuario D", "Usuario G"],
    3:["Usuario F"],
    4:["Usuario E"]
    }
    
    document.getElementById("user-clusters").style.display = "block"
    
    //TODO dynamic add of user
    /* let userClustersDiv = document.getElementById("user-clusters");
    let newdiv = document.createElement('div');
    newdiv.id = 'newid';
    let para = document.createElement("P");              
        para.innerText = "This is a paragraph";             
        newdiv.appendChild(para);  
    userClustersDiv.appendChild(newdiv); */
  };
  reader.onerror = function(ex) {
    console.log(ex);
  };

  reader.readAsBinaryString(file);
};

function sayHello(){
	console.log('arriba');
}

let coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
}