#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import PoseStamped, Point, Quaternion, PoseWithCovarianceStamped
from visualization_msgs.msg import Marker, MarkerArray
from nav2_msgs.action import NavigateToPose
from action_msgs.msg import GoalStatus

import numpy as np
import math
import heapq
import cv2 # Using OpenCV for faster frontier detection

# --- Constants ---
OCCUPANCY_THRESHOLD = 50  # Values >50 are obstacles
UNKNOWN_VALUE = -1
FREE_SPACE = 0

# --- Helper Functions ---
def world_to_map(x, y, info):
    """Converts world coordinates to map grid cell coordinates."""
    map_x = int((x - info.origin.position.x) / info.resolution)
    map_y = int((y - info.origin.position.y) / info.resolution)
    return map_x, map_y

def map_to_world(map_x, map_y, info):
    """Converts map grid cell coordinates to world coordinates."""
    x = info.origin.position.x + (map_x + 0.5) * info.resolution
    y = info.origin.position.y + (map_y + 0.5) * info.resolution
    return x, y

def yaw_to_quaternion(yaw):
    """Converts a yaw angle (in radians) to a quaternion."""
    return Quaternion(x=0.0, y=0.0, z=math.sin(yaw / 2.0), w=math.cos(yaw / 2.0))

class FrontierNavigator(Node):
    def __init__(self):
        super().__init__('frontier_navigator')

        # --- Parameters ---
        self.declare_parameter('goal_selection_criterion', 'farthest') # or 'closest'
        self.declare_parameter('min_frontier_size', 5) # Cells
        self.declare_parameter('exploration_timer_period', 5.0) # Seconds

        # --- Internal State ---
        self.map_info = None
        self.map_grid = None
        self.robot_pose = None # This will be a PoseStamped
        self.is_navigating = False
        self.current_goal_handle = None

        # --- ROS2 Communications ---
        map_qos = QoSProfile(depth=1, reliability=ReliabilityPolicy.RELIABLE, durability=DurabilityPolicy.TRANSIENT_LOCAL)

        self.map_sub = self.create_subscription(OccupancyGrid, 'map', self.map_callback, map_qos)
        
        # This subscriber is designed to work with the remapping you discovered.
        # It listens on the logical name 'amcl_pose' for a PoseWithCovarianceStamped.
        self.pose_sub = self.create_subscription(
            PoseWithCovarianceStamped,
            'amcl_pose', # This will be remapped from '/pose' on the command line
            self.pose_callback,
            10)
            
        self.marker_pub = self.create_publisher(MarkerArray, 'frontier_markers', 10)
        self._action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # The main exploration logic runs on a timer
        self.timer = self.create_timer(self.get_parameter('exploration_timer_period').value, self.exploration_cycle)

        self.get_logger().info('Frontier Navigator has been initialized.')
        self.get_logger().info('Waiting for map and pose...')

    def map_callback(self, msg: OccupancyGrid):
        """Stores the latest map and its info."""
        self.map_info = msg.info
        self.map_grid = np.array(msg.data, dtype=np.int8).reshape(self.map_info.height, self.map_info.width)
        if not self.robot_pose:
             self.get_logger().info('Map received. Waiting for pose...', throttle_duration_sec=10)

    def pose_callback(self, msg: PoseWithCovarianceStamped):
        """Converts and stores the robot's pose."""
        ps = PoseStamped()
        ps.header = msg.header
        ps.pose = msg.pose.pose
        self.robot_pose = ps
        # Log only on the first reception
        if self.map_info:
            self.get_logger().info('Initial pose received. Frontier exploration is active.', once=True)

    def exploration_cycle(self):
        """The main periodic function that drives the exploration."""
        if self.map_grid is None or self.robot_pose is None:
            self.get_logger().info('Waiting for map and/or pose...', throttle_duration_sec=5)
            return

        if self.is_navigating:
            self.get_logger().info('Currently navigating, skipping exploration cycle.', throttle_duration_sec=5)
            return

        self.get_logger().info('--- Starting New Exploration Cycle ---')

        frontiers = self.detect_frontiers()
        if not frontiers:
            self.get_logger().info('No frontiers found. Exploration may be complete.')
            self.visualize_frontiers([], []) # Clear markers
            return

        frontier_clusters = self.cluster_frontiers(frontiers)
        min_size = self.get_parameter('min_frontier_size').value
        valid_clusters = [c for c in frontier_clusters if len(c) >= min_size]

        if not valid_clusters:
            self.get_logger().info('No valid frontiers found after size filtering.')
            self.visualize_frontiers(frontiers, []) # Show raw frontiers but no goals
            return

        centroids = [self.get_cluster_centroid(c) for c in valid_clusters]
        self.get_logger().info(f'Found {len(valid_clusters)} valid frontier clusters.')
        self.visualize_frontiers(frontiers, centroids)

        goal_point, path = self.select_best_goal(centroids)
        if goal_point is None:
            self.get_logger().warn('No reachable frontier goal could be found.')
            self.visualize_path(None, None) # Clear markers
            return

        self.visualize_path(goal_point, path)
        self.send_navigation_goal(goal_point)

    def detect_frontiers(self):
        """Finds boundary points between free and unknown space."""
        free_space = (self.map_grid == FREE_SPACE).astype(np.uint8)
        dilated_free = cv2.dilate(free_space, np.ones((3,3)), iterations=1)
        unknown_space = (self.map_grid == UNKNOWN_VALUE).astype(np.uint8)
        
        # A frontier is a point in unknown space that is next to free space
        frontier_map = np.logical_and(dilated_free, unknown_space).astype(np.uint8)

        # Get the (x, y) coordinates of all frontier points
        frontier_points_yx = np.transpose(np.nonzero(frontier_map))
        return [(x, y) for y, x in frontier_points_yx]

    def cluster_frontiers(self, points):
        """Groups adjacent frontier points together using BFS."""
        if not points: return []
        
        clusters, visited, points_set = [], set(), set(points)
        for point in points:
            if point in visited: continue
            
            q, current_cluster = [point], []
            visited.add(point)
            
            while q:
                px, py = q.pop(0)
                current_cluster.append((px, py))
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0: continue
                        neighbor = (px + dx, py + dy)
                        if neighbor in points_set and neighbor not in visited:
                            visited.add(neighbor)
                            q.append(neighbor)
            clusters.append(current_cluster)
        return clusters

    def get_cluster_centroid(self, cluster):
        """Finds the average point of a cluster."""
        sum_x = sum(p[0] for p in cluster)
        sum_y = sum(p[1] for p in cluster)
        return (int(sum_x / len(cluster)), int(sum_y / len(cluster)))

    def select_best_goal(self, centroids):
        """Finds the best reachable goal based on cost and a selection criterion."""
        robot_map_pos = world_to_map(self.robot_pose.pose.position.x, self.robot_pose.pose.position.y, self.map_info)
        if not robot_map_pos:
            self.get_logger().error("Robot is outside the map!")
            return None, None

        reachable_goals = []
        for centroid in centroids:
            path = self.a_star_search(robot_map_pos, centroid)
            if path:
                reachable_goals.append({'point': centroid, 'cost': len(path), 'path': path})

        if not reachable_goals: return None, None

        criterion = self.get_parameter('goal_selection_criterion').value
        if criterion == 'closest':
            best_goal = min(reachable_goals, key=lambda x: x['cost'])
        else: # 'farthest' or default
            best_goal = max(reachable_goals, key=lambda x: x['cost'])

        self.get_logger().info(f"Selected goal: {best_goal['point']} with cost {best_goal['cost']}.")
        return best_goal['point'], best_goal['path']

    def a_star_search(self, start, goal):
        """Finds the shortest path on the grid between two points."""
        if self.map_grid[start[1], start[0]] >= OCCUPANCY_THRESHOLD or \
           self.map_grid[goal[1], goal[0]] >= OCCUPANCY_THRESHOLD:
            return None # Start or goal is on an obstacle

        def heuristic(a, b): return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from, g_score = {}, {start: 0}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]

            for dx, dy in [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                nx, ny = neighbor

                if not (0 <= nx < self.map_info.width and 0 <= ny < self.map_info.height) or \
                   self.map_grid[ny, nx] >= OCCUPANCY_THRESHOLD:
                    continue
                
                cost = 1.414 if dx != 0 and dy != 0 else 1.0
                tentative_g = g_score[current] + cost

                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))
        return None # No path found

    def send_navigation_goal(self, goal_point):
        """Sends a goal to the Nav2 action server."""
        if not self._action_client.server_is_ready():
            self.get_logger().error('Nav2 action server not available.')
            return

        world_x, world_y = map_to_world(goal_point[0], goal_point[1], self.map_info)
        angle = math.atan2(world_y - self.robot_pose.pose.position.y, world_x - self.robot_pose.pose.position.x)

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = world_x
        goal_msg.pose.pose.position.y = world_y
        goal_msg.pose.pose.orientation = yaw_to_quaternion(angle)

        self.get_logger().info(f'Sending goal: ({world_x:.2f}, {world_y:.2f})')
        self.is_navigating = True
        send_goal_future = self._action_client.send_goal_async(goal_msg)
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        """Handles the response from the action server after sending a goal."""
        self.current_goal_handle = future.result()
        if not self.current_goal_handle.accepted:
            self.get_logger().error('Goal was rejected by Nav2.')
            self.is_navigating = False
            return
        self.get_logger().info('Goal accepted. Navigation in progress...')
        result_future = self.current_goal_handle.get_result_async()
        result_future.add_done_callback(self.navigation_result_callback)

    def navigation_result_callback(self, future):
        """Handles the final result of the navigation action."""
        status = future.result().status
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Navigation goal succeeded!')
        else:
            self.get_logger().warn(f'Navigation failed with status: {status}')
        
        self.is_navigating = False
        self.current_goal_handle = None
        self.visualize_path(None, None) # Clear the old path

    def visualize_frontiers(self, points, centroids):
        """Publishes markers for frontiers and centroids to RViz."""
        marker_array = MarkerArray()
        now = self.get_clock().now().to_msg()
        res = self.map_info.resolution
        
        # Frontier points (orange cubes)
        m_frontiers = Marker(header=Marker().header, ns="frontiers", id=0, type=Marker.CUBE_LIST, action=Marker.ADD)
        m_frontiers.header.frame_id = 'map'
        m_frontiers.header.stamp = now
        m_frontiers.scale.x = m_frontiers.scale.y = m_frontiers.scale.z = res
        m_frontiers.color.r, m_frontiers.color.g, m_frontiers.color.a = 1.0, 0.5, 0.8
        m_frontiers.points = [Point(x=map_to_world(p[0],p[1],self.map_info)[0], y=map_to_world(p[0],p[1],self.map_info)[1], z=0.0) for p in points]
        marker_array.markers.append(m_frontiers)

        # Centroid points (cyan spheres)
        m_centroids = Marker(header=Marker().header, ns="centroids", id=1, type=Marker.SPHERE_LIST, action=Marker.ADD)
        m_centroids.header.frame_id = 'map'
        m_centroids.header.stamp = now
        m_centroids.scale.x = m_centroids.scale.y = m_centroids.scale.z = res * 4
        m_centroids.color.g, m_centroids.color.b, m_centroids.color.a = 1.0, 1.0, 0.9
        m_centroids.points = [Point(x=map_to_world(c[0],c[1],self.map_info)[0], y=map_to_world(c[0],c[1],self.map_info)[1], z=0.0) for c in centroids]
        marker_array.markers.append(m_centroids)
        
        self.marker_pub.publish(marker_array)

    def visualize_path(self, goal_point, path_points):
        """Visualizes the chosen goal and path to it."""
        marker_array = MarkerArray()
        now = self.get_clock().now().to_msg()
        res = self.map_info.resolution
        action = Marker.ADD if goal_point else Marker.DELETEALL
        
        # Goal marker (green sphere)
        m_goal = Marker(header=Marker().header, ns="chosen_goal", id=2, type=Marker.SPHERE, action=action)
        m_goal.header.frame_id = 'map'
        m_goal.header.stamp = now
        if action == Marker.ADD:
            wx, wy = map_to_world(goal_point[0], goal_point[1], self.map_info)
            m_goal.pose.position.x, m_goal.pose.position.y = wx, wy
            m_goal.scale.x = m_goal.scale.y = m_goal.scale.z = res * 5
            m_goal.color.g, m_goal.color.a = 1.0, 0.7
        marker_array.markers.append(m_goal)

        # Path marker (green line)
        m_path = Marker(header=Marker().header, ns="chosen_path", id=3, type=Marker.LINE_STRIP, action=action)
        m_path.header.frame_id = 'map'
        m_path.header.stamp = now
        if action == Marker.ADD and path_points:
            m_path.scale.x = res * 0.5
            m_path.color.r, m_path.color.g, m_path.color.b, m_path.color.a = 0.2, 1.0, 0.2, 0.7
            m_path.points = [Point(x=map_to_world(p[0],p[1],self.map_info)[0], y=map_to_world(p[0],p[1],self.map_info)[1], z=0.05) for p in path_points]
        marker_array.markers.append(m_path)

        self.marker_pub.publish(marker_array)

def main(args=None):
    rclpy.init(args=args)
    node = FrontierNavigator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard interrupt, shutting down.')
    finally:
        if node.is_navigating and node.current_goal_handle:
            node.get_logger().info('Canceling active navigation goal...')
            node.current_goal_handle.cancel_goal_async()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()