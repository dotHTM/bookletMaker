# bookletMaker

A tool for ordering pages for printing varied signatures for printing and binding books.



## Signature Building by Hand

To order a group of pages into a signature, you can visualize the stack of paper and where the page numbers must go.

Each sheet will have 4 pages printed to it, and each sheet will have one half read in sequence, front & back, then at the turn-around point half way, reversed back to the first sheet.

For page numbers 1-16, we will have 4 sheets of paper, with numbers above and below representing page content printed to one side or another. Imagine a booklet laid out in front of you on a table, turned to the middle of the signature:

```
               → → → → → →                     → → → → → →
             ↗︎  8       9  ↘︎                 ↗︎  24     25  ↘︎
            ↑ ======Ø======                 ↑ ======Ø====== ↓
            ↑   7      10   ↓               ↑   23     26   ↓
            ↑               ↓               ↑               ↓
            ↑   6      11   ↓               ↑   22     27   ↓
            ↑ ======Ø====== ↓               ↑ ======Ø====== ↓
            ↑   5      12   ↓               ↑   21     28   ↓
            ↑               ↓               ↑               ↓
            ↑   4      13   ↓               ↑   20     29   ↓
            ↑ ======Ø====== ↓               ↑ ======Ø====== ↓
            ↑   3      14   ↓               ↑   19     30   ↓
Reading     ↑               ↓               ↑               ↓
Direction   ↑   2      15   ↓               ↑   18     31   ↓
            ↑ ======Ø====== ↓               ↑ ======Ø====== ↓
                1      16    ↘︎             ↗︎    17     32   ↘︎
                               → → → → → →                    → → →
               Signature 1                     Signature 2
```

Because the top and bottom sides of these sheets are reversed in reading direction respective to eachother, we need to reverse half, either the evens or the odds.

Keeping a list of duplexed sheets, each page will appear in this order to assemble the first signature:

| Left | Right |
|------|-------|
|   16 |     1 |
|    2 |    15 |
|   14 |     3 |
|    4 |    13 |
|   12 |     5 |
|    6 |    11 |
|   10 |     7 |
|    8 |     9 |

Using a filename template, and a program that can read CSV and layout images on a printed page, we can now arbitrarily size and distribute pages to signatures!

