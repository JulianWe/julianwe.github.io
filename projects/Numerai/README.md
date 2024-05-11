# Numerai https://numer.ai/home Apply machine learning to predict the stock market.


**Install CLI**
```sh
pip install numerapi
```


**Download Data**
https://numer.ai/data/v4.2
```sh
from numerapi import NumerAPI
napi = NumerAPI()
napi.download_dataset("v4.2/train_int8.parquet", "train_int8.parquet")
napi.download_dataset("v4.2/validation_int8.parquet", "validation_int8.parquet")
napi.download_dataset("v4.2/live_int8.parquet", "live_int8.parquet")
napi.download_dataset("v4.2/live_example_preds.parquet", "live_example_preds.parquet")
napi.download_dataset("v4.2/validation_example_preds.parquet", "validation_example_preds.parquet")
napi.download_dataset("v4.2/features.json", "features.json")
napi.download_dataset("v4.2/meta_model.parquet", "meta_model.parquet")
napi.download_dataset("v4.2/live_benchmark_models.parquet", "live_benchmark_models.parquet")
napi.download_dataset("v4.2/validation_benchmark_models.parquet", "validation_benchmark_models.parquet")
napi.download_dataset("v4.2/train_benchmark_models.parquet", "train_benchmark_models.parquet")
```


**CLI Commmands**
```sh
➜  ~ numerapi
Usage: numerapi [OPTIONS] COMMAND [ARGS]...

  Wrapper around the Numerai API

Options:
  --help  Show this message and exit.

Commands:
  account                   Get all information about your account!
  check-new-round           Check if a new round has started within the...
  competitions              Retrieves information about all competitions
  current-round             Get number of the current active round.
  daily-model-performances  Fetch daily performance of a model.
  download-dataset          Download specified file for the given round
  leaderboard               Get the leaderboard.
  list-datasets             List of available data files
  models                    Get map of account models!
  profile                   Fetch the public profile of a user.
  stake-decrease            Decrease your stake by `value` NMR.
  stake-drain               Completely remove your stake.
  stake-get                 Get stake value of a user.
  stake-increase            Increase your stake by `value` NMR.
  submission-filenames      Get filenames of your submissions
  submit                    Upload predictions from file.
  transactions              List all your deposits and withdrawals.
  user                      Get all information about you! DEPRECATED -...
  version                   Installed numerapi version.

  
```



**Example Scripts https://github.com/numerai/example-scripts**
```sh
#!/usr/bin/env python
""" Example classifier on Numerai data using a xgboost regression. """

import pandas as pd
from xgboost import XGBRegressor

# training data contains features and targets
training_data = pd.read_csv("numerai_training_data.csv").set_index("id")

# tournament data contains features only
tournament_data = pd.read_csv("numerai_tournament_data.csv").set_index("id")
feature_names = [f for f in training_data.columns if "feature" in f]

# train a model to make predictions on tournament data
model = XGBRegressor(max_depth=5, learning_rate=0.01, \
                   n_estimators=2000, colsample_bytree=0.1)
model.fit(training_data[feature_names], training_data["target"])

# submit predictions to numer.ai
predictions = model.predict(tournament_data[feature_names])
predictions.to_csv("predictions.csv")

```