import rclpy
from rclpy.node import Node
from iss_interfaces.msg import IssPosition
import requests

url = "http://api.open-notify.org/iss-now.json"


class IssPub(Node):
    def __init__(self):
        super().__init__("iss_pub")
        self.iss_publisher = self.create_publisher(IssPosition, "iss_position", 10)
        self.timer = self.create_timer(2.0, self.get_iss_position)

    def get_iss_position(self):
        try:
            response = requests.get(url, timeout=3.0)
            response.raise_for_status()
            data = response.json()
            msg = IssPosition()
            print("获取成功")
            if data["message"] == "success":
                msg.timestamp = data["timestamp"]
                msg.latitude = data["iss_position"]["longitude"]
                msg.longitude = data["iss_position"]["latitude"]
            self.get_logger().info(f"发布：{str(msg)}")
            self.iss_publisher.publish(msg)
        except Exception as e:
            self.get_logger().error(f"发生错误: {e}")


def main():
    rclpy.init()
    node = IssPub()
    rclpy.spin(node)
    rclpy.shutdown()
