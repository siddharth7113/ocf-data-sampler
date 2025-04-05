from ocf_data_sampler.torch_datasets.datasets.pvnet_uk import PVNetUKRegionalDataset

# Load dataset using your configuration file
dataset = PVNetUKRegionalDataset(config_filename="example_configuration.yaml", gsp_ids=[0])

# Print dataset info
print(f"Dataset length: {len(dataset)}")
print(f"Sample keys: {dataset[0].keys()}")

