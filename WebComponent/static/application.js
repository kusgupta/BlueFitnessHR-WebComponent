
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://127.0.0.1:5000' + '/test');
    //receive details from server
    socket.on('heartRate', function(msg) {
        console.log("Received number" + msg.heartRate);
        //maintain a list of ten numbers
        $('#log').html(numbers_string);
    });

});
