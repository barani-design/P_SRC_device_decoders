//MeteoWind IoT Pro periodic paylod decoder
function decodeUplink(input) {
    var bytes = input.bytes;

    var pos = 0;
    var bindata = "";

    var anemometer_slope = 0.6335;
    var anemometer_offset = 0.3582;

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

    var hz_avg = precisionRound(bitShift(12)*0.02, 2);
    var wind_ave = hz_avg > 0 ? precisionRound(hz_avg*anemometer_slope+anemometer_offset, 2) : 0;

    var hz_3sgust = hz_avg + precisionRound(bitShift(9)*0.1, 2);
    var wind_3sgust = hz_3sgust > 0 ? precisionRound(hz_3sgust*anemometer_slope+anemometer_offset, 2) : 0;

    var hz_1sgust = hz_3sgust + precisionRound(bitShift(8)*0.1, 2);
    var wind_1sgust = hz_1sgust > 0 ? precisionRound(hz_1sgust*anemometer_slope+anemometer_offset, 2) : 0;

    var hz_3min = precisionRound(bitShift(9)*0.1, 2);
    var wind_3smin = hz_3min > 0 ? precisionRound(hz_3min*anemometer_slope+anemometer_offset, 2) : 0;

    var hz_stdev = precisionRound(bitShift(8)*0.1, 2);

    var deg_1s_avg = precisionRound(bitShift(9)*1, 1);
    var deg_1s_gust = precisionRound(bitShift(9)*1, 1);
    var deg_1s_stdev = precisionRound(bitShift(8)*1, 1);

    var gust_time = precisionRound(bitShift(7)*5, 1);
    var alarm_sent = precisionRound(bitShift(1)*1, 1);

    var decoded = {
	"00A_device" : "MeteoWind IoT Pro",
        "index": index,
        "battery_bit": battery_bit,
        "battery_indicator": battery,
        "wind_ave": wind_ave,
        "wind_3s_gust": wind_3sgust,
        "wind_1s_gust": wind_1sgust,
        "wind_3s_min": wind_3smin,
        "wind_stdev": hz_stdev,
        "dir_ave": deg_1s_avg,
        "dir_1s_gust": deg_1s_gust,
        "dir_1s_stdev": deg_1s_stdev,
        "gust_time": gust_time,
        "alarm_sent": alarm_sent,
    };

    return {
        data: decoded
    };
}
