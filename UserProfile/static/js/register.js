
function showPassword(value) {
    console.log(value);
    let password = null;
    if (value == 1) {
        password = document.getElementById("id_password1");
    } else {
        password = document.getElementById("id_password2");
    }
    password.type = password.type == "text" ? "password" : "text";
}

function closeMap(){
    $('.map-group').remove();
}

function showMap() {
    $(".wrapper").prepend(
        '<div class="map-group"> \
            <i class="fa-solid fa-xmark" onclick="closeMap()"></i> \
            <div id="map"></div> \
        </div>');
    const apiKey = "olCohv5QvxMN4f4Opgoi";

    const map = L.map("map").setView([16.0476897, 108.2466488], 12); //starting position
    var marker = null;
    L.tileLayer(
        `https://api.maptiler.com/maps/streets-v2/{z}/{x}/{y}.png?key=${apiKey}`,
        {
            //style URL
            tileSize: 512,
            zoomOffset: -1,
            minZoom: 1,
            attribution:
                '\u003ca href="https://www.maptiler.com/copyright/" target="_blank"\u003e\u0026copy; MapTiler\u003c/a\u003e \u003ca href="https://www.openstreetmap.org/copyright" target="_blank"\u003e\u0026copy; OpenStreetMap contributors\u003c/a\u003e',
            crossOrigin: true,
        }
    ).addTo(map);
    L.control.maptilerGeocoding({ apiKey: apiKey }).addTo(map);
    if (navigator.geolocation && marker == null) {
        navigator.geolocation.getCurrentPosition(function (position) {
            lat = position.coords.latitude;
            lng = position.coords.longitude;
            console.log(lat, lng);
            // this is just a marker placed in that position
            marker = L.marker([lng, lat]).addTo(map);

            // move the map to have the location in its center
            map.panTo(new L.LatLng(lng, lat));
        });
    }

    maptilersdk.config.apiKey = apiKey;
    map.on("click", async (e) => {
        const { lat, lng } = e.latlng;
        const results = await maptilersdk.geocoding.reverse([lng, lat]);
        address = results.features[0].place_name_vi;
        $('.input-address').val(address);
        marker.setLatLng([lat, lng])
            .update()
            .addTo(map)
            .bindPopup(`<h3>Địa chỉ:</h3> ${address}`)
            .openPopup();
    });
}
