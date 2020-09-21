import json
import sys
import geojson
import shapely.wkt
from shapely.geometry import shape

def geojson2Wkt():
    print("【GeoJSON转WKT格式】\n")
    opt = input("$ 请输入需要转换的GeoJSON文件或拖动文件到此处 ")

    try:
        with open(opt) as map:
            g1 = geojson.load(map)

        g1 = g1["features"][0]["geometry"]
        geom = shape(g1)
        geomWkt = geom.wkt
        #print(geomWkt)
    except Exception as e:
        print(e)
        return 0

    with open("temp_wkt.txt", "w+", encoding="utf-8") as f:
        f.write(geomWkt)

    print("转换完成，已保存在当前目录'temp_wkt.txt'文件中\n")
    return 0