//MeteoWind_IoT_Pro_Gen2 HNWL periodic payload decoder
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
        	
        var result = remainder < 5 ? remainder * 0.2 + min_value : remainder * 0.2 + min_value - 1;
        
        var rounded = Math.round(result * 10) / 10;
        return battery_bit === 1 ? `== ${rounded} V` : `!= ${rounded} V`;
    }    

    bindata = data2bits(bytes);

    var index = precisionRound(bitShift(8), 1);

    var batt = precisionRound(bitShift(2)*0.2, 2);
    var battery = precisionRound(batt + 3,5 2); //3,5V is minimum value
    
    //var battery_bits = bitShift(2);
    
    //var battery = batteryIndicator(index, battery_bit);

    var hz_avg1 = precisionRound(bitShift(10)*0.1, 2);
    var hz_avg1 = precisionRound(bitShift(10)*0.1, 2);
    var hz_avg1 = precisionRound(bitShift(10)*0.1, 2);
    var hz_avg1 = precisionRound(bitShift(10)*0.1, 2);
    var hz_avg1 = precisionRound(bitShift(10)*0.1, 2);
    var hz_avg1 = precisionRound(bitShift(10)*0.1, 2);
    var hz_avg1 = precisionRound(bitShift(10)*0.1, 2);
    var hz_avg1 = precisionRound(bitShift(10)*0.1, 2);

    var deg_1s_avg1 = precisionRound(bitShift(8)*2, 1);
    var deg_1s_avg2 = precisionRound(bitShift(8)*2, 1);
    var deg_1s_avg3 = precisionRound(bitShift(8)*2, 1);
    var deg_1s_avg4 = precisionRound(bitShift(8)*2, 1);
    var deg_1s_avg5 = precisionRound(bitShift(8)*2, 1);
    var deg_1s_avg6 = precisionRound(bitShift(8)*2, 1);
    var deg_1s_avg7 = precisionRound(bitShift(8)*2, 1);
    var deg_1s_avg8 = precisionRound(bitShift(8)*2, 1);
  
    var debug = precisionRound(bitShift(6)*1, 1);

    var decoded = {
	"00A_device" : "MeteoWind IoT Pro Gen2 HNWL",
        "index": index,
        "battery_bits": batt,
        "battery_indicator": battery,
        "wind_Hz_AVG1": hz_avg1,
	"wind_Hz_AVG2": hz_avg2,
	"wind_Hz_AVG3": hz_avg3,
        "wind_Hz_AVG4": hz_avg4,    
        "wind_Hz_AVG5": hz_avg5,
        "wind_Hz_AVG6": hz_avg6,
        "wind_Hz_AVG7": hz_avg7,
        "wind_Hz_AVG8": hz_avg8,
	"wind_DEG_AVG1": deg_1s_avg1,    
        "wind_DEG_AVG2": deg_1s_avg2,
	"wind_DEG_AVG3": deg_1s_avg3,
	"wind_DEG_AVG4": deg_1s_avg4,
	"wind_DEG_AVG5": deg_1s_avg5,
	"wind_DEG_AVG6": deg_1s_avg6,
	"wind_DEG_AVG7": deg_1s_avg7,
	"wind_DEG_AVG8": deg_1s_avg8,
        "dbg": debug,
    };

    return {
        data: decoded
    };
}

