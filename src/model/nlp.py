import numpy as np
import scipy as sp
import sklearn


def top_features_sm(dtm : sp.sparse.csr_matrix, vec : sklearn.feature_extraction.text.CountVectorizer, n : int =10) -> dict[str, int]:  # noqa: E501
    """Counts the top n features from a sparse matrix and returns a dictionary with the counts

    Args:
        dtm (sp.sparse.csr_matrix): sparse matrix with the data
        vec (CountVectorizer): sklearn countvetorizer to build vocabulary
        n (int, optional): number of top features to return. Defaults to 10.

    Returns:
        dict[str, int]: dictionary with the top features and their counts
    """

    import numpy as np
    words = np.array(vec.get_feature_names_out())
    dtm = dtm.sum(axis=0)  # Sum across all documents to get the frequency of each feature
    dtm = np.array(dtm).reshape(-1)
    top_indices = dtm.argsort()[-n:]  # Get the indices of the top n features
    top_indices = top_indices[::-1]  # Reverse the order of these indices

    # Create a dictionary with feature names and their counts
    top_features = {words[i]: dtm[i] for i in top_indices}
    return top_features

def most_prevalent_topic(doc_topics : np.ndarray) -> np.ndarray:
    """returns the most prevalent topic for each document

    Args:
        doc_topics (np.ndarray): fitted and transformed array of document topics

    Returns:
        np.ndarray: topic index for each document
    """

    return doc_topics.argmax(axis=1)

def get_topic_words(topic : int, topic_word_dist : np.ndarray, vocab : np.ndarray, topn : int =5) -> np.ndarray:
    """returns the top n words for a given topic from the topic model

    Args:
        topic (int): index of the topic
        topic_word_dist (np.ndarray): word distribution for each topic
        vocab (np.ndarray): vocabulary from vectorizer
        topn (int, optional): number of top words to return. Defaults to 10.

    Returns:
        np.ndarray: top n words for the given topic
    """

    top_words = topic_word_dist[topic,:].argsort()[-topn:][::-1].tolist()
    return vocab[top_words]

def topic_words_dist_ranked(topic_idx : int, topic_word_dist : np.ndarray, vocab : np.ndarray, num_words=10) -> str:
    """returns the top n words for a given topic from the topic model

    Args:
        topic_idx (int): topic number
        topic_word_dist (np.ndarray): distribution of words for each topic
        vocab (np.ndarray): vocabulary from vectorizer
        num_words (int, optional): number of top words to return. Defaults to 10.

    Returns:
        str: word
    """

    top_words = topic_word_dist[topic_idx]
    top_words_indices = top_words.argsort()[-num_words:][::-1]  # Get indices of top words
    return [vocab[i] for i in top_words_indices]
