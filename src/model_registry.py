import argparse
import json
import os
from joblib import dump, load
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

MODEL_DIR = "models"
METADATA_DIR = "metadata"

def get_next_version(model_name):
    """Determine the next version number for a given model."""
    versions = [0]
    for file in os.listdir(METADATA_DIR):
        if file.startswith(model_name):
            version = int(file.split('_v')[-1].split('.')[0])
            versions.append(version)
    return max(versions) + 1

def register(model, features, metadata):
    """Register a new model and its metadata."""
    version = get_next_version(metadata['name'])
    model_file_name = f"{metadata['name']}_model_v{version}.joblib"
    features_file_name = f"{metadata['name']}_features_v{version}.joblib"
    metadata['version'] = version
    metadata['registration_date'] = datetime.now().isoformat()
    
    # Save model
    model_path = os.path.join(MODEL_DIR, model_file_name)
    dump(model, model_path)
    metadata['model'] = model_file_name
    
    features_path = os.path.join(MODEL_DIR, features_file_name)
    dump(features, os.path.join(MODEL_DIR, features_file_name))
    metadata['features'] = features_file_name
    
    # Save metadata
    metadata_file_name = f"{metadata['name']}_v{version}.json"
    metadata_path = os.path.join(METADATA_DIR, metadata_file_name)
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f)
    
    logging.info(f"Registered successfully: {metadata['name']}")
    return metadata_path

def retrieve(model_name, version=None):
    """Retrieve a model and its metadata by name and optionally version."""
    if version is None:
        version = get_next_version(model_name) - 1
    
    metadata_path = os.path.join(METADATA_DIR, f"{model_name}_v{version}.json")
    
    # Load metadata
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
                    
    # Load model
    model = load(os.path.join(MODEL_DIR, metadata["model"]))
    features = load(os.path.join(MODEL_DIR, metadata["features"]))
    
    return model, features
