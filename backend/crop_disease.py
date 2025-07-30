import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# ✅ Set Dataset Paths
BASE_DIR = os.path.abspath(r"C:\Users\soumy\OneDrive\Desktop\TY\HACKATHONS\VESIT\backend\dataset")
TRAIN_DIR = os.path.join(BASE_DIR, "Train")
VALIDATION_DIR = os.path.join(BASE_DIR, "Validation")
TEST_DIR = os.path.join(BASE_DIR, "Test")

# ✅ Ensure dataset folders exist
for directory in [TRAIN_DIR, VALIDATION_DIR, TEST_DIR]:
    if not os.path.exists(directory):
        raise FileNotFoundError(f"❌ Error: Directory {directory} not found!")

# ✅ Image Size, Batch Size, and Hyperparameters
IMG_SIZE = (224, 224)  # ✅ FIXED: MobileNetV2 only supports specific sizes
BATCH_SIZE = 16
EPOCHS = 20
LEARNING_RATE = 0.0005

# ✅ Print Dataset Info
print(f"📂 Train Path: {TRAIN_DIR}")
print(f"📂 Validation Path: {VALIDATION_DIR}")
print(f"📂 Test Path: {TEST_DIR}")

# ✅ Data Augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.3,
    brightness_range=[0.7, 1.3],
    horizontal_flip=True,
    fill_mode="nearest"
)

validation_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

# ✅ Load Data
train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode='categorical'
)
validation_generator = validation_datagen.flow_from_directory(
    VALIDATION_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode='categorical'
)
test_generator = test_datagen.flow_from_directory(
    TEST_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode='categorical'
)

# ✅ Print Class Indices
print("📌 Class Indices:", train_generator.class_indices)

# ✅ Load Pretrained MobileNetV2 Model
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# ✅ Add Custom Layers
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(256, activation='relu')(x)  # Hidden layer with 256 neurons
x = Dropout(0.3)(x)  # Prevents overfitting
x = Dense(128, activation='relu')(x)
x = Dropout(0.2)(x)
output = Dense(3, activation='softmax')(x)  # Output layer (Healthy, Powdery, Rust)

# ✅ Build Model
model = Model(inputs=base_model.input, outputs=output)

# ✅ Fine-Tune the Model (Last 10 Layers)
for layer in base_model.layers[:-10]:  # Unfreeze last 10 layers
    layer.trainable = False

# ✅ Compile Model
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# ✅ Callbacks for Early Stopping & Best Model Saving
checkpoint = ModelCheckpoint("best_model.keras", monitor='val_accuracy', save_best_only=True, verbose=1)  # ✅ FIXED: .h5 ➝ .keras
early_stopping = EarlyStopping(monitor='val_loss', patience=5, verbose=1, restore_best_weights=True)

# ✅ Train Model
history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=validation_generator,
    callbacks=[checkpoint, early_stopping]
)

# ✅ Save Final Model
model.save("final_model.keras")  # ✅ FIXED: Save in `.keras` format
print("✅ Model Training Completed and Saved as final_model.keras")
