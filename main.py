from src.pipeline.rag_pipeline import RAGPipeline

pipeline = RAGPipeline()

while True:
    query = input("\nEnter your query: ")
    if query.lower() in ["exit", "quit"]:
        print("Goodbye ")
        break

    answer = pipeline.run(query)
    print("\nFinal Answer:")
    print(answer)