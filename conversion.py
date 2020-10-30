import logging as log
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
    Name:   MillisecondsToSeconds
    Desc:   Takes integer milliseconds and converts it to float seconds
    Param:  rate - milliseconds (integer)
    Return: rate in seconds (float)
'''
def MillisecondsToSeconds(rate):
    return (float(rate) / 1000)
