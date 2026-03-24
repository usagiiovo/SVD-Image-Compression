import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# STEP 1: Load the image and convert it to grayscale
# Grayscale means the image is just a 2D matrix of numbers (0-255)
image_path = "my_image.jpg"
img = Image.open(image_path).convert("L")  # L = grayscale
A = np.array(img, dtype=float)/255.0

# Print image size to see the matrix dimensions (height, width)
print("Original image shape:", A.shape)

# STEP 2: Perform SVD (Singular Value Decomposition)
# This splits the matrix A into three parts: U, s, and Vt
# s (singular values) represents the "importance" of information
U, s, Vt = np.linalg.svd(A, full_matrices=False)

# STEP 3: Function to reconstruct the image using only 'k' components
def compress_image(U, s, Vt, k):
    # only take the first k columns of U
    # only take the first k singular values of s
    # only take the first k rows of Vt
    # this is called "Rank-k Approximation"
    compressed_A = (U[:, :k] * s[:k]) @ Vt[:k, :]
    return compressed_A

# STEP 4: Choose different k values to see the effect
# k is the number of "features" we keep. Smaller k = more compression
k_values = [5, 20, 50, 78, 100]

# Create a window to show results side by side
plt.figure(figsize=(20, 5))

# Show original image first
plt.subplot(1, len(k_values) + 1, 1)
plt.imshow(A, cmap='gray')
plt.title("Original")
plt.axis("off")

for i, k in enumerate(k_values):
    reconstructed = compress_image(U, s, Vt, k)
    
    # Calculate relative error
    error = np.linalg.norm(A - reconstructed) / np.linalg.norm(A)

    # Calculate storage ratio ( k*(m+n+1)/(m*n))
    m,n = A.shape
    storage_pct = (k * (m + n + 1)) / (m * n) * 100

    #compression ratio
    compression_ratio = (m * n) / (k * (m + n + 1))

    # print out on terminal
    print(f"k = {k}: Error = {error*100:.2f}% , Storage Used = {storage_pct:.2f}%, CR ≈ {compression_ratio:.1f}:1")

    # Show compressed versions
    plt.subplot(1, len(k_values) + 1, i + 2)
    plt.imshow(reconstructed, cmap='gray')
    plt.title(f"k = {k} (Err: {error:.1%})")
    plt.axis("off")

plt.tight_layout()
plt.savefig("result.png", dpi=200)
plt.show()
