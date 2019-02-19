console.info("Loaded map.js");
console.info(document.location.origin);

var map;
var coordinates=[];

function initMap() {
    var nyc = {lat: 40.7128, lng: -74.006};

    map = new google.maps.Map(document.getElementById('map'), {
      zoom: 4,
      center: nyc
    });
  }

function UpdateCoordinates()
{  
    console.log("Clearing coordinates.");
    coordinates.forEach(function(c){
        c.setMap(null);
    });
    coordinates = []
    fetch(document.location.origin + "/locations")
    .then(res => res.json())
    .then((out) => {
    out.forEach(function(c) {
        console.log(c.latitude + "," + c.longtitude);
        coordinates.push(new google.maps.Marker({
            position: {lat: c.latitude, lng:c.longtitude},
            map: map,
            title: c.ip
          }));
    })
  })
  .catch(err => { throw err });
}

function UpdateCoordinatesHandler()
{
    try{
        UpdateCoordinates();
        setTimeout(UpdateCoordinatesHandler, 5000);
    }
    catch(e)
    {
        console.log(e);
        console.log("Error updating coordinates");
    }
}

UpdateCoordinatesHandler();