def chunk_text(text,chunk_size=100,overlap=20):
    words = text.split( )
    chunks=[]
    for i in range(0,len(words),chunk_size-overlap):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks