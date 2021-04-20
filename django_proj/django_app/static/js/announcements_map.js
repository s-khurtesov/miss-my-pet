function initMap(lat,lng) {
	const myLatLng = { lat,lng };
	map = new google.maps.Map(document.getElementById("WinMap"), {
		zoom: 14,
		center: myLatLng,
	});

	var marker = new google.maps.Marker({
	position: myLatLng,
	map,
	});
}