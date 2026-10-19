import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import csv
import math
import os

class RouteLoggerNode(Node):
    def __init__(self):
        super().__init__('route_logger_node')
        
        # Parameters
        self.declare_parameter('role_name', 'hero')
        self.declare_parameter('output_file', 'reference_trajectory.csv')
        
        role_name = self.get_parameter('role_name').get_parameter_value().string_value
        self.output_file = self.get_parameter('output_file').get_parameter_value().string_value
        
        # Setup CSV
        file_exists = os.path.isfile(self.output_file)
        self.csv_file = open(self.output_file, mode='a', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        
        if not file_exists:
            self.csv_writer.writerow(['timestamp', 'x', 'y', 'yaw', 'velocity'])
            
        # Subscriber
        topic_name = f'/carla/{role_name}/odometry'
        self.subscription = self.create_subscription(
            Odometry,
            topic_name,
            self.odom_callback,
            10)
            
        self.get_logger().info(f'Logging route data from {topic_name} to {self.output_file}')

    def odom_callback(self, msg):
        # Extract timestamp
        sec = msg.header.stamp.sec
        nanosec = msg.header.stamp.nanosec
        timestamp = sec + (nanosec / 1e9)
        
        # Position
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        
        # Orientation (Quaternion to Yaw/Psi)
        q = msg.pose.pose.orientation
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
        yaw = math.atan2(siny_cosp, cosy_cosp)
        
        # Velocity magnitude
        vx = msg.twist.twist.linear.x
        vy = msg.twist.twist.linear.y
        vz = msg.twist.twist.linear.z
        v = math.sqrt(vx**2 + vy**2 + vz**2)
        
        # Log to CSV
        self.csv_writer.writerow([timestamp, x, y, yaw, v])

    def destroy_node(self):
        self.csv_file.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = RouteLoggerNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Route logging stopped by user.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()