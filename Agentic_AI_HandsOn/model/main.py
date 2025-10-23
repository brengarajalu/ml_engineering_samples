import torch

from neural_net import Net
from torchvision.transforms import transforms
from PIL import Image
import argparse

parser = argparse.ArgumentParser(description='Predict class for a given MNIST image using a pre-trained model.')
parser.add_argument('image_path', type=str, help='Path to the input image.')
args = parser.parse_args()
image_path = args.image_path

model = Net()

# Load the saved model parameters
model.load_state_dict(torch.load('mnist_model.pth'))

# Set the model in evaluation mode (important for models with dropout, batch normalization, etc.)
model.eval()

transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
image = Image.open(image_path).convert("L")  # Convert to grayscale
image = transform(image)

image = image.unsqueeze(0)  # Add batch dimension. image shape becomes [1, 1, 28, 28]

with torch.no_grad():
    output = model(image)
    predicted_class = torch.argmax(output, dim=1).item()

print(f"The model predicts the image as class: {predicted_class}")