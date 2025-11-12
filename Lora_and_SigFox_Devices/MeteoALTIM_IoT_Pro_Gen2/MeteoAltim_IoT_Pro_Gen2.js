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
        var result = remainder < 5 ? remainder * 0.2 + min_value : remainder * 0.2 + min_value - 1;

        var rounded = Math.round(result * 10) / 10;
        return battery_bit === 1 ? `> ${rounded} V` : ` -- `;
    }

    bindata = data2bits(bytes);

    var index = precisionRound(bitShift(8), 1);

    var battery_bit = bitShift(1);
    var battery = batteryIndicator(index, battery_bit);

    var temperature = precisionRound(bitShift(6)*2, 1) - 45;
    var humidity = precisionRound(bitShift(4)*4, 1) + 40;
    var ref_p = ((precisionRound(bitShift(13)*10, 1)) + 30000);
    var diff_p0 = precisionRound(bitShift(10)*0.5, 1) - 256;
    var diff_p1 = precisionRound(bitShift(10)*0.5, 1)- 256;
    var diff_p2 = precisionRound(bitShift(10)*0.5, 1)- 256;
    var diff_p3 = precisionRound(bitShift(10)*0.5, 1)- 256;
    var diff_p4 = precisionRound(bitShift(10)*0.5, 1)- 256;
    var diff_p5 = precisionRound(bitShift(10)*0.5, 1)- 256;
    var std_dev0 = precisionRound(bitShift(6), 1);
    var std_dev1 = precisionRound(bitShift(6), 1);
    var std_dev2 = precisionRound(bitShift(6), 1);
    var std_dev3 = precisionRound(bitShift(6), 1);
    var std_dev4 = precisionRound(bitShift(6), 1);
    var std_dev5 = precisionRound(bitShift(6), 1);

    function toHexString(byteArray) {
        return Array.from(byteArray, function(byte) {
            return ('0' + (byte & 0xFF).toString(16)).slice(-2);
        }).join('')
    }

    var st = toHexString(input.bytes).toUpperCase();

    var decoded = {
        "00A_device" : "MeteoAltim IoT Pro Gen2",
        "payload" : st,
        "index": index,
        "battery_bit": battery_bit,
        "battery_indicator": battery,
        "temperature": temperature,
        "humidity": humidity,
        "ref_p": ref_p,
        "diff_p0":diff_p0,
        "diff_p1":diff_p1,
        "diff_p2":diff_p2,
        "diff_p3":diff_p3,
        "diff_p4":diff_p4,
        "diff_p5":diff_p5,
        "std_dev0":std_dev0,
        "std_dev1":std_dev1,
        "std_dev2":std_dev2,
        "std_dev3":std_dev3,
        "std_dev4":std_dev4,
        "std_dev5":std_dev5,
    };

    return {
        data: decoded
    };
}