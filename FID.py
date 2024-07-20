# import subprocess
#
# dataset1_path = "Data_Screw/public resources screw icons/public FID"
# dataset2_path = "Data_Screw/public resources screw icons/screws_public_resources_long_prompt/inference FID"
#
#
# output_file = "FID_screw.txt"
#
#
# batch_size = 7  # can adjust this value
#
#
# command = f'python -m pytorch_fid "{dataset1_path}" "{dataset2_path}" --batch-size {batch_size}'
# result = subprocess.run(command, shell=True, capture_output=True, text=True)
#
#
# print("STDOUT:", result.stdout)
# print("STDERR:", result.stderr)
#
#
# with open(output_file, 'a') as f:
#     f.write(f"public data long prompt FID score: {result.stdout.strip()}\n")

############ Above code will cause error when run with public data, because public data has a lot of differenent size
# and format icon images, so rewrite the code#####################



import os
from PIL import Image
import numpy as np
from scipy import linalg
from pytorch_fid.inception import InceptionV3
from pytorch_fid.fid_score import compute_statistics_of_path



def resize_images_in_directory(directory, size=(256, 256)):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('jpg', 'jpeg', 'png')):
                img_path = os.path.join(root, file)
                try:
                    with Image.open(img_path) as img:
                        img_resized = img.resize(size)
                        img_resized.save(img_path)
                except Exception as e:
                    print(f"Error processing {img_path}: {e}")



def check_images_for_nan_inf(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('jpg', 'jpeg', 'png')):
                img_path = os.path.join(root, file)
                try:
                    with Image.open(img_path) as img:
                        img_array = np.array(img)
                        if np.isnan(img_array).any() or np.isinf(img_array).any():
                            print(f"Invalid values in {img_path}")
                except Exception as e:
                    print(f"Error reading {img_path}: {e}")


# function to calculate Frechet distance
def calculate_frechet_distance(mu1, sigma1, mu2, sigma2, eps=1e-6):

    mu1 = np.atleast_1d(mu1)
    mu2 = np.atleast_1d(mu2)

    sigma1 = np.atleast_2d(sigma1)
    sigma2 = np.atleast_2d(sigma2)

    assert mu1.shape == mu2.shape, \
        'Training and test mean vectors have different lengths'
    assert sigma1.shape == sigma2.shape, \
        'Training and test covariances have different dimensions'

    diff = mu1 - mu2


    covmean, _ = linalg.sqrtm(sigma1.dot(sigma2), disp=False)
    if not np.isfinite(covmean).all():
        msg = ('fid calculation produces singular product; '
               'adding %s to diagonal of cov estimates') % eps
        print(msg)
        offset = np.eye(sigma1.shape[0]) * eps
        covmean = linalg.sqrtm((sigma1 + offset).dot(sigma2 + offset))

    # Numerical error might give slight imaginary component
    if np.iscomplexobj(covmean):
        print(f"Covariance mean has imaginary component, making real: {np.trace(covmean)}")
        covmean = covmean.real

    tr_covmean = np.trace(covmean)

    print(f"Means: {mu1}, {mu2}")
    print(f"Covariances: {sigma1}, {sigma2}")
    print(f"Trace of product of covariances: {tr_covmean}")

    return (diff.dot(diff) + np.trace(sigma1) +
            np.trace(sigma2) - 2 * tr_covmean)



def calculate_fid_given_paths(paths, batch_size, device, dims, num_workers):
    block_idx = InceptionV3.BLOCK_INDEX_BY_DIM[dims]
    model = InceptionV3([block_idx]).to(device)

    for path in paths:
        num_images = len(os.listdir(path))
        adjusted_batch_size = min(batch_size, num_images)
        if adjusted_batch_size == 0:
            raise ValueError(f"No images found in directory: {path}")

        if num_images < batch_size:
            print(f"Warning: batch size is bigger than the data size. Setting batch size to data size: {num_images}")

        m, s = compute_statistics_of_path(path, model, adjusted_batch_size, dims, device, num_workers)
        yield m, s

def main():
    dataset1_path = "Data_Screw/home depot data/home depot FID"
    dataset2_path = "DALL.E/inference FID"

    resize_images_in_directory(dataset1_path)
    resize_images_in_directory(dataset2_path)
    check_images_for_nan_inf(dataset1_path)
    check_images_for_nan_inf(dataset2_path)


    paths = [dataset1_path, dataset2_path]
    batch_size = 7  # can adjust this value

    m1, s1 = next(calculate_fid_given_paths([paths[0]], batch_size, 'cpu', 2048, 8))
    m2, s2 = next(calculate_fid_given_paths([paths[1]], batch_size, 'cpu', 2048, 8))

    fid_value = calculate_frechet_distance(m1, s1, m2, s2)
    print(f"FID Value: {fid_value}")


    output_file = "FID_screw.txt"
    with open(output_file, 'a') as f:
        f.write(f"Dalle FID score: {fid_value}\n")


if __name__ == '__main__':
    main()
