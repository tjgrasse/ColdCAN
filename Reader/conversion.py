import logging as log
import decimal

'''
    Name:   RawToMetric
    Desc:   Takes a raw CAN values and uses the offset and resolution to compute the metric value
    Param:  value - Raw Value 
    Param:  resolution - Scaling factor assigned to the variable
    Param:  offset - offset value applied to value
    Return: metrict value as a float
'''
def RawToMetric(value, resolution, offset):
    val = float((value * resolution) + offset)
    log.debug("value=%d resolution=%f offset=%d NewVal=%f", value, resolution, offset, val)
    return val

'''
    Name:   MetricToRaw
    Desc:   Takes the metric value and converts it back to the raw CAN message
    Param:  value - Metric Value 
    Param:  resolution - Scaling factor assigned to the variable
    Param:  offset - offset value applied to value
    Return: raw CAN variable as an integer
'''
def MetricToRaw(value, resolution, offset):
    val = int((value - offset) / resolution)
    log.debug("value=%d resolution=%f offset=%d NewVal=%f", value, resolution, offset, val)
    return val

'''
    Name:   MetricToRawRnd
    Desc:   Takes the metric value and converts it back to the raw CAN message
    Param:  value - Metric Value 
    Param:  resolution - Scaling factor assigned to the variable
    Param:  offset - offset value applied to value
    Return: raw CAN variable as an integer
    Ref:    Information on the use of the decimal module to appy half-up rounding in python 
            instead of the default banker's rounding.
            https://stackoverflow.com/questions/43851273/how-to-round-float-0-5-up-to-1-0-while-still-rounding-0-45-to-0-0-as-the-usual?rq=1 
'''
def MetricToRawRnd(value, resolution, offset):
    val = (value - offset) / resolution
    raw = decimal.Decimal(val).quantize(decimal.Decimal('1'), rounding=decimal.ROUND_HALF_UP)
    log.debug("value=%d resolution=%f offset=%d NewVal=%f", value, resolution, offset, raw)
    return int(raw)

'''
    Name:   MillisecondsToSeconds
    Desc:   Takes integer milliseconds and converts it to float seconds
    Param:  rate - milliseconds (integer)
    Return: rate in seconds (float)
'''
def MillisecondsToSeconds(rate):
    return (float(rate) / 1000)
     
'''
    Name:   StrIsFloat
    Desc:   Takes takes a string and check if valid float
    Param:  string - a string that should represent a float
    Return: true if float / false if not float
'''
def StrIsFloat(string):
    try: 
    	float(string)
    	return True
    except ValueError:
    	return False
