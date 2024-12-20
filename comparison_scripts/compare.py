import os
import json
import torch

def compare_first_item_in_lists(folder_a, folder_b):
    subfolders = sorted([f for f in os.listdir(folder_a) if os.path.isdir(os.path.join(folder_a, f))])
    for subfolder in subfolders:
        # Construct paths to output.json in each subfolder
        file_a = os.path.join(folder_a, subfolder, 'output.json')
        file_b = os.path.join(folder_b, subfolder, 'output.json')

        # Check if files exist
        if os.path.exists(file_a) and os.path.exists(file_b):
            with open(file_a, 'r') as fa, open(file_b, 'r') as fb:
                try:
                    data_a = json.load(fa)
                    data_b = json.load(fb)
                    
                    # Compare the first item in the list
                    if len(data_a) > 0 and len(data_b) > 0:
                        first_item_a = torch.load(data_a[1]['path'])
                        first_item_b = torch.load(data_b[1]['path'])
                        
                        if torch.equal(first_item_a,first_item_b):
                            print(f"Subfolder {subfolder}: First items are equal.")
                        else:
                            print(f"Subfolder {subfolder}: First items are different by {torch.quantile(torch.abs(first_item_a-first_item_b),.5)}.")
                    else:
                        print(f"Subfolder {subfolder}: One or both lists are empty.")
                except json.JSONDecodeError:
                    print(f"Subfolder {subfolder}: Failed to decode JSON.")
        else:
            print(f"Subfolder {subfolder}: 'output.json' not found in one or both folders.")

# Specify the paths to folder A and folder B
folder_a_path = '/home/riley/mamba/mamba_versions_2/comp/v1/mamba/selective_scan_fn'
folder_b_path = '/home/riley/mamba/mamba_versions_2/comp/v2/mamba/selective_scan_fn'

# Run the comparison
compare_first_item_in_lists(folder_a_path, folder_b_path)
