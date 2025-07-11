import os, sys
parent_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_dir)

import torch
import torch.nn as nn
import torch.nn.functional as F

import pandas as pd
import re


def constrain_type(config, tgt_word, final_words):
    # Simple token classification without external script
    def classify_token(token):
        """Simple token classification"""
        if token.isdigit():
            return 'integer'
        elif token.replace('.', '').isdigit() and '.' in token:
            return 'floating'
        elif token.startswith('"') or token.startswith("'") or token.endswith('"') or token.endswith("'"):
            return 'string'
        elif token in ['if', 'for', 'while', 'def', 'class', 'return', 'import', 'from', 'as', 'in', 'is', 'and', 'or', 'not', 'True', 'False', 'None', 'try', 'except', 'finally', 'with', 'lambda', 'yield', 'raise', 'assert', 'del', 'global', 'nonlocal', 'pass', 'break', 'continue', 'elif', 'else', 'public', 'private', 'protected', 'static', 'final', 'abstract', 'interface', 'extends', 'implements', 'new', 'this', 'super', 'null', 'void', 'int', 'float', 'double', 'boolean', 'char', 'string', 'var', 'let', 'const', 'function', 'class', 'constructor', 'get', 'set', 'async', 'await', 'export', 'import', 'default', 'module', 'require', 'console', 'log', 'print', 'printf', 'scanf', 'malloc', 'free', 'sizeof', 'struct', 'union', 'enum', 'typedef', 'define', 'include', 'ifdef', 'endif', 'pragma', 'extern', 'volatile', 'register', 'auto', 'goto', 'switch', 'case', 'default', 'do', 'while', 'for', 'if', 'else', 'return', 'break', 'continue', 'sizeof', 'typeof', 'instanceof', 'delete', 'new', 'in', 'of', 'yield', 'await', 'async', 'function', 'class', 'extends', 'implements', 'interface', 'enum', 'namespace', 'module', 'export', 'import', 'require', 'define', 'amd', 'umd', 'commonjs', 'es6', 'strict', 'use', 'strict']:
            return 'keyword'
        elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', token):
            return 'identifier'
        elif token in ['+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>=', '&&', '||', '!', '&', '|', '^', '~', '<<', '>>', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=', '++', '--', '->', '=>', '::', '...', '?', ':', ';', ',', '.', '(', ')', '[', ']', '{', '}', '@', '#', '$', '%', '&', '*', '+', '-', '=', '|', '\\', '/', '`', '~', '!', '?', '^', '_', ':', ';', '"', "'", '<', '>', ',', '.']:
            return 'operator'
        else:
            return 'identifier'  # Default to identifier
    
    # Create simple classification data
    results = []
    all_words = [tgt_word] + final_words
    
    for i, word in enumerate(all_words, 1):
        token_class = classify_token(word)
        results.append({
            'line': i,
            'column': 1,
            'class': token_class,
            'token': word
        })
    
    # Create meta_data similar to original logic
    meta_data = {}
    token_class = ['identifier', 'keyword', 'integer', 'floating', 'string', 'character', 'operator', 'preprocessor', 'sum_classes']
   
    for i in range(1, len(all_words)+1):
        meta_data[i] = {}
        for c in token_class:
            meta_data[i][c] = 0

    for result in results:
        meta_data[result['line']][result['class']] = meta_data[result['line']][result['class']] + 1
        meta_data[result['line']]['sum_classes'] = meta_data[result['line']]['sum_classes'] + 1

    tgt_class = meta_data[1]['sum_classes']
    poss_words = []
    rejected_words = []

    # Stricter Type Constraint
    tgt_tokens = [r['class'] for r in results if r['line'] == 1]

    # If DFG constraint only
    if config['use_dfg_constraint'] == 1:
        if list(set(tgt_tokens)) != ['operator']:
            return poss_words

    for key in meta_data:
        # Making sure the same classes are replaced
        if meta_data[key]['sum_classes'] == tgt_class:
            sub_tokens = [r['class'] for r in results if r['line'] == key]
            if tgt_tokens == sub_tokens:
                poss_words.append(all_words[key-1])
            else:
                rejected_words.append(all_words[key-1])

        # Addition of an operator
        elif meta_data[key]['sum_classes'] == tgt_class + 1:
            sub_tokens = [r['class'] for r in results if r['line'] == key]
            sub_len = sub_tokens.count('operator')
            tgt_len = tgt_tokens.count('operator')
            if sub_len - tgt_len == 1:
                # Make sure the token classes are the same except an operator
                # A keyword is only replaced by a keyword, etc.
                if set(sub_tokens) == set(tgt_tokens):
                    poss_words.append(all_words[key-1])
                else:
                    rejected_words.append(all_words[key-1])
            else:
                rejected_words.append(all_words[key-1])

        # Deletion of an operator
        elif meta_data[key]['sum_classes'] == tgt_class - 1:
            sub_tokens = [r['class'] for r in results if r['line'] == key]
            sub_len = sub_tokens.count('operator')
            tgt_len = tgt_tokens.count('operator')
            if tgt_len - sub_len == 1:
                # Make sure the token classes are the same except an operator
                # A keyword is only replaced by a keyword, etc.
                if set(sub_tokens) == set(tgt_tokens):
                    poss_words.append(all_words[key-1])
                else:
                    rejected_words.append(all_words[key-1])
            else:
                rejected_words.append(all_words[key-1])
        else:
            rejected_words.append(all_words[key-1])

    return poss_words[1:]


def get_bpe_substitues(config, tgt_word, substitutes, tokenizer, mlm_model):
    # substitutes L, k

    substitutes = substitutes[0:12, 0:4] # maximum BPE candidates

    # find all possible candidates 

    all_substitutes = []
    for i in range(substitutes.size(0)):
        if len(all_substitutes) == 0:
            lev_i = substitutes[i]
            all_substitutes = [[int(c)] for c in lev_i]
        else:
            lev_i = []
            for all_sub in all_substitutes:
                for j in substitutes[i]:
                    lev_i.append(all_sub + [int(j)])
            all_substitutes = lev_i

    # all substitutes  list of list of token-id (all candidates)
    c_loss = nn.CrossEntropyLoss(reduction='none')
    word_list = []
    # all_substitutes = all_substitutes[:24]
    all_substitutes = torch.tensor(all_substitutes) # [ N, L ]
    # Use device from config instead of hard-coded cuda
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    all_substitutes = all_substitutes[:24].to(device)
    # print(substitutes.size(), all_substitutes.size())
    N, L = all_substitutes.size()
    word_predictions = mlm_model(all_substitutes)[0] # N L vocab-size
    ppl = c_loss(word_predictions.view(N*L, -1), all_substitutes.view(-1)) # [ N*L ] 
    ppl = torch.exp(torch.mean(ppl.view(N, L), dim=-1)) # N  
    _, word_list = torch.sort(ppl)
    word_list = [all_substitutes[i] for i in word_list]
    final_words = []
    for word in word_list:
        tokens = [tokenizer._convert_id_to_token(int(i)) for i in word]
        text = tokenizer.convert_tokens_to_string(tokens)
        final_words.append(text)

    # Add Type Detection as a constraint
    if config['use_ast_constraint'] == 1:
        final_words = constrain_type(config, tgt_word, final_words)

    return final_words


# def get_substitues(config, tgt_word, substitutes, tokenizer, mlm_model, substitutes_score=None, threshold=3.0):
def get_substitues(config, tgt_word, keys, atk_model, word_predictions, word_pred_scores_all, top_index, threshold):

    # Get the sub_words and their scores for a particular maksed word
    # substitues L, k
    # from this matrix to recover a word
    substitutes = word_predictions[keys[top_index[0]][0]:keys[top_index[0]][1]]  # L, k
    substitutes_score = word_pred_scores_all[keys[top_index[0]][0]:keys[top_index[0]][1]]

    tokenizer = atk_model['tokenizer']
    mlm_model = atk_model['mlm']

    words = []
    sub_len, k = substitutes.size()  # sub-len, k

    if sub_len == 0:
        return words
        
    elif sub_len == 1:
        for (i,j) in zip(substitutes[0], substitutes_score[0]):
            if threshold != 0 and j < threshold:
                break
            words.append(tokenizer._convert_id_to_token(int(i)))
        
        if config['use_ast_constraint'] == 1:
            words = constrain_type(config, tgt_word, words)

    else:
        if config['use_bpe'] == 1:
            words = get_bpe_substitues(config, tgt_word, substitutes, tokenizer, mlm_model)
        else:
            return words
    return words
