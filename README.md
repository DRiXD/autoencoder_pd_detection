# autoencoder_pd_detection
This repository holds the code developed for my master thesis "Unmasking Cryptocurrency Pump and Dump Schemes:
An Autoencoder Approach for Detection"

## Installation
Install the requirements for this repo
```
pip3 install -r requirements.txt
```



## Baselines

[Random Forest model](https://github.com/SystemsLab-Sapienza/pump-and-dump-dataset) published by La Morgia et al. 

[Anomaly Transformer and C-LSTM model](https://github.com/Derposoft/crypto_pump_and_dump_with_deep_learning) published by Chadalapaka et al.
To run the Anomaly Transformer we used this command
```
python -m train --model AnomalyTransformer --feature_size 12 --n_layers 4 --n_epochs 200 --lambda 0.0001 --lr 1e-3 --lr_decay_step 0 --batch_size 32 --undersample_ratio 0.05 --segment_length 15 --prthreshold 0.48 --kfolds 5 --dataset ./data features_15S.csv.gz --final_run True
```
And for the C-LSTM this
```
python -m train --model CLSTM --embedding_size 350 --n_layers 1 --n_epochs 200 --kernel_size 3 --dropout 0.0 --cell_norm False --out_norm False --lr 1e-3 --lr_decay_step 0 --batch_size 600 --undersample_ratio 0.05 --segment_length 15 --prthreshold 0.7 --kfolds 5 --dataset ./data/features_15S.csv.gz --final_run True
```
based on their configurations published [here](https://github.com/Derposoft/crypto_pump_and_dump_with_deep_learning/tree/main/models).

