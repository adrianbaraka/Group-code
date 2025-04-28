% ------------------------------------------------------------------
% A high-quality Library Catalog KB in Prolog
% ------------------------------------------------------------------

:- dynamic
    borrowed/3.    % borrowed(BookID, Borrower, Date)

%-------------------------------------------------------------------
% 1. ENTITIES (Authors, Publishers, Genres, Books)
%-------------------------------------------------------------------

% Authors: author(ID, Name, BirthYear, Country)
author(1,  'George Orwell',            1903, 'United Kingdom').
author(2,  'Harper Lee',               1926, 'United States').
author(3,  'J.K. Rowling',             1965, 'United Kingdom').
author(4,  'J.R.R. Tolkien',           1892, 'United Kingdom').
author(5,  'F. Scott Fitzgerald',      1896, 'United States').
author(6,  'Jane Austen',              1775, 'United Kingdom').
author(7,  'Brian W. Kernighan',       1942, 'United States').
author(8,  'Dennis M. Ritchie',        1941, 'United States').
author(9,  'Donald E. Knuth',          1938, 'United States').
author(10, 'Robert C. Martin',         1952, 'United States').
author(11, 'Eric Matthes',             1980, 'United States').
author(12, 'Richard O''Keefe',         1956, 'Australia').

% Publishers: publisher(ID, Name, Country)
publisher(1,  'Penguin Random House',     'United States').
publisher(2,  'Bloomsbury Publishing',    'United Kingdom').
publisher(3,  'HarperCollins',            'United States').
publisher(4,  'Prentice Hall',            'United States').
publisher(5,  'Addison-Wesley',           'United States').
publisher(6,  'No Starch Press',          'United States').
publisher(7,  'University of Cambridge',  'United Kingdom').

% Genres: genre(ID, Name)
genre(1,  'Dystopian').
genre(2,  'Classic').
genre(3,  'Fantasy').
genre(4,  'Science Fiction').
genre(5,  'Historical Fiction').
genre(6,  'Romance').
genre(7,  'Drama').
genre(8,  'Programming').
genre(9,  'Algorithms').
genre(10, 'Software Engineering').
genre(11, 'Data Structures').

% Books: book(ID, Title, AuthorID, PublisherID, Year)
book(1,  '1984',                                  1, 1, 1949).
book(2,  'Animal Farm',                          1, 1, 1945).
book(3,  'To Kill a Mockingbird',                2, 3, 1960).
book(4,  'Harry Potter and the Sorcerer''s Stone', 3, 2, 1997).
book(5,  'The Hobbit',                           4, 2, 1937).
book(6,  'The Great Gatsby',                     5, 3, 1925).
book(7,  'Pride and Prejudice',                  6, 1, 1813).
book(8,  'Harry Potter and the Chamber of Secrets', 3, 2, 1998).
book(9,  'Harry Potter and the Prisoner of Azkaban',3, 2, 1999).
book(10, 'Sense and Sensibility',                6, 1, 1811).

% Coding & CS books
book(11, 'The C Programming Language',           7, 4, 1978).
book(12, 'The Unix Programming Environment',      8, 4, 1984).
book(13, 'The Art of Computer Programming',       9, 5, 1968).
book(14, 'Clean Code',                            10,5, 2008).
book(15, 'Python Crash Course',                   11,6, 2015).
book(16, 'Learn Prolog Now!',                     12,7, 2006).

% Book–Genre links: book_genre(BookID, GenreID)
book_genre(1,  1).   book_genre(1,  4).
book_genre(2,  1).
book_genre(3,  2).   book_genre(3,  7).
book_genre(4,  3).
book_genre(5,  3).
book_genre(6,  2).
book_genre(7,  2).   book_genre(7,  5). book_genre(7,  6).
book_genre(8,  3).
book_genre(9,  3).
book_genre(10, 2).   book_genre(10, 5).

% Coding genres
book_genre(11, 8). book_genre(11, 11).
book_genre(12, 8).
book_genre(13, 8). book_genre(13, 9).
book_genre(14, 10).
book_genre(15, 8).
book_genre(16, 8). book_genre(16, 11).

%-------------------------------------------------------------------
% 2. LOAN MANAGEMENT
%-------------------------------------------------------------------

% List all available books
available_book(Title) :-
  book(ID, Title, _, _, _),
  \+ borrowed(ID, _, _).

