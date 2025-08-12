import torch
from PIL import Image
from torchvision import transforms
import torch.nn as nn

class LeNetUltraLight(nn.Module):
    def __init__(self, num_classes=2):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 6, kernel_size=5, padding=2),
            nn.ReLU(inplace=True),
            nn.AvgPool2d(2),
            nn.Conv2d(6, 16, kernel_size=5),
            nn.ReLU(inplace=True),
            nn.AvgPool2d(2),
            nn.AdaptiveAvgPool2d((6, 6))
        )
        self.flatten = nn.Flatten()
        self.classifier = nn.Sequential(
            nn.Linear(16 * 6 * 6, 120),
            nn.ReLU(inplace=True),
            nn.Linear(120, 84),
            nn.ReLU(inplace=True),
            nn.Linear(84, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.flatten(x)
        x = self.classifier(x)
        return x

class ImageClassifier:
    def __init__(self, model_path="lenet_classifier2.pth", device='cpu'):
        self.device = device
        self.num_classes = 2
        self.class_labels = ["clock", "fire_extinguisher"]
        
        # Load model
        self.model = LeNetUltraLight(self.num_classes)
        self.model.load_state_dict(torch.load(model_path, map_location=device))
        self.model.to(device)
        self.model.eval()
        
        # Define transforms
        self.transform = transforms.Compose([
            transforms.Resize((640, 640)),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
    
    def predict(self, image):
        """
        Dự đoán class của ảnh
        
        Args:
            image_path (str): Đường dẫn đến ảnh
            
        Returns:
            str: Tên class được dự đoán
        """
        # Load và preprocess image
        # image = Image.open(image_path).convert("RGB")
        transformed_image = self.transform(image)
        transformed_image = transformed_image.unsqueeze(0).to(self.device)
        
        # Prediction
        with torch.no_grad():
            outputs = self.model(transformed_image)
            _, predicted = torch.max(outputs.data, 1)
        
        predicted_class = self.class_labels[predicted.item()]
        return predicted_class
