"""
For fast loading of cooccurence network for key words without need to
recalculate statistics.
Useful for presenting results without requiring too much computation.
"""

import time

import pandas as pd

import NL_helpers

t0 = time.time()

def populate_df(df, stat, search_terms):
    """Populate df of cooccurrences for list of search terms
    and their cooccurrences."""
    if stat == 'log dice':
        function = NL_helpers.log_dice_coocs
    elif stat == 'mi':
        function = NL_helpers.mi_coocs

    for term in search_terms:
        try:
            coocs = function(term, dtm, ttm, num_coocs=NUM_COOCS)
            cooc_df.loc[f'{term}_{stat}'] = (
                coocs
                .index
                .to_series()
                .append(coocs, ignore_index=True)
                .to_list()
            )
            for i in coocs.index:
                if not f'{i}_{stat}' in cooc_df.index:
                    secondary_coocs = function(i, dtm, ttm, num_coocs=NUM_COOCS)
                    cooc_df.loc[f'{i}_{stat}'] = (
                        secondary_coocs
                        .index
                        .to_series()
                        .append(secondary_coocs, ignore_index=True)
                        .to_list()
                    )
        except KeyError:
            print(f'{term} not in dictionary')

search_terms = [
    'philosophy',
    'theology',
    'evolutionary', #
    'darwin',
    'huxley',
    'conflict',
    'priestcraft',
    'ancestor',
    'primate',
    'monkey',
    'lower',
    'design',
    'designed',
    'heretic',
    'heresy',
    'creation',
    'creator', # Perhaps I should have stemmed these?
    'warfare'
]

NUM_COOCS = 50



# to_be_generated = [
#     'BOW_entities',
#     'TF-IDF_entities',
#     'BOW_propn',
#     'TF-IDF_propn',
#     'TF-IDF_25kwords'
# ]
# to_be_generated = [
#     'nb2_BOW_11kwords',
#     'nb2_TF-IDF_11kwords'
# ]


entity_terms = [
    'darwin',
    'the church',
    'the sciences',
    'the university',
    'synod',
    'truth',
    'the created word',
    'creation',
    'the reign of grace',
    'leaven of modern thought',
    'the leaven of modern thought',
    'feeling of the modern world',
    'the feeling of the modern world',
    'otago institute'
]

propn_terms = [
    'Darwin',
    'Huxley',
    'White',
    'Draper',
    'Wilberforce',
    'Wallace',
    'Stout',
    'Haast',
    'Evolution',
    'Science',
    'Religion',
    'Theology',
    'Salmond',
    'Macgregor',
    'Mcgregor',
    'Frankland',
    'Parker'
]

to_be_generated = [
    'rel_v2_TF-IDF_11kwords',
    'rel_v2_BOW_11kwords',
    'rel_v2_TF-IDF_entities',
    'rel_v2_BOW_entities',
    'rel_v2_TF-IDF_propn',
    'rel_v2_BOW_propn'
]

for variety in to_be_generated:
    if variety.endswith('11kwords'):
        keywords = search_terms
    elif variety.endswith('entities'):
        keywords = entity_terms
    elif variety.endswith('propn'):
        keywords = propn_terms
    dtm = pd.read_pickle(f'pickles/dtm_{variety}.tar.gz')
    ttm = pd.read_pickle(f'pickles/ttm_{variety}.tar.gz')
    cooc_df = pd.DataFrame(columns = [f'Term {i}' for i in range(NUM_COOCS)] + [f'Score {i}' for i in range(NUM_COOCS)])
    stats = ['log dice', 'mi']
    for stat in stats:
        populate_df(cooc_df, stat, keywords)
    cooc_df.to_pickle(f'pickles/cooc_{variety}_df.tar.gz')
    del dtm, ttm