#include <rclcpp/rclcpp.hpp>

#include "iss_interfaces/msg/iss_position.hpp"

using IssPos = iss_interfaces::msg::IssPosition;

class IssSub : public rclcpp::Node {
   private:
    rclcpp::Subscription<IssPos>::SharedPtr subscriber_;

   public:
    IssSub() : Node("iss_sub") {
        subscriber_ = this->create_subscription<IssPos>(
            "/iss_position", 10, [&](const IssPos::SharedPtr msg) -> void { RCLCPP_INFO(this->get_logger(), "时间戳：%ld | 经度：%s | 维度：%s", msg->timestamp, msg->latitude.c_str(), msg->longitude.c_str()); });
    }
};

int main(int argc, char* argv[]) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<IssSub>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}