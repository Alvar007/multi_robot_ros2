import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import math

class FollowerNode(Node):

    def __init__(self):
        super().__init__('follower_node')

        # Subscripciones
        self.sub_leader = self.create_subscription(
            Odometry,
            '/tb3_0/odom',
            self.leader_callback,
            10)

        self.sub_follower = self.create_subscription(
            Odometry,
            '/odom',
            self.follower_callback,
            10)

        # Publicador de velocidad
        self.pub_cmd = self.create_publisher(Twist, '/cmd_vel', 10)

        self.leader_pose = None
        self.follower_pose = None

        # Parámetros
        self.desired_distance = 0.5
        self.k_linear = 0.8
        self.k_angular = 2.0

    def leader_callback(self, msg):
        self.leader_pose = msg.pose.pose
        self.control_loop()

    def follower_callback(self, msg):
        self.follower_pose = msg.pose.pose
        self.control_loop()

    def control_loop(self):
        if self.leader_pose is None or self.follower_pose is None:
            return

        # Posiciones
        lx = self.leader_pose.position.x
        ly = self.leader_pose.position.y

        fx = self.follower_pose.position.x
        fy = self.follower_pose.position.y

        # Diferencias
        dx = lx - fx
        dy = ly - fy

        distance = math.sqrt(dx**2 + dy**2)

        # Ángulo hacia el líder
        target_angle = math.atan2(dy, dx)

        # Orientación actual del follower
        q = self.follower_pose.orientation
        yaw = self.quaternion_to_yaw(q)

        angle_error = self.normalize_angle(target_angle - yaw)

        # Control
        cmd = Twist()

        # Control lineal con zona muerta
        if distance > self.desired_distance:
            cmd.linear.x = self.k_linear * (distance - self.desired_distance)
        else:
            cmd.linear.x = 0.0

        cmd.angular.z = self.k_angular * angle_error

        self.pub_cmd.publish(cmd)

    def quaternion_to_yaw(self, q):
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
        return math.atan2(siny_cosp, cosy_cosp)

    def normalize_angle(self, angle):
        while angle > math.pi:
            angle -= 2.0 * math.pi
        while angle < -math.pi:
            angle += 2.0 * math.pi
        return angle


def main():
    rclpy.init()
    node = FollowerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
