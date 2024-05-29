# cish

A "C"-ish compiler and interpreter targeted to accompany my RISC-V Logisim videos.

A playlist to the Logisim videos can be found here: https://www.youtube.com/watch?v=Z7LHCMTc0gI&list=PLM8YDhk_PWu0pdBNHMMSiBm8CEkCQ94T8

## Inspiration
Credit is given to @TsodingDaily https://www.youtube.com/@TsodingDaily/playlists for the inspiration to write this compiler. While I took a different approach, I used many of his techniques. I only wish I could code on camera and it not be a hot mess. The Logisim stuff is easy enough, but I don't know how he does it.

Also, the startup for this work was not mine. Credit ChatGPT. The dialog for the code launch off point is here: https://chatgpt.com/share/de4f17d0-7269-4ec8-bf5a-da94a1e72347. While it did give me a good start, firstly it was not bug-free. Second, I wound up restructuring the parser and interpreter quite a bit. The lexer was nearly perfect.

Also note that I made a first attempt to build a compiler for the HackCPU, which is located at https://github.com/chuckb/hackc, but I never finished. This is an attempt to remedy that.