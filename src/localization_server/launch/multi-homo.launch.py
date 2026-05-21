#!/usr/bin/env python3
#
# Copyright 2019 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors: Darby Lim

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir
from launch.actions import ExecuteProcess
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.substitutions import Command


TURTLEBOT3_MODEL = "burger"

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    world_file_name = 'turtlebot3_tc_two_robots.world'
    world = os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'worlds', world_file_name)
    robot_desc_path = os.path.join(get_package_share_directory("turtlebot3_description"), "urdf", "turtlebot3_burger.urdf")

    entity_name_0="tb3_0"
    entity_name_1="tb3_1"
    
    controller_yaml_0 = os.path.join(get_package_share_directory('path_planner_server'), 'config', 'tb3_0_controller.yaml')
    bt_navigator_yaml_0 = os.path.join(get_package_share_directory('path_planner_server'), 'config', 'tb3_0_bt_navigator.yaml')
    planner_yaml_0 = os.path.join(get_package_share_directory('path_planner_server'), 'config', 'tb3_0_planner_server.yaml')
    recovery_yaml_0 = os.path.join(get_package_share_directory('path_planner_server'), 'config', 'tb3_0_recovery.yaml')
    controller_yaml_1 = os.path.join(get_package_share_directory('path_planner_server'), 'config', 'tb3_1_controller.yaml')
    bt_navigator_yaml_1 = os.path.join(get_package_share_directory('path_planner_server'), 'config', 'tb3_1_bt_navigator.yaml')
    planner_yaml_1 = os.path.join(get_package_share_directory('path_planner_server'), 'config', 'tb3_1_planner_server.yaml')
    recovery_yaml_1 = os.path.join(get_package_share_directory('path_planner_server'), 'config', 'tb3_1_recovery.yaml')

    nav2_yaml_0 = os.path.join(get_package_share_directory(
        'localization_server'), 'config', 'tb3_0_amcl_config.yaml')
    nav2_yaml_1 = os.path.join(get_package_share_directory(
        'localization_server'), 'config', 'tb3_1_amcl_config.yaml')
    map_file = os.path.join(get_package_share_directory(
        'map_server'), 'config', 'turtlebot_area.yaml')   

    rviz_config_dir = os.path.join(get_package_share_directory('localization_server'), 'rviz', 'multi-homo.rviz')

    return LaunchDescription([
        ExecuteProcess(
            cmd=['gazebo', '--verbose', world, '-s', 'libgazebo_ros_init.so'],
            output='screen'),
        
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            namespace=entity_name_0,
            parameters=[{'frame_prefix': entity_name_0+'/', 'use_sim_time': use_sim_time, 'robot_description': Command(['xacro ', robot_desc_path, ' robot_name:=', entity_name_0])}],
            output="screen"
        ),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            namespace=entity_name_1,
            parameters=[{'frame_prefix': entity_name_1+'/', 'use_sim_time': use_sim_time, 'robot_description': Command(['xacro ', robot_desc_path, ' robot_name:=', entity_name_1])}],
            output="screen"
        ),

        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            parameters=[{'use_sim_time': True}, 
                        {'topic_name':"map"},
                        {'frame_id':"map"},
                        {'yaml_filename':map_file}]
        ),

        Node(
            namespace='tb3_0',
            package='nav2_amcl',
            executable='amcl',
            name='amcl',
            output='screen',
            parameters=[nav2_yaml_0]
        ),

        Node(
            namespace='tb3_1',
            package='nav2_amcl',
            executable='amcl',
            name='amcl',
            output='screen',
            parameters=[nav2_yaml_1]
        ),
        
        Node(
            namespace='tb3_0',
            package='nav2_controller',
            executable='controller_server',
            name='controller_server',
            output='screen',
            parameters=[controller_yaml_0]),

        Node(
            namespace='tb3_0',
            package='nav2_planner',
            executable='planner_server',
            name='planner_server',
            output='screen',
            parameters=[planner_yaml_0]),
            
        Node(
            namespace='tb3_0',
            package='nav2_behaviors',
            executable='behavior_server',
            name='recoveries_server',
            parameters=[recovery_yaml_0],
            output='screen'),

        Node(
            namespace='tb3_0',
            package='nav2_bt_navigator',
            executable='bt_navigator',
            name='bt_navigator',
            output='screen',
            parameters=[bt_navigator_yaml_0]),

        Node(
            namespace='tb3_1',
            package='nav2_controller',
            executable='controller_server',
            name='controller_server',
            output='screen',
            parameters=[controller_yaml_1]),

        Node(
            namespace='tb3_1',
            package='nav2_planner',
            executable='planner_server',
            name='planner_server',
            output='screen',
            parameters=[planner_yaml_1]),
            
        Node(
            namespace='tb3_1',
            package='nav2_behaviors',
            executable='behavior_server',
            name='recoveries_server',
            parameters=[recovery_yaml_1],
            output='screen'),

        Node(
            namespace='tb3_1',
            package='nav2_bt_navigator',
            executable='bt_navigator',
            name='bt_navigator',
            output='screen',
            parameters=[bt_navigator_yaml_1]),

        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_localization',
            output='screen',
            parameters=[{'use_sim_time': True},
                        {'autostart': True},
                        {'bond_timeout':0.0},
                        {'node_names': ['map_server', 'tb3_0/amcl', 'tb3_1/amcl', 'tb3_0/planner_server',
                                        'tb3_0/controller_server',
                                        'tb3_0/recoveries_server',
                                        'tb3_0/bt_navigator',
                                        'tb3_1/planner_server',
                                        'tb3_1/controller_server',
                                        'tb3_1/recoveries_server',
                                        'tb3_1/bt_navigator']}]
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_dir],
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen'),
    ])
