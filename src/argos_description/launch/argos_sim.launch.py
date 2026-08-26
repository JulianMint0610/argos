import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.actions import SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():
    argos_description = get_package_share_directory(
        'argos_description'
    )

    ros_gz_sim = get_package_share_directory(
        'ros_gz_sim'
    )

    world_path = os.path.join(
        argos_description,
        'worlds',
        'argos_world.sdf',
    )

    model_path = os.path.join(
        argos_description,
        'models',
    )

    existing_resource_path = os.environ.get(
        'GZ_SIM_RESOURCE_PATH',
        '',
    )

    if existing_resource_path:
        resource_path = (
            model_path
            + os.pathsep
            + existing_resource_path
        )
    else:
        resource_path = model_path

    
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                ros_gz_sim,
                'launch',
                'gz_sim.launch.py',
            )
        ),
        launch_arguments={
            'gz_args' : f' -r {world_path}',
        }.items(),
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
                '/model/vehicle_blue/cmd_vel'
                '@geometry_msgs/msg/Twist'
                '@gz.msgs.Twist',

                '/argos/front_camera/image'
                '@sensor_msgs/msg/Image'
                '@gz.msgs.Image',
                
                '/argos/front_camera/camera_info'
                '@sensor_msgs/msg/CameraInfo'
                '@gz.msgs.CameraInfo',
        ],
        output='screen',
    )

    return LaunchDescription([
        SetEnvironmentVariable(
            'GZ_SIM_RESOURCE_PATH',
            resource_path,
        ),
        gz_sim,
        bridge,
    ])

