//MeteoRain IoT Pro Gen2 peridoc payload decoder
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
    
    function batteryIndicator(index, battery_bit, min_value=3.3) {
        var remainder = index % 10;
        var result = remainder < 4 ? remainder * 0.2 + min_value : remainder * 0.2 + min_value - 1;
        
        var rounded = Math.round(result * 10) / 10;
        return battery_bit === 1 ? `> ${rounded} V` : `< ${rounded} V`;
    }    

    bindata = data2bits(bytes);

    var index = precisionRound(bitShift(8), 1);
    var battery_bit = bitShift(1);
    var battery = batteryIndicator(index, battery_bit);
    
    var rain_clicks = precisionRound(bitShift(12)*1, 2);
    var tim = precisionRound(bitShift(10)*1, 2);
    
    var time_bt = 0.0;

    if ( tim > 0 )
    {
      time_bt = ( 728 / tim );
      time_bt = time_bt * time_bt;
      
    }
  
    //var time_bt = ( 728 / tim );
    //time_bt = time_bt * time_bt;
    
    var rain_intensity = precisionRound(bitShift(12)*0.01, 2);
    var temp = precisionRound(bitShift(1)*1, 2);
    var debug = precisionRound(bitShift(1)*1, 2);


    var decoded = {
        "index": index,
        "battery_bit": battery_bit,
        "battery_indicator": battery,
        "rain_clicks": rain_clicks,
        "time_btwn": time_bt,
        "rain_intensity_correction": rain_intensity,
        "temp above 2 deg": temp,
        "debug": debug,
    };

    return {
        data: decoded
    };
}
