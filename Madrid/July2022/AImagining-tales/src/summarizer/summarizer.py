import datasets
import pandas as pd
import tensorflow as tf
import transformers
from transformers import (
    AdamWeightDecay,
    AutoTokenizer,
    DataCollatorForSeq2Seq,
    TFAutoModelForSeq2SeqLM,
)


def load_dataset(path: str, summary_field: str, text_field: str) -> 'datasets.Dataset':
    """Load the data from a given path as a HuggingFace Dataset."""
    dataset = pd.read_csv(path)
    dataset = dataset[[summary_field, text_field]].copy()
    dataset.dropna(inplace=True)
    dataset.reset_index(inplace=True, drop=True)
    return datasets.Dataset.from_pandas(dataset)


def split_train_test_dataset(dataset: 'datasets.Dataset', test_size: float = 0.2) -> 'datasets.Dataset':
    """Split the original dataset into train and test datasets."""
    return dataset.train_test_split(test_size=test_size)


def load_tokenizer(model: str) -> 'transformers.Tokenizer':
    """Load a pretrained Tokenizer from Hugging Face."""
    return AutoTokenizer.from_pretrained(model)


def load_summarizer_model(model: str) -> 'transformers.SummarizerModel':
    """Load a pretrained Summarizer from Hugging Face."""
    return TFAutoModelForSeq2SeqLM.from_pretrained(model)


def load_adam_optimizer(learning_rate: float = 2e-5, weight_decay_rate: float = 0.01) -> 'transformers.Optimizer':
    """Load an Adam optimizer to train the model."""
    return AdamWeightDecay(learning_rate=learning_rate, weight_decay_rate=weight_decay_rate)


def preprocess_dataset(dataset: 'datasets.Dataset', tokenizer: 'transformers.Tokenizer', text_field: str,
                       summary_field: str, tokenizer_prefix: str = '') -> 'datasets.Dataset':
    """Preprocess the dataset tokenizing texts and summaries."""

    def preprocess_function(sample_batch):
        # Some tokenizers require to add a prefix to the input text.
        inputs = [tokenizer_prefix + text for text in sample_batch[text_field]]
        model_inputs = tokenizer(inputs, max_length=1024, truncation=True)

        with tokenizer.as_target_tokenizer():
            labels = tokenizer(sample_batch[summary_field], max_length=128, truncation=True)

        model_inputs['labels'] = labels['input_ids']
        return model_inputs

    return dataset.map(preprocess_function, batched=True)


def collate_dataset(dataset: 'datasets.Dataset', tokenizer: 'transformers.Tokenizer',
                    summarizer: 'transformers.SummarizerModel') -> tuple:
    """Collate the preprocessed dataset."""
    data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=summarizer, return_tensors="tf")

    tf_train_data = dataset["train"].to_tf_dataset(
        columns=["attention_mask", "input_ids", "labels"],
        shuffle=True, batch_size=4, collate_fn=data_collator,
    )
    tf_test_data = dataset["test"].to_tf_dataset(
        columns=["attention_mask", "input_ids", "labels"],
        shuffle=False, batch_size=4, collate_fn=data_collator,
    )

    return tf_train_data, tf_test_data


def train_summarizer(summarizer: 'transformers.SummarizerModel', optimizer: 'transformers.Optimizer',
                     train_data: 'tf.Dataset', validation_data: 'tf.Dataset', epochs: int = 10
                     ) -> 'transformers.SummarizerModel':
    """Compile and train the summarizer model."""
    summarizer.compile(optimizer=optimizer)
    summarizer.fit(x=train_data, validation_data=validation_data, epochs=epochs)
    return summarizer


def save_models(summarizer: 'transformers.SummarizerModel' = None, summarizer_path: str = None,
                tokenizer: 'transformers.Tokenizer' = None, tokenizer_path: str = None) -> None:
    """Save the summarizer and the tokenizer models."""
    if summarizer and summarizer_path:
        summarizer.save_pretrained(summarizer_path)
    if tokenizer and tokenizer_path:
        tokenizer.save_pretrained(tokenizer_path)


def main(data_path: str, text_field: str, summary_field: str,
         tokenizer_model: str, tokenizer_prefix: str,
         tokenizer_path: str, summarizer_model: str, summarizer_path: str) -> None:
    """Execute the main process.

    The main execution process includes:
      - Loading and preparing the data.
      - Preprocessing the data, tokenizing the input texts and summaries.
      - Compiling and training the summarizer model.
      - Saving the trained tokenizer and summarizer.
    """

    # Load the data from a given path.
    data = load_dataset(data_path, summary_field, text_field)
    data = split_train_test_dataset(data)

    # Load a pretrained tokenizer, summarizer and optimizer from Hugging Face.
    tokenizer = load_tokenizer(tokenizer_model)
    summarizer = load_summarizer_model(summarizer_model)
    optimizer = load_adam_optimizer()

    # Preprocess the data, tokenize texts and summaries.
    data = preprocess_dataset(data, tokenizer, text_field, summary_field, tokenizer_prefix=tokenizer_prefix)
    train_data, test_data = collate_dataset(data, tokenizer, summarizer)

    # Train the model.
    summarizer = train_summarizer(summarizer, optimizer, train_data=train_data, validation_data=test_data)

    # Save the summarizer and the tokenizer.
    save_models(summarizer=summarizer, summarizer_path=summarizer_path,
                tokenizer=tokenizer, tokenizer_path=tokenizer_path)


if __name__ == '__main__':

    # Input data.
    data_path = './preprocessed_data/data.csv'
    text_field = 'story_text'
    summary_field = 'summary_text'

    # Tokenizer information.
    tokenizer_model = 't5-small'
    tokenizer_prefix = 'summarize: '
    tokenizer_path = './models/tokenizer'

    # Summarizer information.
    summarizer_model = 't5-small'
    summarizer_path = './models/summarizer'

    main(
        data_path,          # Path of the input data.
        text_field,         # Text field name.
        summary_field,      # Summary field name.
        tokenizer_model,    # Tokenizer model name.
        tokenizer_prefix,   # Tokenizer model prefix (if required).
        tokenizer_path,     # Path to save the Tokenizer model.
        summarizer_model,   # Summarizer model name.
        summarizer_path,    # Path to save the Summarizer model.
    )
