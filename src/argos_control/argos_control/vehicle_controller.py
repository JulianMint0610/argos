from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node


class VehicleController(Node):

    def __init__(self):
        super().__init__('vehicle_controller')

        self.publisher = self.create_publisher(
            Twist,
            'model/vehicle_blue/cmd_vel',
            10
        )

        self.start_time = self.get_clock().now()
        self.current_phase = None

        self.timer = self.create_timer(
            0.1,
            self.control_vehicle,
        )

        self.get_logger().info(
            'ARGOS autonomous sequence started'
        )

    def control_vehicle(self):
        now = self.get_clock().now()

        elapsed_time = (
            now - self.start_time
        ).nanoseconds / 1_000_000_000

        command = Twist()

        if elapsed_time < 3.0:
            phase = 'FORWARD_1'

            command.linear.x = 1.0
            command.angular.z = 0.0

        elif elapsed_time < 6.0:
            phase = 'TURN_LEFT'

            command.linear.x = 0.5
            command.angular.z = 1.0

        elif elapsed_time < 9.0:
            phase = 'FORWARD_2'

            command.linear.x = 1.0
            command.angular.z = -1.0

        else:
            phase = 'STOP'

            command.linear.x = 0.0
            command.angular.z = 0.0

        if phase != self.current_phase:
            self.current_phase = phase

            self.get_logger().info(
                f'phase: {phase} | '
                f'elapsed: {elapsed_time:.1f}s'
            )

        self.publisher.publish(command)


def main(args=None):
    rclpy.init(args=args)

    node = VehicleController()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        if rclpy.ok():
            stop_command = Twist()
            node.publisher.publish(stop_command)

        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