% check out a book (record the date as an atom or date/3 term)
checkout(Title, Borrower, date(Year,Month,Day)) :-
    book(ID, Title, _, _, _),
    \+ borrowed(ID, _, _),
    assertz(borrowed(ID, Borrower, date(Year,Month,Day))).

% return a book
return_book(Title, Borrower) :-
  book(ID, Title, _, _, _),
  borrowed(ID, Borrower, _),
  retract(borrowed(ID, Borrower, _)).

% is a book currently available?
available(Title) :-
  book(ID, Title, _, _, _),
  \+ borrowed(ID, _, _).
  
% List all currently borrowed books. 
borrowed_book(Title, Borrower, Date) :-
  borrowed(BookID, Borrower, Date),
  book(BookID, Title, _, _, _).

% who has borrowed a given book?
borrowed_by(Title, Borrower) :-
  book(ID, Title, _, _, _),
  borrowed(ID, Borrower, _).

% list all books on loan by a borrower
loans_of(Borrower, Title) :-
  borrowed(ID, Borrower, _),
  book(ID, Title, _, _, _).

% Count the number of days the book has been borrowed. 
days_between(date(Y1,M1,D1), date(Y2,M2,D2), Days) :-
    date_time_stamp(date(Y1,M1,D1,0,0,0,0,-,-), T1),
    date_time_stamp(date(Y2,M2,D2,0,0,0,0,-,-), T2),
    SecDiff is T2 - T1,
    Days is round(SecDiff / 86400).
  
% Check overdue
is_overdue(Title, Borrower, BorrowDate, DaysOverdue) :-
    borrowed(BookID, Borrower, BorrowDate),
    book(BookID, Title, _, _, _),
    get_time(NowStamp),
    stamp_date_time(NowStamp, date(CurrentY,CurrentM,CurrentD,_,_,_,_,_,_), 'UTC'),
    days_between(BorrowDate, date(CurrentY,CurrentM,CurrentD), DaysBorrowed),
    DaysBorrowed > 14,  % Threshold: 14 days
    DaysOverdue is DaysBorrowed - 14.
  
% List all overdue books
list_overdue :-
    is_overdue(Title, Borrower, BorrowDate, DaysOverdue),
    format('~nBorrower: ~w~nBook: ~w~nBorrowed On: ~w~nDays Overdue: ~w~n-----------------', 
          [Borrower, Title, BorrowDate, DaysOverdue]),
    fail.
list_overdue.

%-------------------------------------------------------------------
% 3. BASIC QUERY RULES
%-------------------------------------------------------------------

% books by a given author
book_by_author(AuthorName, Title) :-
  author(AID, AuthorName, _, _),
  book(_, Title, AID, _, _).

% books in a given genre
books_in_genre(GenreName, Title) :-
  genre(GID, GenreName),
  book_genre(BID, GID),
  book(BID, Title, _, _, _).

% books published between two years (inclusive)
books_between_years(Y1, Y2, Title) :-
  book(_, Title, _, _, Year),
  Year >= Y1,
  Year =< Y2.

% count how many books an author has written
count_books_by_author(AuthorName, Count) :-
  author(AID, AuthorName, _, _),
  findall(BID, book(BID, _, AID, _, _), BIDs),
  length(BIDs, Count).

% authors with more than N books
prolific_author(AuthorName, N) :-
  count_books_by_author(AuthorName, Count),
  Count > N.

% recommend books in the same genre as a given title
recommend_same_genre(Title, RecTitle) :-
  book(BID, Title, _, _, _),
  book_genre(BID, GID),
  book_genre(OtherID, GID),
  OtherID \= BID,
  book(OtherID, RecTitle, _, _, _).
  
publisher_country_for_book(Title, Country) :-
  book(_, Title, _, PubID, _),
  publisher(PubID,_, Country).

%-------------------------------------------------------------------
% 4. ADVANCED QUERY RULES
%-------------------------------------------------------------------

% co-authors: two authors who share at least one book
co_authors(AName1, AName2, Title) :-
  book(BID, Title, AID1, _, _),
  book(BID, Title, AID2, _, _),
  AID1 \= AID2,
  author(AID1, AName1, _, _),
  author(AID2, AName2, _, _).

% most popular genre by number of books
count_books_in_genre(GenreName, Count) :-
  genre(GID, GenreName),
  findall(BID, book_genre(BID, GID), L),
  length(L, Count).

most_popular_genre(GenreName) :-
  findall(Count-Name, (count_books_in_genre(Name,Count)), Pairs),
  keysort(Pairs, Sorted),
  reverse(Sorted, [ _Max-GenreName | _ ]).


