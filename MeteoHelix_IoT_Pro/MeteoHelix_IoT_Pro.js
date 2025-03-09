// MeteoHelix IoT Pro periodic payload decoder
function decodeUplink(input) {
    var bytes = input.bytes;

    var pos = 0;
    var bindata = "";

    var ConvertBase = function (num) {
        return {
            from : function (baseFrom) {
                return {
                    to : function (baseTo) {
                        return parseInt(num, baseFrom).toString(baseTo);
                    }
                };
            }
        };
    };

    function pad(num) {
        var s = "0000000" + num;
        return s.slice(-8);
    }

    ConvertBase.dec2bin = function (num) {
        return pad(ConvertBase(num).from(10).to(2));
    };

    ConvertBase.bin2dec = function (num) {
        return ConvertBase(num).from(2).to(10);
    };

    function data2bits(data) {
        var binary = "";
        for(var i=0; i<data.length; i++) {
            binary += ConvertBase.dec2bin(data[i]);
        }
        return binary;
    }

    function bitShift(bits) {
        var num = ConvertBase.bin2dec(bindata.substr(pos, bits));
        pos += bits;
        return Number(num);
    }

    function precisionRound(number, precision) {
        var factor = Math.pow(10, precision);
        return Math.round(number * factor) / factor;
    }
    

    bindata = data2bits(bytes);

    var typ_e = precisionRound(bitShift(2), 1);

    var batt = bitShift(5);
    var battery = precisionRound(batt + 3, 2); //3V is minimum value

    var temp = precisionRound(bitShift(11)*0.1, 2);
    var temperature = precisionRound(temp + (-100), 2); //-100 is minimum value
    
    var t_min = precisionRound(bitShift(6)*0.1, 2);
    var t_max = precisionRound(bitShift(6)*0.1, 2);
    
    var humidity = precisionRound(bitShift(9)*0.2, 2);
    
    var press = precisionRound(bitShift(14)*5, 2);
    var pressure = precisionRound(press + 50000, 2);
    
    var irradiation = precisionRound(bitShift(10)*2, 2);
    var irr_max = precisionRound(bitShift(9)*2, 2);
    var rain = precisionRound(bitShift(8)*1, 2);



    var decoded = {
        "msg_type": typ_e,
        "battery": battery,
        "temperature": temperature,
        "temp_min": t_min,
        "temp_max": t_max,
        "humidity": humidity,
        "pressure" : pressure,
        "irradiation": irradiation,
        "irr_max": irr_max,
        "rain_clicks": rain,
	"time_interval": "NOT IMPLEMENTED",
    };

    return {
        data: decoded
    };
}