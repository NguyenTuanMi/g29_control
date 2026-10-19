"""
Drive the ego vehicle with a Logitech G29 wheel and optionally log the
driven route to a CSV.

Requires the ROS 2 `joy` package (apt/rosdep) to read the wheel's HID
reports, and a CARLA ego vehicle already spawned under the given role_name
(see sim_bringup's ego_vehicle.launch.py).

  ros2 launch g29_control manual_recording.launch.py
  ros2 launch g29_control manual_recording.launch.py role_name:=ego_vehicle \
      output_file:=/tmp/my_route.csv
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    role_name_arg = DeclareLaunchArgument(
        'role_name',
        default_value='hero',
        description='Role name of the ego vehicle in CARLA'
    )

    steer_axis_arg = DeclareLaunchArgument('steer_axis', default_value='0')
    throttle_axis_arg = DeclareLaunchArgument('throttle_axis', default_value='2')
    brake_axis_arg = DeclareLaunchArgument('brake_axis', default_value='3')

    output_file_arg = DeclareLaunchArgument(
        'output_file',
        default_value='route.csv',
        description='Absolute or relative path to save the logged route CSV'
    )

    # Standard joy node to read the physical wheel/pedals.
    joy_node = Node(
        package='joy',
        executable='joy_node',
        name='joy_node',
        parameters=[{
            'device_id': 0
        }],
        output='screen'
    )

    # Maps G29 raw axes/buttons to CarlaEgoVehicleControl.
    g29_mapping_node = Node(
        package='g29_control',
        executable='g29_to_carla',
        name='g29_to_carla_node',
        parameters=[{
            'role_name': LaunchConfiguration('role_name'),
            'steer_axis': LaunchConfiguration('steer_axis'),
            'throttle_axis': LaunchConfiguration('throttle_axis'),
            'brake_axis': LaunchConfiguration('brake_axis'),
        }],
        output='screen'
    )

    # Optional: logs odometry to a CSV while driving.
    route_logger_node = Node(
        package='g29_control',
        executable='route_logger',
        name='route_logger_node',
        parameters=[{
            'role_name': LaunchConfiguration('role_name'),
            'output_file': LaunchConfiguration('output_file')
        }],
        output='screen'
    )

    return LaunchDescription([
        role_name_arg,
        steer_axis_arg,
        throttle_axis_arg,
        brake_axis_arg,
        output_file_arg,
        joy_node,
        g29_mapping_node,
        route_logger_node
    ])
