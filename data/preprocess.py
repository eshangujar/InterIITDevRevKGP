from ast import literal_eval
import pandas as pd

def preprocess_fn(df, tokenizer):
    """
    No preprocessing in v1
    """

    df["Answer_text"] = df["Answer_text"].apply(lambda x: literal_eval(x))
    df["Answer_start"] = df["Answer_start"].apply(lambda x: literal_eval(x))
    
    # TODO: this is inefficient, we should tokenize everything at once
    df["Answer_encoded_start"]  = df.apply(lambda x: find_position(x.Paragraph, x.Answer_text, x.Answer_start, tokenizer), axis = 1)
    # df["Answer_start"] = df["Answer_start"].apply(lambda x: x if x != [] else [0])

    return df

def find_position(Paragraph, Answer_text, Answer_start, tokenizer):
	# TODO: optimize this so that tokenizers are called only once
    encoded_s = tokenizer(Paragraph)
    if len(Answer_start) != 0:
        Answer_start = Answer_start[0]
    else:
        return 0, 0
    encoded_s_sliced = tokenizer(Paragraph[Answer_start:])
    encoded_t = tokenizer(Answer_text)
    len_t = len(encoded_t['input_ids']) - 2
    start = len(encoded_s["input_ids"]) - len(encoded_t["input_ids"])
    end = start + len_t

    return start, end