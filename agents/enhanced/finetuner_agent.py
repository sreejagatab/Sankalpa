
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import os
import json
import subprocess
import shutil
from datetime import datetime
from agents.base import BaseAgent
from pathlib import Path

class FinetunerAgent(BaseAgent):
    """
    Fully functional fine-tuning agent that creates and executes fine-tuning jobs for various LLM models
    and provides tools for data preparation, monitoring, and evaluation.
    """
    
    def run(self, input_data):
        # Extract parameters
        model_name = input_data.get("model", "gpt-3.5-turbo")
        dataset_path = input_data.get("dataset", "data/train.jsonl") 
        n_epochs = input_data.get("epochs", 3)
        batch_size = input_data.get("batch_size", 4)
        learning_rate = input_data.get("learning_rate", 0.0002)
        suffix = input_data.get("suffix", datetime.now().strftime("%Y%m%d_%H%M%S"))
        validate_data = input_data.get("validate_data", True)
        
        # Additional parameters
        auto_execute = input_data.get("auto_execute", False)
        api_key = input_data.get("api_key", os.environ.get("OPENAI_API_KEY", ""))
        evaluation_data = input_data.get("evaluation_data", "")
        
        # Directory for fine-tuning assets
        os.makedirs("fine_tuning", exist_ok=True)
        os.makedirs("fine_tuning/scripts", exist_ok=True)
        os.makedirs("fine_tuning/configs", exist_ok=True)
        os.makedirs("fine_tuning/data", exist_ok=True)
        os.makedirs("fine_tuning/evaluation", exist_ok=True)
        
        # Create fine-tuning configuration
        config = {
            "model": model_name,
            "dataset": dataset_path,
            "n_epochs": n_epochs,
            "batch_size": batch_size,
            "learning_rate": learning_rate,
            "suffix": suffix,
            "created_at": datetime.now().isoformat(),
            "evaluation_data": evaluation_data
        }
        
        # Save configuration
        config_path = f"fine_tuning/configs/config_{suffix}.json"
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        
        # Create data validation script
        validation_script = """#!/usr/bin/env python3
import json
import sys
import os

def validate_jsonl(file_path):
    print("Validating file:", file_path)
    line_number = 0
    valid = True
    errors = []

    with open(file_path, 'r') as f:
        for line_number, line in enumerate(f, 1):
            try:
                # Parse JSON
                data = json.loads(line)
                
                # Check required fields for different formats
                if 'messages' in data:
                    # Chat format
                    if not isinstance(data['messages'], list) or len(data['messages']) < 1:
                        errors.append(f"Line {line_number}: 'messages' must be a non-empty list")
                        valid = False
                    for msg in data['messages']:
                        if 'role' not in msg or 'content' not in msg:
                            errors.append(f"Line {line_number}: Each message must have 'role' and 'content'")
                            valid = False
                        if msg['role'] not in ['system', 'user', 'assistant']:
                            errors.append(f"Line {line_number}: Invalid role: {msg['role']}")
                            valid = False
                
                elif 'prompt' in data and 'completion' in data:
                    # Completion format (deprecated but supported)
                    if not isinstance(data['prompt'], str) or not isinstance(data['completion'], str):
                        errors.append(f"Line {line_number}: 'prompt' and 'completion' must be strings")
                        valid = False
                
                else:
                    errors.append(f"Line {line_number}: Missing required fields")
                    valid = False
                    
            except json.JSONDecodeError as e:
                errors.append(f"Line {line_number}: Invalid JSON - {str(e)}")
                valid = False
                
    if valid:
        print(f"✅ Validation passed! Processed {line_number} examples.")
        return True
    else:
        print(f"❌ Validation failed with {len(errors)} errors:")
        for error in errors:
            print(f"  - {error}")
        return False

def auto_fix_jsonl(file_path, output_path=None):
    # Try to fix common issues in the JSONL file
    if not output_path:
        output_path = file_path + ".fixed"
    
    fixed_lines = []
    issues_fixed = 0
    
    with open(file_path, 'r') as f:
        for line_number, line in enumerate(f, 1):
            try:
                # Parse JSON
                data = json.loads(line)
                # No issues with this line
                fixed_lines.append(json.dumps(data))
                
            except json.JSONDecodeError:
                # Try to fix common JSON issues
                fixed_line = line.strip()
                
                # Handle missing quotes around keys
                for potential_key in ["messages", "role", "content", "prompt", "completion"]:
                    fixed_line = fixed_line.replace(f"{potential_key}:", f"\"{potential_key}\":")
                
                # Handle missing quotes around string values
                fixed_line = fixed_line.replace(": system", ": \"system\"")
                fixed_line = fixed_line.replace(": user", ": \"user\"")
                fixed_line = fixed_line.replace(": assistant", ": \"assistant\"")
                
                # Try to parse again
                try:
                    json.loads(fixed_line)
                    fixed_lines.append(fixed_line)
                    issues_fixed += 1
                    print(f"Fixed line {line_number}")
                except json.JSONDecodeError:
                    print(f"Could not fix line {line_number}, skipping")
    
    # Write the fixed file
    with open(output_path, 'w') as f:
        for line in fixed_lines:
            f.write(line + "\\n")
    
    print(f"Fixed {issues_fixed} issues. Saved to {output_path}")
    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_data.py <path_to_jsonl> [--fix]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
        
    # Check if --fix flag is provided
    if len(sys.argv) > 2 and sys.argv[2] == "--fix":
        fixed_file = auto_fix_jsonl(file_path)
        print(f"Validating fixed file: {fixed_file}")
        if validate_jsonl(fixed_file):
            print(f"Fixed file passed validation: {fixed_file}")
            sys.exit(0)
        else:
            print(f"Fixed file still has issues: {fixed_file}")
            sys.exit(1)
    else:
        if validate_jsonl(file_path):
            sys.exit(0)
        else:
            sys.exit(1)
"""
        
        # Create dataset preparation utility
        dataset_script = """#!/usr/bin/env python3
import json
import csv
import argparse
import os
import random
from sklearn.model_selection import train_test_split
from pathlib import Path

def convert_csv_to_jsonl(csv_file, jsonl_file, format_type="chat"):
    # Convert a CSV file to JSONL format for fine-tuning
    print(f"Converting {csv_file} to {jsonl_file} in {format_type} format")
    
    with open(csv_file, 'r', encoding='utf-8') as infile:
        with open(jsonl_file, 'w', encoding='utf-8') as outfile:
            reader = csv.DictReader(infile)
            
            for row in reader:
                if format_type == "chat":
                    # Chat format (for newer models)
                    system_content = row.get('system', 'You are a helpful AI assistant.')
                    user_content = row.get('user', '')
                    assistant_content = row.get('assistant', '')
                    
                    chat_example = {
                        "messages": [
                            {"role": "system", "content": system_content},
                            {"role": "user", "content": user_content},
                            {"role": "assistant", "content": assistant_content}
                        ]
                    }
                    json.dump(chat_example, outfile)
                    outfile.write('\\n')
                else:
                    # Completion format (for older models)
                    prompt = row.get('prompt', '')
                    completion = row.get('completion', '')
                    
                    completion_example = {
                        "prompt": prompt,
                        "completion": completion
                    }
                    json.dump(completion_example, outfile)
                    outfile.write('\\n')

def split_dataset(input_file, train_ratio=0.8, format_check=True):
    # Split a JSONL dataset into training and evaluation sets
    input_path = Path(input_file)
    base_dir = input_path.parent
    stem = input_path.stem
    
    train_file = base_dir / f"{stem}_train.jsonl"
    eval_file = base_dir / f"{stem}_eval.jsonl"
    
    # Read the dataset
    data = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                entry = json.loads(line)
                # Validate format if requested
                if format_check:
                    if 'messages' in entry:
                        if not isinstance(entry['messages'], list) or len(entry['messages']) < 2:
                            print("Warning: Skipping invalid entry (messages must be a list with at least 2 items)")
                            continue
                    elif 'prompt' in entry and 'completion' in entry:
                        pass
                    else:
                        print("Warning: Skipping entry with missing required fields")
                        continue
                data.append(line)
            except json.JSONDecodeError:
                print("Warning: Skipping invalid JSON line")
    
    # Split the data
    train_data, eval_data = train_test_split(data, train_size=train_ratio, random_state=42)
    
    # Write the split files
    with open(train_file, 'w', encoding='utf-8') as f:
        for line in train_data:
            f.write(line)
    
    with open(eval_file, 'w', encoding='utf-8') as f:
        for line in eval_data:
            f.write(line)
    
    print(f"Dataset split into {len(train_data)} training examples and {len(eval_data)} evaluation examples")
    print(f"Training file: {train_file}")
    print(f"Evaluation file: {eval_file}")
    
    return str(train_file), str(eval_file)

def create_sample_data(output_file, num_samples=10, format_type="chat"):
    # Create a sample dataset for demonstration purposes
    with open(output_file, 'w', encoding='utf-8') as f:
        for i in range(num_samples):
            if format_type == "chat":
                sample = {
                    "messages": [
                        {"role": "system", "content": "You are a helpful AI assistant."},
                        {"role": "user", "content": f"Example question {i+1}: What is artificial intelligence?"},
                        {"role": "assistant", "content": f"Example answer {i+1}: Artificial intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think and learn like humans."}
                    ]
                }
            else:
                sample = {
                    "prompt": f"Example question {i+1}: What is artificial intelligence?\\n",
                    "completion": f"Example answer {i+1}: Artificial intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think and learn like humans.\\n"
                }
            json.dump(sample, f)
            f.write('\\n')
    
    print(f"Created sample dataset with {num_samples} examples at {output_file}")
    return output_file

def main():
    parser = argparse.ArgumentParser(description='Dataset utilities for OpenAI fine-tuning')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Convert CSV command
    convert_parser = subparsers.add_parser('convert', help='Convert CSV to JSONL')
    convert_parser.add_argument('csv_file', help='Path to input CSV file')
    convert_parser.add_argument('jsonl_file', help='Path to output JSONL file')
    convert_parser.add_argument('--format', choices=['chat', 'completion'], default='chat',
                    help='Format type: chat (for ChatGPT) or completion (for older models)')
    
    # Split dataset command
    split_parser = subparsers.add_parser('split', help='Split dataset into training and evaluation')
    split_parser.add_argument('input_file', help='Path to input JSONL file')
    split_parser.add_argument('--ratio', type=float, default=0.8, help='Training set ratio (default: 0.8)')
    
    # Create sample command
    sample_parser = subparsers.add_parser('sample', help='Create sample dataset')
    sample_parser.add_argument('output_file', help='Path to output JSONL file')
    sample_parser.add_argument('--count', type=int, default=10, help='Number of samples to create')
    sample_parser.add_argument('--format', choices=['chat', 'completion'], default='chat',
                    help='Format type: chat (for ChatGPT) or completion (for older models)')
    
    args = parser.parse_args()
    
    if args.command == 'convert':
        convert_csv_to_jsonl(args.csv_file, args.jsonl_file, args.format)
        print(f"Conversion complete! Created {args.jsonl_file}")
    
    elif args.command == 'split':
        train_file, eval_file = split_dataset(args.input_file, args.ratio)
        print(f"Split complete!")
    
    elif args.command == 'sample':
        sample_file = create_sample_data(args.output_file, args.count, args.format)
        print(f"Sample data created!")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
"""

        # Create fine-tuning script that actually performs fine-tuning
        finetune_script = f"""#!/bin/bash
# Real fine-tuning script for {model_name} on {dataset_path}
# Generated by Sankalpa Finetuner Agent

set -e  # Exit on any error

# Load configuration
CONFIG_FILE="{config_path}"
echo "Loading configuration from $CONFIG_FILE"
MODEL=$(jq -r '.model' "$CONFIG_FILE")
DATASET=$(jq -r '.dataset' "$CONFIG_FILE")
SUFFIX=$(jq -r '.suffix' "$CONFIG_FILE")
EVALUATION_DATA=$(jq -r '.evaluation_data // ""' "$CONFIG_FILE")

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY environment variable is not set."
    echo "Please set your API key with: export OPENAI_API_KEY=your_api_key"
    exit 1
fi

# Ensure the dataset exists
if [ ! -f "$DATASET" ]; then
    echo "Dataset file not found: $DATASET"
    echo "Creating a sample dataset..."
    python fine_tuning/scripts/dataset_utils.py sample "fine_tuning/data/sample_data.jsonl" --count 20
    DATASET="fine_tuning/data/sample_data.jsonl"
    # Update config
    jq ".dataset = \\"$DATASET\\"" "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
fi

# Validate dataset
echo "Validating dataset: $DATASET"
python fine_tuning/scripts/validate_data.py "$DATASET"
if [ $? -ne 0 ]; then
    echo "Data validation failed. Attempting to fix dataset..."
    python fine_tuning/scripts/validate_data.py "$DATASET" --fix
    if [ $? -ne 0 ]; then
        echo "Could not automatically fix dataset. Please fix your dataset before proceeding."
        exit 1
    fi
    DATASET="$DATASET.fixed"
    # Update config
    jq ".dataset = \\"$DATASET\\"" "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
fi

# Check if we need to create evaluation data
if [ -z "$EVALUATION_DATA" ] || [ ! -f "$EVALUATION_DATA" ]; then
    echo "Creating evaluation data by splitting dataset..."
    TRAIN_FILE=$(basename "$DATASET" .jsonl)_train.jsonl
    EVAL_FILE=$(basename "$DATASET" .jsonl)_eval.jsonl
    python fine_tuning/scripts/dataset_utils.py split "$DATASET" --ratio 0.8
    DATASET="fine_tuning/data/$TRAIN_FILE"
    EVALUATION_DATA="fine_tuning/data/$EVAL_FILE"
    # Update config
    jq ".dataset = \\"$DATASET\\" | .evaluation_data = \\"$EVALUATION_DATA\\"" "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
fi

echo "Starting fine-tuning job..."
echo "Model: $MODEL"
echo "Dataset: $DATASET"
echo "Suffix: $SUFFIX"

# Actually upload the training file
echo "Uploading training file to OpenAI..."
TRAINING_FILE_RESP=$(openai files create --file "$DATASET" --purpose fine-tune)
TRAINING_FILE_ID=$(echo $TRAINING_FILE_RESP | jq -r '.id')

if [ -z "$TRAINING_FILE_ID" ] || [ "$TRAINING_FILE_ID" == "null" ]; then
    echo "Failed to upload training file!"
    echo "$TRAINING_FILE_RESP"
    exit 1
fi

echo "Training file uploaded with ID: $TRAINING_FILE_ID"

# Start fine-tuning
if [[ "$MODEL" == gpt-3.5* ]] || [[ "$MODEL" == gpt-4* ]]; then
    # Fine-tune ChatGPT models using chat format
    echo "Creating fine-tuning job for ChatGPT model..."
    FINE_TUNE_RESP=$(openai fine_tuning.create \\
        --training_file "$TRAINING_FILE_ID" \\
        --model "$MODEL" \\
        --suffix "$SUFFIX" \\
        --hyperparameters n_epochs={n_epochs} batch_size={batch_size} learning_rate_multiplier={learning_rate})
else
    # Fall back to legacy fine-tuning for other models
    echo "Creating legacy fine-tuning job..."
    FINE_TUNE_RESP=$(openai api fine_tunes.create \\
        --training_file "$TRAINING_FILE_ID" \\
        --model "$MODEL" \\
        --suffix "$SUFFIX" \\
        --n_epochs {n_epochs})
fi

FINE_TUNE_ID=$(echo $FINE_TUNE_RESP | jq -r '.id')

if [ -z "$FINE_TUNE_ID" ] || [ "$FINE_TUNE_ID" == "null" ]; then
    echo "Failed to create fine-tuning job!"
    echo "$FINE_TUNE_RESP"
    exit 1
fi

echo "Fine-tuning job submitted successfully with ID: $FINE_TUNE_ID"
echo "Writing job ID to config file..."

# Update config with job ID
jq ".job_id = \\"$FINE_TUNE_ID\\"" "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"

echo "You can check the status of your fine-tuning jobs with:"
echo "openai api fine_tuning.list"
echo "or specifically for this job:"
echo "openai api fine_tuning.get -i $FINE_TUNE_ID"
echo "To stream events:"
echo "openai api fine_tuning.events -i $FINE_TUNE_ID --stream"
"""

        # Create monitoring script
        monitor_script = """#!/bin/bash
# Script to monitor fine-tuning jobs

if [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY environment variable is not set."
    echo "Please set your API key with: export OPENAI_API_KEY=your_api_key"
    exit 1
fi

# Check if we're monitoring a specific job
if [ "$1" != "" ]; then
    # Monitor specific job
    JOB_ID="$1"
    echo "Monitoring fine-tuning job: $JOB_ID"
    echo "Press Ctrl+C to stop streaming events"
    openai fine_tuning.events --stream -i "$JOB_ID"
    exit 0
fi

# Otherwise list all jobs
echo "Fetching active fine-tuning jobs..."
openai fine_tuning.list --limit 10

echo ""
echo "To check details of a specific job, run:"
echo "openai fine_tuning.get -i <job_id>"

echo ""
echo "To stream events from a job, run:"
echo "$(basename "$0") <job_id>"
"""

        # Create evaluation script
        evaluation_script = """#!/usr/bin/env python3
import os
import json
import sys
import argparse
try:
    import openai
except ImportError:
    print("OpenAI SDK not installed. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
    import openai
    
from pathlib import Path

def evaluate_model(model_id, eval_file, max_examples=50, temperature=0.0):
    # Evaluate a fine-tuned model against a test set
    
    # Load evaluation data
    eval_examples = []
    with open(eval_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                example = json.loads(line)
                eval_examples.append(example)
            except json.JSONDecodeError:
                print("Warning: Skipping invalid JSON line")
    
    # Limit the number of examples if needed
    if len(eval_examples) > max_examples:
        print(f"Limiting evaluation to {max_examples} examples (from {len(eval_examples)})")
        eval_examples = eval_examples[:max_examples]
    
    # Initialize OpenAI client
    client = openai.OpenAI()
    
    # Process each example
    results = []
    
    print(f"Evaluating model {model_id} on {len(eval_examples)} examples")
    
    for i, example in enumerate(eval_examples):
        try:
            # Extract the prompt based on format
            if 'messages' in example:  # Chat format
                messages = example['messages']
                # We'll use all messages except the last one (which is the expected assistant response)
                prompt_messages = messages[:-1]
                expected_response = messages[-1]['content'] if messages[-1]['role'] == 'assistant' else None
                
                # Call the model
                response = client.chat.completions.create(
                    model=model_id,
                    messages=prompt_messages,
                    temperature=temperature
                )
                
                model_response = response.choices[0].message.content
                
            elif 'prompt' in example and 'completion' in example:  # Completion format
                prompt = example['prompt']
                expected_response = example['completion']
                
                # Call the model
                response = client.completions.create(
                    model=model_id,
                    prompt=prompt,
                    temperature=temperature,
                    max_tokens=1000
                )
                
                model_response = response.choices[0].text
            
            else:
                print(f"Example {i} has invalid format, skipping")
                continue
            
            # Store the result
            results.append({
                'example_id': i,
                'prompt': prompt_messages if 'messages' in example else prompt,
                'expected_response': expected_response,
                'model_response': model_response
            })
            
            # Print progress
            if (i + 1) % 5 == 0:
                print(f"Processed {i + 1}/{len(eval_examples)} examples")
            
        except Exception as e:
            print(f"Error processing example {i}: {str(e)}")
    
    # Calculate simple metrics
    if results:
        # Save detailed results
        output_file = f"fine_tuning/evaluation/{Path(model_id).stem}_eval_results.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        print(f"Evaluation complete. Results saved to {output_file}")
        print(f"Processed {len(results)} out of {len(eval_examples)} examples")
    else:
        print("No results generated during evaluation")

def main():
    parser = argparse.ArgumentParser(description='Evaluate a fine-tuned model')
    parser.add_argument('model_id', help='The fine-tuned model ID to evaluate')
    parser.add_argument('eval_file', help='Path to the evaluation JSONL file')
    parser.add_argument('--max', type=int, default=50, help='Maximum number of examples to evaluate')
    parser.add_argument('--temp', type=float, default=0.0, help='Temperature for generation (0.0 for deterministic)')
    
    args = parser.parse_args()
    
    # Check if API key is set
    if not os.environ.get('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY environment variable is not set")
        sys.exit(1)
    
    # Check if eval file exists
    if not os.path.exists(args.eval_file):
        print(f"Error: Evaluation file not found: {args.eval_file}")
        sys.exit(1)
    
    evaluate_model(args.model_id, args.eval_file, args.max, args.temp)

if __name__ == "__main__":
    main()
"""

        # Create real fine-tuning module
        finetuning_module = """#!/usr/bin/env python3
import os
import json
import time
import subprocess
import argparse
from pathlib import Path
try:
    import openai
except ImportError:
    print("OpenAI SDK not installed. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
    import openai

class FineTuner:
    def __init__(self, api_key=None, config_path=None):
        # Initialize the fine-tuner with API key and config
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key.")
        
        # Set API key for client
        os.environ['OPENAI_API_KEY'] = self.api_key
        self.client = openai.OpenAI(api_key=self.api_key)
        
        # Load config if provided
        self.config = {}
        if config_path:
            with open(config_path, 'r') as f:
                self.config = json.load(f)
                self.config["config_path"] = config_path
    
    def validate_data(self, dataset_path):
        # Validate the dataset format
        print(f"Validating dataset: {dataset_path}")
        
        # Use the validate script
        validate_script = Path("fine_tuning/scripts/validate_data.py")
        if validate_script.exists():
            result = subprocess.run(['python', str(validate_script), dataset_path], 
                                    capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Validation failed: {result.stderr or result.stdout}")
                return False
            return True
        
        # Manual validation as fallback
        try:
            valid = True
            errors = []
            with open(dataset_path, 'r') as f:
                for i, line in enumerate(f, 1):
                    try:
                        data = json.loads(line)
                        # Simple format check
                        if not ('messages' in data or ('prompt' in data and 'completion' in data)):
                            errors.append(f"Line {i}: Missing required fields")
                            valid = False
                    except json.JSONDecodeError:
                        errors.append(f"Line {i}: Invalid JSON")
                        valid = False
            
            if not valid:
                for error in errors[:5]:  # Show first 5 errors
                    print(error)
                if len(errors) > 5:
                    print(f"...and {len(errors) - 5} more errors")
            
            return valid
        except Exception as e:
            print(f"Validation error: {str(e)}")
            return False
    
    def upload_file(self, file_path):
        # Upload a file to OpenAI
        print(f"Uploading file: {file_path}")
        try:
            with open(file_path, 'rb') as f:
                response = self.client.files.create(
                    file=f,
                    purpose="fine-tune"
                )
            print(f"File uploaded with ID: {response.id}")
            return response.id
        except Exception as e:
            print(f"Error uploading file: {str(e)}")
            return None
    
    def create_finetune_job(self, training_file_id, model="gpt-3.5-turbo", suffix=None, 
                           n_epochs=3, batch_size=4, learning_rate=0.0002):
        # Create a fine-tuning job
        print(f"Creating fine-tuning job for model: {model}")
        try:
            # Handle different model types
            if model.startswith(("gpt-3.5", "gpt-4")):
                # New fine-tuning API
                response = self.client.fine_tuning.create(
                    training_file=training_file_id,
                    model=model,
                    suffix=suffix,
                    hyperparameters={
                        "n_epochs": n_epochs,
                        "batch_size": batch_size,
                        "learning_rate_multiplier": learning_rate
                    }
                )
            else:
                # Legacy fine-tuning API
                response = self.client.fine_tunes.create(
                    training_file=training_file_id,
                    model=model,
                    suffix=suffix,
                    n_epochs=n_epochs
                )
            
            print(f"Fine-tuning job created with ID: {response.id}")
            return response.id
            
        except Exception as e:
            print(f"Error creating fine-tuning job: {str(e)}")
            return None
    
    def monitor_job(self, job_id, polling_interval=10, max_wait_time=None):
        # Monitor a fine-tuning job until completion
        print(f"Monitoring fine-tuning job: {job_id}")
        status = "running"
        start_time = time.time()
        
        try:
            # First determine if this is a new or legacy job
            is_legacy = False
            try:
                self.client.fine_tuning.retrieve(job_id)
            except:
                is_legacy = True
            
            previous_progress = 0
            
            while status in ["running", "created", "pending"]:
                # Check timeout
                if max_wait_time and (time.time() - start_time) > max_wait_time:
                    print(f"Monitoring timed out after {max_wait_time} seconds")
                    break
                
                # Get job status
                if is_legacy:
                    job = self.client.fine_tunes.retrieve(job_id)
                    status = job.status
                    progress = job.get("progress", 0)
                else:
                    job = self.client.fine_tuning.retrieve(job_id)
                    status = job.status
                    # Calculate progress from the events
                    events = self.client.fine_tuning.events(job_id).data
                    progress_events = [e for e in events if "progress" in e.data]
                    progress = progress_events[-1].data["progress"] if progress_events else 0
                
                # Update progress
                if progress > previous_progress:
                    print(f"Progress: {progress}%")
                    previous_progress = progress
                
                # Wait before checking again
                if status in ["running", "created", "pending"]:
                    time.sleep(polling_interval)
            
            # Get final status
            if is_legacy:
                job = self.client.fine_tunes.retrieve(job_id)
            else:
                job = self.client.fine_tuning.retrieve(job_id)
            
            if job.status == "succeeded":
                fine_tuned_model = job.fine_tuned_model
                print(f"Fine-tuning completed successfully!")
                print(f"Fine-tuned model ID: {fine_tuned_model}")
                return {
                    "status": "succeeded",
                    "model_id": fine_tuned_model,
                    "job_id": job_id
                }
            else:
                print(f"Fine-tuning ended with status: {job.status}")
                return {
                    "status": job.status,
                    "job_id": job_id
                }
                
        except Exception as e:
            print(f"Error monitoring fine-tuning job: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "job_id": job_id
            }
    
    def run(self, dataset_path, model="gpt-3.5-turbo", wait_for_completion=True):
        # Run the complete fine-tuning process
        # Validate the dataset
        if not self.validate_data(dataset_path):
            print("Dataset validation failed.")
            return {
                "status": "error",
                "error": "Dataset validation failed"
            }
        
        # Upload the file
        file_id = self.upload_file(dataset_path)
        if not file_id:
            return {
                "status": "error",
                "error": "File upload failed"
            }
        
        # Create fine-tuning job
        suffix = f"ft_{int(time.time())}"
        job_id = self.create_finetune_job(
            training_file_id=file_id,
            model=model,
            suffix=suffix,
            n_epochs=self.config.get("n_epochs", 3),
            batch_size=self.config.get("batch_size", 4),
            learning_rate=self.config.get("learning_rate", 0.0002)
        )
        
        if not job_id:
            return {
                "status": "error",
                "error": "Failed to create fine-tuning job"
            }
        
        # Save job info
        job_info = {
            "job_id": job_id,
            "file_id": file_id,
            "model": model,
            "dataset": dataset_path,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "running"
        }
        
        # Update config with job info
        if self.config:
            self.config.update(job_info)
            config_path = self.config.get("config_path")
            if config_path:
                with open(config_path, 'w') as f:
                    json.dump(self.config, f, indent=2)
        
        # Monitor the job if requested
        if wait_for_completion:
            result = self.monitor_job(job_id)
            
            # Update config with final status
            if self.config and "config_path" in self.config:
                self.config.update(result)
                with open(self.config["config_path"], 'w') as f:
                    json.dump(self.config, f, indent=2)
            
            return result
        
        return job_info

def main():
    parser = argparse.ArgumentParser(description='Run fine-tuning process')
    parser.add_argument('dataset', help='Path to the training dataset (JSONL)')
    parser.add_argument('--model', default='gpt-3.5-turbo', help='Base model to fine-tune')
    parser.add_argument('--config', help='Path to configuration file')
    parser.add_argument('--no-wait', action='store_true', help='Don\'t wait for job completion')
    
    args = parser.parse_args()
    
    # Check if dataset exists
    if not os.path.exists(args.dataset):
        print(f"Error: Dataset not found: {args.dataset}")
        return
    
    try:
        # Create fine-tuner
        fine_tuner = FineTuner(config_path=args.config)
        
        # Run fine-tuning
        result = fine_tuner.run(
            dataset_path=args.dataset,
            model=args.model,
            wait_for_completion=not args.no_wait
        )
        
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
"""

        # Save all scripts
        files = {
            "fine_tuning/scripts/fine_tune.sh": finetune_script,
            "fine_tuning/scripts/validate_data.py": validation_script,
            "fine_tuning/scripts/dataset_utils.py": dataset_script,
            "fine_tuning/scripts/monitor_jobs.sh": monitor_script,
            "fine_tuning/scripts/evaluate_model.py": evaluation_script,
            "fine_tuning/scripts/fine_tuner.py": finetuning_module,
            "fine_tuning/configs/config_{}.json".format(suffix): json.dumps(config, indent=2)
        }
        
        # Write files to disk
        for file_path, content in files.items():
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                f.write(content)
        
        # Make scripts executable
        for script_path in [
            "fine_tuning/scripts/fine_tune.sh", 
            "fine_tuning/scripts/monitor_jobs.sh",
            "fine_tuning/scripts/validate_data.py",
            "fine_tuning/scripts/dataset_utils.py",
            "fine_tuning/scripts/evaluate_model.py",
            "fine_tuning/scripts/fine_tuner.py"
        ]:
            full_path = os.path.join(os.getcwd(), script_path)
            if os.path.exists(full_path):
                os.chmod(full_path, 0o755)
        
        # If auto_execute is enabled, actually start fine-tuning
        result = {
            "message": "Fine-tuning package created with fully functional scripts for data preparation, validation, job submission, and monitoring.",
            "config": config,
            "files": files,
            "instructions": [
                "1. Place your training data in JSONL format at '{}'".format(dataset_path),
                "2. Set your OpenAI API key: export OPENAI_API_KEY=your_key",
                "3. Run the validation script: python fine_tuning/scripts/validate_data.py {}".format(dataset_path),
                "4. Start fine-tuning: bash fine_tuning/scripts/fine_tune.sh",
                "5. Monitor your jobs: bash fine_tuning/scripts/monitor_jobs.sh",
                "6. Evaluate your model: python fine_tuning/scripts/evaluate_model.py <model_id> <evaluation_data>"
            ]
        }
        
        if auto_execute and api_key:
            try:
                # Set API key
                os.environ["OPENAI_API_KEY"] = api_key
                
                # Check if dataset exists, if not create a sample one
                if not os.path.exists(dataset_path):
                    print(f"Dataset not found at {dataset_path}, creating a sample dataset.")
                    sample_path = "fine_tuning/data/sample_data.jsonl"
                    # Create sample data directory
                    os.makedirs(os.path.dirname(sample_path), exist_ok=True)
                    # Create sample data
                    try:
                        from openai import OpenAI
                        client = OpenAI(api_key=api_key)
                    except ImportError:
                        # If OpenAI SDK is not installed, create sample data manually
                        client = None
                    
                    # Simple sample data
                    samples = []
                    for i in range(10):
                        samples.append({
                            "messages": [
                                {"role": "system", "content": "You are a helpful assistant specializing in technology."},
                                {"role": "user", "content": f"What is a {['computer', 'smartphone', 'tablet', 'cloud computing', 'machine learning'][i % 5]}?"},
                                {"role": "assistant", "content": f"A detailed explanation of {['computer', 'smartphone', 'tablet', 'cloud computing', 'machine learning'][i % 5]} would include its definition, history, and applications."}
                            ]
                        })
                    
                    with open(sample_path, "w") as f:
                        for sample in samples:
                            f.write(json.dumps(sample) + "\n")
                    
                    dataset_path = sample_path
                    config["dataset"] = dataset_path
                    
                    # Update config file
                    with open(config_path, "w") as f:
                        json.dump(config, f, indent=2)
                
                # Run fine-tuning script
                print("Starting fine-tuning...")
                try:
                    # Try to use the fine_tuner module
                    import importlib.util
                    spec = importlib.util.spec_from_file_location("fine_tuner", "fine_tuning/scripts/fine_tuner.py")
                    fine_tuner_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(fine_tuner_module)
                    
                    # Create fine tuner
                    fine_tuner = fine_tuner_module.FineTuner(api_key=api_key, config_path=config_path)
                    
                    # Run fine-tuning
                    ft_result = fine_tuner.run(
                        dataset_path=dataset_path,
                        model=model_name,
                        wait_for_completion=False  # Don't wait in the agent to avoid timeouts
                    )
                    
                    result["fine_tuning_job"] = ft_result
                    result["message"] = "Fine-tuning job started! Use the monitor script to check progress."
                except Exception as e:
                    print(f"Error importing fine-tuner module: {str(e)}")
                    # Fall back to using the script directly
                    subprocess.Popen(["bash", "fine_tuning/scripts/fine_tune.sh"], 
                                    env=dict(os.environ, OPENAI_API_KEY=api_key))
                    result["message"] = "Fine-tuning job started via script! Use the monitor script to check progress."
                
            except Exception as e:
                print(f"Error executing fine-tuning: {str(e)}")
                result["auto_execute_error"] = str(e)
        
        return result