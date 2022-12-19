import os
import yaml
import argparse
import pandas as pd 
from sklearn.model_selection import train_test_split

from transformers import AutoTokenizer

from config import Config
from utils import set_seed
from data import SQuAD_Dataset
from src import Bert_Classifier_QA

from torch.utils.data import DataLoader

if __name__ == "__main__":
	print(os.getcwd())
	print(os.listdir("data-dir/"))

	parser = argparse.ArgumentParser()
	parser.add_argument('--config', default="config.yaml", help="Config File")

	args = parser.parse_args()
	with open(args.config) as f:
		config = yaml.safe_load(f)
		config = Config(**config)

	set_seed(config.seed)

	df = pd.read_excel(config.data.data_path)
	df_train, df_test = train_test_split(df, test_size=config.data.test_size, random_state=config.seed)
	df_train, df_val = train_test_split(df_train, test_size=config.data.test_size, random_state=config.seed)
	
	tokenizer = AutoTokenizer.from_pretrained(config.model.model_path, TOKENIZERS_PARALLELISM=True, model_max_length=512, padding="max_length") # add local_files_only=local_files_only if using server

	train_ds = SQuAD_Dataset(config, df_train, tokenizer)
	val_ds = SQuAD_Dataset(config, df_val, tokenizer)
	test_ds = SQuAD_Dataset(config, df_test, tokenizer)

	train_dataloader = DataLoader(train_ds, batch_size=config.data.train_batch_size, collate_fn=train_ds.collate_fn)
	val_dataloader = DataLoader(val_ds, batch_size=config.data.val_batch_size, collate_fn=val_ds.collate_fn)
	test_dataloader = DataLoader(test_ds, batch_size=config.data.val_batch_size, collate_fn=test_ds.collate_fn)

	model = Bert_Classifier_QA(config)
	model.__train__(train_dataloader)