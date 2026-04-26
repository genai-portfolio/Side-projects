from recommendation_engine import RecommendationEngine
import sys

def display_recommendations(recommendations, method_name):
    """Display recommendations in a formatted way"""
    if not recommendations:
        print(f"No {method_name} recommendations found.")
        return
    
    print(f"\n{method_name.capitalize()} Recommendations:")
    print("-" * 50)
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['title']}")
        print(f"   Author: {rec['author']}")
        print(f"   Year: {rec['year']}")
        print(f"   Score: {rec['score']:.3f}")
        print(f"   Publisher: {rec['publisher']}")
        print()

def interactive_mode(engine):
    """Run in interactive mode"""
    print("\n" + "="*60)
    print("INTERACTIVE BOOK RECOMMENDATION SYSTEM")
    print("="*60)
    print("Commands:")
    print("1. Type a book title to get recommendations")
    print("2. Type 'list' to see available books")
    print("3. Type 'search <keyword>' to search for books")
    print("4. Type 'info <book title>' to get book details")
    print("5. Type 'exit' to quit")
    print("="*60)

    while True:
        user_input = input("\nEnter command or book title: ").strip()

        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        elif user_input.lower() == 'list':
            books = engine.get_available_books(limit=20)
            print("\nAvailable Books (showing first 20):")
            for i, title in enumerate(books, 1):
                print(f"{i}. {title}")
        elif user_input.lower().startswith('search '):
            keyword = user_input[7:]
            results = engine.search_books(keyword)
            if results:
                print(f"\nSearch results for '{keyword}':")
                for r in results:
                    print(f"- {r['title']} by {r['author']} ({r['year']})")
            else:
                print("No matching books found.")
        elif user_input.lower().startswith('info '):
            book_title = user_input[5:]
            info = engine.get_book_info(book_title)
            if info:
                print(f"\nTitle: {info['title']}")
                print(f"Author: {info['author']}")
                print(f"Year: {info['year']}")
                print(f"Publisher: {info['publisher']}")
                print(f"Image URL: {info['image_url']}")
            else:
                print("Book not found.")
        else:
            # Show recommendations for entered book title
            for method in ['collaborative', 'content', 'hybrid']:
                recs = engine.get_recommendations(user_input, method=method)
                display_recommendations(recs, method)

def main():
    engine = RecommendationEngine()

    # Try loading pre-trained models, if not found, train them
    if not engine.load_trained_models():
        print("\nNo trained models found. Training now...")
        if not engine.train_models():
            print("Model training failed. Exiting.")
            sys.exit(1)

    # Start interactive mode
    interactive_mode(engine)

if __name__ == "__main__":
    main()
