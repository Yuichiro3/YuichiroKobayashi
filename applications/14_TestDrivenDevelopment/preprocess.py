def remove_stopwords(text, stopwords):
    words = text.split()
    filtered = [word for word in words if word not in stopwords]
    return " ".join(filtered)