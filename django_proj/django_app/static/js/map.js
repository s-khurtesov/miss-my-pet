let marker;
let map;

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 10,
        center: {lat: 59.93863, lng: 30.31413},
    });

    marker = new google.maps.Marker({
        map: map,
    });

    map.setOptions({draggableCursor: 'crosshair'});

    // Add a listener for the click event
    map.addListener("click", addLatLng);
}

// Handles click events on a map, and adds a new point to the Polyline.
function addLatLng(event) {

    // Add a new marker
    marker.setMap(null);
    marker = new google.maps.Marker({
        position: event.latLng,
        map: map,
    });

    //Add a var for sending values to server
    var latitude = document.getElementById("latitude");
    var longitude = document.getElementById("longitude");
    latitude.value=event.latLng.lat();
    longitude.value=event.latLng.lng();
}