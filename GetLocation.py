import geocoder
import math
import random


class GetLocation:
    def get_current_location(self):
        # 使用geocoder库获取当前位置信息
        location = geocoder.ip('me')

        # 提取经纬度信息
        latitude, longitude = location.latlng

        return latitude, longitude

    # 随机生成: 半径为radius米范围内的新经纬度
    def generate_random_coordinates_within_circle(self, lat, lon, radius):
        # 地球半径（单位：米）
        R = 6371000

        # 生成随机角度
        random_angle = random.uniform(0, 2 * math.pi)

        # 生成随机半径（在给定半径内）
        random_radius = math.sqrt(random.uniform(0, 1)) * radius

        # 计算纬度的偏移值
        lat_offset = random_radius / R

        # 计算经度的偏移值
        lon_offset = random_radius / (R * math.cos(math.radians(lat)))

        # 新的经纬度
        new_lat = lat + math.degrees(lat_offset)
        new_lon = lon + math.degrees(lon_offset)

        return new_lat, new_lon
