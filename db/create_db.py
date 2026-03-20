from datetime import date
from db.models import AuthorORM, BookORM
from db.database import Base, engine, SessionCreator


def create_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def insert_data():
    with SessionCreator() as conn:
        authors = [
            AuthorORM(
                name="Jane Austen", 
                bio="English novelist known primarily for her six major novels, which interpret, critique, and comment upon the British landed gentry at the end of the 18th century."
            ),
            AuthorORM(
                name="George Orwell", 
                bio="English novelist, essayist, and critic, famous for his lucid prose and social criticism, particularly in '1984' and 'Animal Farm'."
            ),
            AuthorORM(
                name="Mary Shelley", 
                bio="English novelist who wrote the Gothic novel 'Frankenstein', often considered the first true work of science fiction."
            ),
            AuthorORM(
                name="Leo Tolstoy", 
                bio="Russian writer who is regarded as one of the greatest authors of all time, best known for the epics 'War and Peace' and 'Anna Karenina'."
            ),
            AuthorORM(
                name="Virginia Woolf", 
                bio="English writer and a pioneer in the use of stream of consciousness as a narrative device, central to 20th-century modernism."
            ),
            AuthorORM(
                name="Gabriel García Márquez", 
                bio="Colombian novelist and Nobel laureate who popularized the 'magical realism' genre, most notably in 'One Hundred Years of Solitude'."
            ),
            AuthorORM(
                name="Toni Morrison", 
                bio="American novelist and Nobel laureate whose work examines the Black female experience within the African American community."
            ),
            AuthorORM(
                name="Franz Kafka", 
                bio="German-speaking Bohemian novelist whose work, featuring isolated protagonists facing bizarre or surrealistic predicaments, defines the 'Kafkaesque'."
            ),
            AuthorORM(
                name="Emily Dickinson", 
                bio="American poet who lived much of her life in isolation and is now widely considered one of the most important figures in American poetry."
            ),
            AuthorORM(
                name="Mark Twain", 
                bio="American writer, humorist, and entrepreneur often called the 'father of American literature', famous for 'The Adventures of Huckleberry Finn'."
            )
        ]
        conn.add_all(authors)
        conn.flush()
        books = [
            # Jane Austen (author_id=1)
            BookORM(
                title="Pride and Prejudice",
                summary="A sparkling comedy of manners that follows the headstrong Elizabeth Bennet and the proud Mr. Darcy as they overcome their social prejudices to find love.",
                publication_date=date(1813, 1, 28),
                author_id=1
            ),
            BookORM(
                title="Emma",
                summary="A clever and meddlesome young woman learns the dangers of interfering in the romantic lives of others while discovering her own feelings.",
                publication_date=date(1815, 12, 23),
                author_id=1
            ),
            # George Orwell (author_id=2)
            BookORM(
                title="1984",
                summary="A chilling dystopian novel set in a totalitarian society ruled by Big Brother, where thoughtcrime is punished and history is constantly rewritten.",
                publication_date=date(1949, 6, 8),
                author_id=2
            ),
            BookORM(
                title="Animal Farm",
                summary="A satirical allegory where farm animals overthrow their human master only to succumb to a new form of tyranny led by the pigs.",
                publication_date=date(1945, 8, 17),
                author_id=2
            ),
            # Mary Shelley (author_id=3)
            BookORM(
                title="Frankenstein",
                summary="A gothic tale about Victor Frankenstein, a scientist who creates a sapient creature in an unorthodox scientific experiment, only to be haunted by his creation.",
                publication_date=date(1818, 1, 1),
                author_id=3
            ),
            # Leo Tolstoy (author_id=4)
            BookORM(
                title="War and Peace",
                summary="A massive epic following five aristocratic families during the Napoleonic Wars, blending historical events with philosophical inquiry.",
                publication_date=date(1869, 1, 1),
                author_id=4
            ),
            BookORM(
                title="Anna Karenina",
                summary="A tragic story of a high-society woman who defies social conventions to pursue an affair with a dashing officer, leading to her eventual downfall.",
                publication_date=date(1877, 1, 1),
                author_id=4
            ),
            # Virginia Woolf (author_id=5)
            BookORM(
                title="Mrs Dalloway",
                summary="A high-modernist novel that explores a single day in the life of Clarissa Dalloway as she prepares for a party in post-WWI London.",
                publication_date=date(1925, 5, 14),
                author_id=5
            ),
            BookORM(
                title="To the Lighthouse",
                summary="A fragmented and poetic narrative focusing on the Ramsay family's visits to the Isle of Skye, exploring the passage of time and family dynamics.",
                publication_date=date(1927, 5, 5),
                author_id=5
            ),
            # Gabriel García Márquez (author_id=6)
            BookORM(
                title="One Hundred Years of Solitude",
                summary="The multi-generational story of the Buendía family in the fictional town of Macondo, where the magical and the mundane are inextricably linked.",
                publication_date=date(1967, 5, 30),
                author_id=6
            ),
            BookORM(
                title="Love in the Time of Cholera",
                summary="A sweeping tale of unrequited love that lasts for over half a century, set against the backdrop of a South American city plagued by cholera.",
                publication_date=date(1985, 1, 1),
                author_id=6
            ),
            # Toni Morrison (author_id=7)
            BookORM(
                title="Beloved",
                summary="A powerful and haunting novel about a former slave who is haunted by the ghost of the daughter she killed to save from a life of bondage.",
                publication_date=date(1987, 9, 16),
                author_id=7
            ),
            BookORM(
                title="Song of Solomon",
                summary="A lyrical narrative following the life of Macon 'Milkman' Dead III as he embarks on a journey to discover his family heritage and sense of self.",
                publication_date=date(1977, 1, 1),
                author_id=7
            ),
            # Franz Kafka (author_id=8)
            BookORM(
                title="The Metamorphosis",
                summary="A surreal novella about Gregor Samsa, a salesman who wakes up one morning to find himself transformed into a giant, monstrous insect.",
                publication_date=date(1915, 10, 1),
                author_id=8
            ),
            BookORM(
                title="The Trial",
                summary="The unsettling story of Josef K., a man arrested and prosecuted by a remote, inaccessible authority for a crime that is never revealed.",
                publication_date=date(1925, 4, 1),
                author_id=8
            ),
            # Emily Dickinson (author_id=9)
            BookORM(
                title="The Poems of Emily Dickinson",
                summary="A comprehensive collection of Dickinson's unique, punctuated, and deeply introspective poetry, published largely after her death.",
                publication_date=date(1890, 11, 12),
                author_id=9
            ),
            # Mark Twain (author_id=10)
            BookORM(
                title="The Adventures of Huckleberry Finn",
                summary="A classic American novel following a young boy and an escaped slave as they travel down the Mississippi River on a raft.",
                publication_date=date(1884, 12, 10),
                author_id=10
            ),
            BookORM(
                title="The Adventures of Tom Sawyer",
                summary="A nostalgic tale of boyhood adventures, mischief, and growing up in a small town on the banks of the Mississippi.",
                publication_date=date(1876, 6, 1),
                author_id=10
            ),
            BookORM(
                title="A Connecticut Yankee in King Arthur's Court",
                summary="A satirical time-travel story about an engineer who is transported back to medieval England and attempts to modernize the kingdom.",
                publication_date=date(1889, 1, 1),
                author_id=10
            ),
            BookORM(
                title="Life on the Mississippi",
                summary="A memoir and travelogue that reflects on Twain's days as a steamboat pilot and the changing culture along the great river.",
                publication_date=date(1883, 5, 17),
                author_id=10
            )
        ]
        conn.add_all(books)
        conn.commit()

if __name__ == "__main__":
    create_tables()
    insert_data()