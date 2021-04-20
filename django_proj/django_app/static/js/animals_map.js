function initMap () {
    let map = new google.maps.Map(
        document.getElementById("WinMap"),
        {
            zoom: 10,
            center: {lat: 59.93863, lng: 30.31413},
        }
    );

    let markers = document.getElementById('markers').children;

    for (let i = 0; i < markers.length; i++)
    {
        let li_m = markers[i];

        let plat = parseFloat(li_m.children[0].innerText);
        let plng = parseFloat(li_m.children[1].innerText);

        let latLng = new google.maps.LatLng(plat, plng);
        let marker = new google.maps.Marker({
            position: latLng,
            map: map,
        });

        let infowindow = new google.maps.InfoWindow
        ({
            content: li_m.children[2].innerHTML,
        });

        google.maps.event.addListener(marker, 'click', function()
        {
            infowindow.open(map,marker);
        });
    }
}