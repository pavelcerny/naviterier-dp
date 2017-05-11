/**
 * Created by cerny on 04.05.2017.
 */

function getAddress(lat, lon, callback) {
    // get address from coordinates
    $.get(
        "{% url 'apis:addressFromGps' %}",
        {'lat': lat, 'lon': lon},
        callback
    );
}

function getGPS(address, callback) {
    // get gps fromAddress
    $.get(
        "{% url 'apis:gpsFromAddress' %}",
        {'address': address},
        callback);
}

function inNaviterierDB(address, callback) {
    //check if address is Naviterier
    //todo
    return true;
}