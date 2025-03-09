//MeteoHelix IoT Pro Gen2 Periodic payload decoder
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
        var remainder = index % 5;
        
        if ( remainder > 4)
        {
          return 0;
        }
        
        else
        {
          var result = remainder < 4 ? remainder * 0.2 + min_value : remainder * 0.2 + min_value - 1;
          var rounded = Math.round(result * 10) / 10;
          return battery_bit === 1 ? `> ${rounded} V` : `< ${rounded} V`;
        }
        
    }    

    bindata = data2bits(bytes);

    var index = precisionRound(bitShift(8), 1);

    var battery_bit = bitShift(1);
    var battery = batteryIndicator(index, battery_bit);

    var temp_avg = precisionRound(bitShift(14)*0.01, 2);
    temp_avg = precisionRound(temp_avg + (-50), 2);
    
    //tem_avg = Math.round(temp_avg * 10) / 10;

    var temp_min_diff = precisionRound(bitShift(8)*0.05, 2);
    var temp_max_diff = precisionRound(bitShift(8)*0.05, 2);
    
    var temp_min = temp_avg - temp_min_diff
    var temp_max = temp_avg + temp_min_diff
    
    //tem_avg = Math.round(temp_avg * 10) / 10;
    temp_min = Math.round(temp_min * 100) / 100;
    temp_max = Math.round(temp_max * 100) / 100;
    
    var humidity = precisionRound(bitShift(9)*0.2, 2);
    var pressure = precisionRound(bitShift(15)*2.5, 2);
    
    pressure = pressure + 30000;
    
    var irradiation = precisionRound(bitShift(11)*1, 2);
    var irr_min_diff = precisionRound(bitShift(10)*2, 2);
    var irr_max_diff = precisionRound(bitShift(10)*2, 2);
    
    var irr_min = irradiation - irr_min_diff
    var irr_max = irradiation + irr_max_diff
    
    var rain_clicks = precisionRound(bitShift(12)*1, 2);
    
    var t_int = precisionRound(bitShift(10)*1, 2);
    
    var time_interval = 0.0
    
    if ( t_int > 0 )
    {
        time_interval = 728 / t_int
        time_interval = 	 time_interval * time_interval   
    }
    
    var rain_intens = precisionRound(bitShift(10)*0,01, 2);
    
    var alarm_dbg = precisionRound(bitShift(1)*1, 2);
    


    var decoded = {
	"00A_device" : "MeteoHelix IoT Pro Gen2",
        "index": index,
        "battery_bit": battery_bit,
        "battery_indicator": battery,
        "temp_avg": temp_avg,
        "temp_min": temp_min,
        "temp_max": temp_max,
        "humidity": humidity,
        "pressure" : pressure,
        "irradiation": irradiation,
        "irr_min": irr_min,
        "irr_max": irr_max,
        "rain_clicks": rain_clicks,
	"time_interval": time_interval,
	"rain_intens": rain_intens,
        "alarm_dbg": alarm_dbg,
    };

    return {
        data: decoded
    };
}