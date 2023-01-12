import pcl
import numpy as np
import pcl.pcl_visualization

def main():
    cloud = pcl.load("tabletop.pcd")

    # Centred the data
    centred = cloud - np.mean(cloud, 0)
    ptcloud_centred = pcl.PointCloud()
    ptcloud_centred.from_array(centred)

    visual = pcl.pcl_visualization.CloudViewing()

    # PointXYZ
    visual.ShowMonochromeCloud(ptcloud_centred, b'cloud')
    v = True
    while v:
        v = not(visual.WasStopped())

if __name__ == "__main__":
    main()
    pass