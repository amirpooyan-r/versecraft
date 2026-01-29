class MockBook {
  const MockBook({required this.id, required this.name});

  final String id;
  final String name;
}

const List<MockBook> mockBooks = [
  MockBook(id: 'gen', name: 'Genesis'),
  MockBook(id: 'psa', name: 'Psalms'),
  MockBook(id: 'jhn', name: 'John'),
];

MockBook? findMockBook(String id) {
  for (final book in mockBooks) {
    if (book.id == id) {
      return book;
    }
  }
  return null;
}

List<int> mockChapters() => List<int>.generate(5, (index) => index + 1);

List<int> mockVerses() => List<int>.generate(30, (index) => index + 1);
