# Acceptance Test Plan for Compose Module

## A1: Quote Selection

**Given**: Query "What does Lord Henry say about influence?"

**Expected**: At least one quote contains the word "influence" (or a close variant).

**Test**: 
- Retrieve top-k chunks for the query
- Compose answer with quotes
- Verify at least one quote in the result contains "influence" (case-insensitive)

---

## A2: Citation References

**Given**: Query "How is Achilles' anger framed in Book 1?"

**Expected**: Answer includes [1] and [1] references a quote from early book content.

**Test**:
- Compose answer for the query
- Verify answer text contains reference markers like [1], [2], [3]
- Verify citations list includes corresponding entries
- For Iliad queries, verify that cited chunks reference Book 1 or early content

---

## A3: Conservative Fallback

**Given**: Query with no relevant chunk score exceeding a threshold

**Expected**: Answer returns a cautious message and still lists the top quote candidates.

**Test**:
- Use a query that retrieves low-scoring chunks (e.g., very specific or out-of-domain question)
- Compose answer
- Verify answer contains a cautious statement (e.g., "The text suggests...", "Based on available passages...")
- Verify quotes list is non-empty (shows top candidates even if weak)

---

## A4: Quote Diversity (MMR-lite)

**Given**: Multiple retrieved chunks with similar content

**Expected**: Selected quotes are diverse (not near-duplicates).

**Test**:
- Retrieve chunks for a query that returns similar passages
- Compose answer with max_quotes=3
- Verify selected quotes are not near-identical (e.g., edit distance > 50% of average quote length)

---

## A5: Answer Length

**Given**: Any query

**Expected**: Answer is 2–4 sentences, ~100–140 words.

**Test**:
- Compose answers for multiple queries
- Verify word count is between 80–160 words (allowing some variance)
- Verify sentence count is between 2–5

---

## A6: Attribution (Token Overlap)

**Given**: Composed answer with quotes

**Expected**: Each answer sentence shares ≥2 content words with at least one quote.

**Test**:
- Compose answer for a query
- For each sentence in the answer:
  - Extract content words (remove stopwords)
  - Check overlap with content words from all quotes
  - Verify overlap count ≥ 2 for at least one quote

---

## Notes

- These tests are designed to run after implementing the compose module
- Some tests require manual inspection (e.g., A2 for verifying Book 1 references)
- Consider automating A1, A3, A4, A5, A6 with unit tests in `tests/test_compose.py` (to be created)

