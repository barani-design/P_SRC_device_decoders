// MeteoAG IoT Pro Gen2 periodic payload decoder for v1.02.002 +
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
          var result = remainder < 5 ? remainder * 0.2 + min_value : remainder * 0.2 + min_value - 1;
          var rounded = Math.round(result * 10) / 10;
          return battery_bit === 1 ? `> ${rounded} V` : ` -- `;
        }
        
    }    

    bindata = data2bits(bytes);

    var index = precisionRound(bitShift(8), 1);

    var battery_bit = bitShift(1);
    var battery = batteryIndicator(index, battery_bit);

    var soil_select = precisionRound(bitShift(3)*1, 2);
    var temp_select = precisionRound(bitShift(3)*1, 2);
    var leaf_select = precisionRound(bitShift(3)*1, 2); 
    
    var soil_e1 = precisionRound(bitShift(12)*1, 2);  
    var soil_e2 = precisionRound(bitShift(12)*1, 2);  
    var soil_e3 = precisionRound(bitShift(12)*1, 2);  

    var soil_f1 = precisionRound(bitShift(12)*1, 2);  
    var soil_f2 = precisionRound(bitShift(12)*1, 2);  
    var soil_f3 = precisionRound(bitShift(12)*1, 2);    
  
    var soil_g3 = precisionRound(bitShift(12)*1, 2); 
    
    var dbg = precisionRound(bitShift(2)*1, 2);
    


    var decoded = {
	"00A_device" : "MeteoAG IoT Pro Gen2",
        "index": index,
        "battery_bit": battery_bit,
        "battery_indicator": battery,
        "soil_select": soil_select,
        "temp_select": temp_select,
        "leaf_select": leaf_select,
        "soil_e1": soil_e1,
	"soil_e2": soil_e2,
	"soil_e3": soil_e3,
        "soil_f1": soil_f1,
	"soil_f2": soil_f2,
	"soil_f3": soil_f3,
	"soil_g3": soil_g3,	    
        "dbg": dbg,
    };

    return {
        data: decoded
    };
}