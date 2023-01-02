# -*- coding: utf-8 -*-
# port of
# http://pointclouds.org/documentation/tutorials/statistical_outlier.php
# you need to download
# http://svn.pointclouds.org/data/tutorials/table_scene_lms400.pcd

import pcl


def main():
    p = pcl.load("table_scene_lms400.pcd")

    # Much like the previous filters, we start by creating a filter object: 
    fil = p.make_statistical_outlier_filter()
    # Set the number of neighboring points to analyze for any given point
    fil.set_mean_k(50)
    # Any point with a mean distance larger than global (mean distance+x*std_dev) will be considered outlier
    fil.set_std_dev_mul_thresh(1.0)

    # Finally call the filter function for magic
    pcl.save(fil.filter(),"table_scene_lms400_inliers.pcd")

    fil.set_negative(True)
    pcl.save(fil.filter(),"table_scene_lms400_outliers.pcd")


if __name__ == "__main__":
    # import cProfile
    # cProfile.run('main()', sort='time')
    main()