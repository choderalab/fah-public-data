import numpy as np
import os
from glob import glob
import sys


def get_trajectories_to_upload(path, indexes_file_name="sub_longer250ns_indexes.npy"):
    trajs = sorted(
        [
            traj
            for proj in ["11743", "11749"]
            for traj in glob(os.path.join(path, proj, "*.h5"))
        ]
    )
    indexes = np.load(os.path.join(path, indexes_file_name))
    return list(np.array(trajs)[indexes])


if __name__ == "__main__":
    path = './' if len(sys.argv) < 2 else sys.argv[1]
    print('\n'.join(get_trajectories_to_upload(path)))
