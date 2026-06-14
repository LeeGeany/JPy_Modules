import os
import io
import folium
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QTimer

from geographiclib.geodesic import Geodesic
from branca.element import Element
from branca.element import Figure
import geopandas as gpd

class GeoWebView:
    def __init__(self, webengine: QWebEngineView):
        self.engine = webengine
        self.geod = Geodesic.WGS84

        # 지도 영역
        self.lat_min, self.lat_max = 33, 43
        self.lon_min, self.lon_max = 124, 132

        # 데이터 경로
        data_dir = "_maps"
        self.land = gpd.read_file(os.path.join(data_dir, "ne_10m_land", "ne_10m_land.shp"))
        self.rivers = gpd.read_file(os.path.join(data_dir, "ne_10m_rivers_lake_centerlines", "ne_10m_rivers_lake_centerlines.shp"))
        self.ocean = gpd.read_file(os.path.join(data_dir, "ne_10m_ocean", "ne_10m_ocean.shp"))

        # Folium 초기화
        self.map = folium.Map(location=[37.5, 127.5], zoom_start=7, tiles=None)
        self._init_map()
        self._inject_layers()

        # HTML 저장
        os.makedirs("_maps", exist_ok=True)
        self.map_html_path = os.path.abspath("_maps/map.html")
        self.map.save(self.map_html_path)

        # JS 실행을 loadFinished에 연결
        self.engine.loadFinished.connect(lambda ok: self.check_map_ready())

        # 지도 로드
        self.render()


    def _init_map(self):
        folium.GeoJson(
            self.land.cx[self.lon_min:self.lon_max, self.lat_min:self.lat_max],
            name="Land",
            style_function=lambda x: {"fillColor": "#dcdcdc", "color": "#808080", "weight": 0.5},
        ).add_to(self.map)

        folium.GeoJson(
            self.rivers.cx[self.lon_min:self.lon_max, self.lat_min:self.lat_max],
            name="Rivers",
            style_function=lambda x: {"color": "#66aaff", "weight": 1.0},
        ).add_to(self.map)

        folium.GeoJson(
            self.ocean.cx[self.lon_min:self.lon_max, self.lat_min:self.lat_max],
            name="Lakes",
            style_function=lambda x: {"fillColor": "#99ccff", "color": "#66aaff", "weight": 0.5},
        ).add_to(self.map)


    def _inject_layers(self):
        js_code = """
        <script>
        // folium이 자동으로 만든 map_* 객체를 window.map으로 등록
        window.addEventListener('load', function() {
            for (var key in window) {
                if (key.startsWith('map_')) {
                    window.map = window[key];
                    console.log('✅ window.map initialized:', key);
                    break;
                }
            }

            // map 객체가 준비된 뒤에 layer group 추가
            if (window.map) {
                window.pointLayer = L.layerGroup().addTo(window.map);
                window.lineLayer = L.layerGroup().addTo(window.map);

                window.addPoint = function(name, lat, lon) {
                    L.marker([lat, lon]).bindTooltip(name)
                     .bindPopup(`(${lat}, ${lon})`)
                     .addTo(pointLayer);
                };

                window.addLine = function(coords, color) {
                    L.polyline(coords, {color: color, weight:1}).addTo(lineLayer);
                };

                window.clearLayers = function() {
                    pointLayer.clearLayers();
                    lineLayer.clearLayers();
                };
            } else {
                console.error("❌ map object not found in window");
            }
        });
        </script>
        """

        e = Element(js_code)
        fig = Figure()
        fig.add_child(self.map)
        fig.html.add_child(e)


    def render(self):
        self.engine.load(QUrl.fromLocalFile(self.map_html_path))


    def check_map_ready(self):
        js_check = """
        if (typeof window.map !== 'undefined') {
            console.log('✅ window.map ready');
            true;
        } else {
            console.log('⏳ waiting for window.map');
            false;
        }
        """
        self.engine.page().runJavaScript(js_check, lambda result: self.on_check_result(result))


    def on_check_result(self, result):
        if result:
            print("✅ window.map is ready!")
            self.is_loaded = True
        else:
            # 아직 준비 안 됨 → 0.5초 후 다시 확인
            print("checking...")
            QTimer.singleShot(3000, self.check_map_ready)


    def add_point(self, name, lat, lon):
        js = f"addPoint('{name}', {lat}, {lon});"
        if self.is_loaded:
            self.engine.page().runJavaScript(js, lambda result: print("JS executed:", result))
        else:
            print("[WARN] Map not ready yet. Try after loadFinished signal.")


    def add_line(self, lat1, lon1, lat2, lon2, color="red"):
        line = self.geod.InverseLine(lat1, lon1, lat2, lon2)
        coords = [[line.Position(i*line.s13/200)['lat2'], line.Position(i*line.s13/200)['lon2']] for i in range(201)]
        js_coords = str(coords)
        js = f"addLine({js_coords}, '{color}');"
        self.engine.page().runJavaScript(js)


    def add_line_azimuth(self, name,  lat1, lon1, Azimuth, color="red"):
        result = self.geod.Direct(lat1, lon1, Azimuth, 500000.0)
        lat2, lon2 = result['lat2'], result['lon2']

        self.add_point(name, lat1, lon1)
        self.add_line(lat1, lon1, float(lat2), float(lon2), "blue")


    def clear(self):
        js = "clearLayers();"
        self.engine.page().runJavaScript(js)
