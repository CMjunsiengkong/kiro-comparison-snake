# M3 decision points

`prompts/m3-feature.md` leaves these choices open on purpose. The hidden tests don't check them. For each M3 run, record which ones the agent **asked you about** before coding, which ones it **wrote down** in a plan or spec without asking, and which ones it **decided silently** in code. Never show this file to an agent.

| #  | Decision point                                                                 | Asked | Written down | Silent |
|----|--------------------------------------------------------------------------------|-------|--------------|--------|
| D1 | Where the high score file lives (project folder, home folder, OS app-data folder) |       |              |        |
| D2 | File format (plain number, JSON, ...)                                          |       |              |        |
| D3 | What happens if the file is corrupt or can't be read or written               |       |              |        |
| D4 | When the high score is saved (at game over, as soon as it's beaten, on quit)   |       |              |        |
| D5 | The speed-up rule (per food or every N points, by how much)                    |       |              |        |
| D6 | A maximum speed, so the game stays playable                                    |       |              |        |
| D7 | Where the high score shows on screen (score bar, game-over screen, "New high score!") |       |              |        |
| D8 | Keeping tests and git away from the real high score file (temp paths, `.gitignore`) |       |              |        |

## Answering rule

When an agent asks about one of these, answer with the **"Reference answer"** below so every run builds the same game. For anything not listed here, reply "Your choice." Don't add requirements of your own.

| #  | Reference answer                                                       |
|----|------------------------------------------------------------------------|
| D1 | A file in the user's home folder: `~/.snake_highscore`                 |
| D2 | Plain text, just the number                                            |
| D3 | Treat it as 0 and keep playing; never crash                            |
| D4 | At game over                                                           |
| D5 | +1 move per second for every 5 points                                  |
| D6 | Cap at 20 moves per second                                             |
| D7 | Show "Best: N" next to the score, and "New high score!" on the game-over screen when it's beaten |
| D8 | Yes, tests must not touch the real file                                |
