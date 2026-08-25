# Bert-VITS2 Hakka

## Dataset Preparation

Place your dataset in a subdirectory of `data`. The dataset must contain a
`raw` directory with WAV files and an `esd.list` metadata file. You can use
[`sample_esd.old`](sample_esd.old) as a reference for the metadata format.

For example:

```text
data/
└── finetuned/
	├── esd.list
	└── raw/
		├── speaker_001.wav
		└── speaker_002.wav
```

Each line in `esd.list` should use the following format:

```text
audio_path|speaker_name|language_id|phoneme
```

Example:

```text
raw/speaker_001.wav|speaker|HAKKA|miau4 geu3 giet5 yen4
```

## Preprocess the Dataset

Start the preprocessing web UI:

```bash
python webui_preprocess.py
```

In the web UI, enter the dataset directory name. For the example above, enter
`finetuned`, then run the following actions in order:

1. Generate the configuration file.
2. Preprocess the audio files.
3. Preprocess the metadata file.
4. NO need generate bert features

## Train the Model

After preprocessing is complete, start training with:

```bash
python train_ms.py
```