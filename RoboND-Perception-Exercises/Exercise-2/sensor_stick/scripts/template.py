#!/usr/bin/env python

# Import modules
from pcl_helper import *

# TODO: Define functions as required

# Callback function for your Point Cloud Subscriber
def pcl_callback(pcl_msg):

    # TODO: Convert ROS msg to PCL data
    pcl_data = ros_to_pcl(pcl_msg)

    # TODO: Voxel Grid Downsampling
    vox = pcl_data.make_voxel_grid_filter()
    
    LEAF_SIZE = 0.01
    vox.set_leaf_size(LEAF_SIZE, LEAF_SIZE, LEAF_SIZE)
    cloud_filtered = vox.filter()

    # TODO: PassThrough Filter
    passthrough = cloud_filtered.make_passthrough_filter()
    filter_axis = 'z'
    passthrough.set_filter_field_name(filter_axis)
    
    axis_min = 0.6
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
    extracted_inliers = cloud_filtered.extract(inliers, negative=True)

    ######################################
    # TODO: Euclidean Clustering
    max_distance = 1
    db = DBSCAN(eps=max_distance, min_samples=10).fit(extracted_inliers)

    # TODO: Create Cluster-Mask Point Cloud to visualize each cluster separately
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True

    labels = db.labels_
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    unique_labels = set(labels)

    # TODO: Convert PCL data to ROS messages
    pcl_ros_msg = pcl_to_ros(unique_labels)

    # TODO: Publish ROS messages
    pcl_pub.publish()


if __name__ == '__main__':

    # TODO: ROS node initialization
    rospy.init_node("pcl_seg_node")

    # TODO: Create Subscribers
    pcl_sub = rospy.Subscriber()

    # TODO: Create Publishers
    pcl_pub = rospy.Publisher()

    # Initialize color_list
    get_color_list.color_list = []

    # TODO: Spin while node is not shutdown
    rospy.spin()

