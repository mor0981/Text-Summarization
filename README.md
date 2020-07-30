# Text-Summarization
Information Retrieval - Developed a system for summarization of texts.


<p style="display: flex;">
    <img src="https://github.com/mor0981/Text-Summarization-/blob/master/image.png" >
</p>

### The Problem:
There is a huge amount of textual material, and it is only growing day by day.
There is a great need to reduce a large part of this data to shorter and more focused texts, which provide the important details and contain the information we are looking for.

### Solution:
We will use the auto-text summary method, which is the process of creating a shorter version of a longer document.

### Our method - TextRank

Our method is the Extractive method
Extractive - This method relies on extracting sentences from the text.
Therefore, identifying the appropriate sentences for the summary is of paramount importance in the Extractive method.

Let’s understand the TextRank algorithm, now that we have a grasp on PageRank.

1) The text is represented as a graph, with each sentence converted to a node
2) Similarity between any two sentences is used as an equivalent to the web page transition probability
3) The similarity scores are stored in a square matrix, similar to the matrix M used for PageRank

### How It Works

1) The first step would be to concatenate all the text contained in the articles
2) Then split the text into individual sentences
3) In the next step, we will find vector representation (word embeddings) for each and every sentence
4) Similarities between sentence vectors are then calculated and stored in a matrix
5) The similarity matrix is then converted into a graph, with sentences as vertices and similarity scores as edges, for sentence rank calculation
6) Finally, a certain number of top-ranked sentences form the final summary


