import httplib2, json, time

def fetchforecast(coorlat='59.11', coorlon='18.10', wservice="smhi"):
    if wservice=="smhi":
        h = httplib2.Http('.cache')
        response, content = h.request('http://opendata-download-metfcst.smhi.se/api/category/pmp2g/version/1/geopoint/lat/59.11/lon/18.10/data.json')
        contentdict = json.loads(content.decode('utf-8'))
        wserielist = contentdict['timeseries']
    else:
        wserielist = []
    return wserielist

def extrweather(forcdata, hourfwd=1):
    weatherf = forcdata[hourfwd-1]
    #isotime - adds 30min+ 30 min*hourfwd-1, because weatherf returns next higher validTime forcast, so localtime 11.30.01-12.30.00 will show the forcast for 13.00, 12.30.01- will show 14.00
    isotime = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(time.time()+1800+1800*(hourfwd-1)))
    # a generator! pick desired forcast depending on hourfwd argument
    weatherf = next((item for item in forcdata if item["validTime"] >= isotime), None)
    #paramshort = ['t', 'wd', 'ws', 'tstm', 'tcc', 'pcat', 'pit', 'validTime']
    paramshort = ['t', 'wd', 'ws', 'tstm', 'tcc_mean', 'pcat', 'pmean', 'validTime']
    precicategory = ['no', 'snow', 'snow and rain', 'rain', 'drizzle', 'freezing rain', 'freezing drizzle']
    # filter out (or slice) keys and values corresponding to keys in paramshort, from weatherf
    wreportdic = { kval:weatherf[kval] for kval in paramshort }
    #print(wreportdic)
    # build string from the extracted forecast - just for testing, wreportdic is to be used to trigger graphics and later gpioports
    wreportstr = " Temperature: {t}*C. Wind direction: {wd}*. Wind speed: {ws}m/s. Probability thunderstorm:{tstm}%. \
Total cloud cover: {tcc_mean}/8. Precipitation: {pcat}. Precipitation intensity total: {pmean} @{validTime}".format(**wreportdic)
    return wreportstr

if __name__ == '__main__':
    forecast = fetchforecast()
    print(extrweather(forecast, 1))
    print(extrweather(forecast, 2))
    print(extrweather(forecast, 3))
          
    
def logger(func):
    def inner ( *args, **kwargs):
        print("TimeNow, args: {}, kwargs: {}".format(args, kwargs))
        return func(*args, **kwargs)
    return inner
