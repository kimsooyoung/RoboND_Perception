#!/usr/bin/env python3

# Import modules
from pcl_helper import *

# TODO: Define functions as required
is_save = False
save_flag = True

# Callback function for your Point Cloud Subscriber
def pcl_callback(pcl_msg):

    # TODO: Convert ROS msg to PCL data
    pcl_data = ros_to_pcl(pcl_msg)

    ####### save pcl for experiment
    #
    # global save_flag
    # if save_flag is True:
    #     print("save save")
    #     pcl.save(pcl_data, "rostopic_to_pcd.pcd")
    #     save_flag = False
    #
    ##############################

    # TODO: Voxel Grid Downsampling
    vox = pcl_data.make_voxel_grid_filter()
    
    LEAF_SIZE = 0.01
    vox.set_leaf_size(LEAF_SIZE, LEAF_SIZE, LEAF_SIZE)
    cloud_filtered = vox.filter()

    # TODO: PassThrough Filter
    passthrough = cloud_filtered.make_passthrough_filter()
    filter_axis = 'z'
    passthrough.set_filter_field_name(filter_axis)
    
    axis_min = 0.76
    axis_max = 1.1
    passthrough.set_filter_limits(axis_min, axis_max)
    
    cloud_filtered = passthrough.filter()

    # TODO: RANSAC Plane Segmentation
    seg = cloud_filtered.make_segmenter()
    seg.set_model_type(pcl.SACMODEL_PLANE)
    seg.set_method_type(pcl.SAC_RANSAC)

    max_distance = 0.01
    seg.set_distance_threshold(max_distance)
    inliers, coefficients = seg.segment()

    # TODO: Extract inliers and outliers
    objectd_cloud = cloud_filtered.extract(inliers, negative=True)
    table_cloud = cloud_filtered.extract(inliers, negative=False)

    ######################################
    # TODO: Euclidean Clustering
    # Apply function to convert XYZRGB to XYZ
    white_cloud = XYZRGB_to_XYZ(objectd_cloud) 
    tree = white_cloud.make_kdtree()

    # Create a cluster extraction object
    ec = white_cloud.make_EuclideanClusterExtraction()
    # Set tolerances for distance threshold 
    # as well as minimum and maximum cluster size (in points)
    # NOTE: These are poor choices of clustering parameters
    # Your task is to experiment and find values that work for segmenting objects.
    ec.set_ClusterTolerance(0.02)
    ec.set_MinClusterSize(10)
    ec.set_MaxClusterSize(9000)
    # Search the k-d tree for clusters
    ec.set_SearchMethod(tree)
    # Extract indices for each of the discovered clusters
    cluster_indices = ec.Extract()

    # TODO: Create Cluster-Mask Point Cloud to visualize each cluster separately
    #Assign a color corresponding to each segmented object in scene
    cluster_color = get_color_list(len(cluster_indices))

    color_cluster_point_list = []

    for j, indices in enumerate(cluster_indices):
        for i, indice in enumerate(indices):
            color_cluster_point_list.append([white_cloud[indice][0],
                                            white_cloud[indice][1],
                                            white_cloud[indice][2],
                                            rgb_to_float(cluster_color[j])])

    #Create new cloud containing all clusters, each with unique color
    cluster_cloud = pcl.PointCloud_PointXYZRGB()
    cluster_cloud.from_list(color_cluster_point_list)

    # TODO: Publish ROS messages
    ######################################

    # TODO: Convert PCL data to ROS messages
    objectd_cloud_msg = pcl_to_ros(objectd_cloud)
    table_cloud_msg = pcl_to_ros(table_cloud)
    ros_cluster_cloud = pcl_to_ros(cluster_cloud)

    pcl_objects_pub.publish(objectd_cloud_msg)
    pcl_table_pub.publish(table_cloud_msg)
    pcl_cluster_pub.publish(ros_cluster_cloud)


if __name__ == '__main__':

    # TODO: ROS node initialization
    rospy.init_node("pcl_seg_node")

    # TODO: Create Subscribers
    pcl_sub = rospy.Subscriber("/sensor_stick/point_cloud", pc2.PointCloud2, pcl_callback, queue_size=1)

    # TODO: Create Publishers
    pcl_objects_pub = rospy.Publisher("/pcl_objects", PointCloud2, queue_size=1)
    pcl_table_pub = rospy.Publisher("/pcl_table", PointCloud2, queue_size=1)
    pcl_cluster_pub = rospy.Publisher("/pcl_cluster", PointCloud2, queue_size=1)

    # Initialize color_list
    get_color_list.color_list = []

    # TODO: Spin while node is not shutdown
    rospy.spin()

