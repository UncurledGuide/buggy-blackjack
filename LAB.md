# Bug Hunt Lab: Buggy Blackjack

This repo is a small terminal Blackjack game with **lots of planted bugs**:
wrong rules, wrong payouts, crashes, security holes, missing features, weak tests
and an out-of-date README. Your job is to build a squad of Claude Code subagents
that finds and fixes them.

> Note: `README.md` is **wrong on purpose** (that's the docs-writer's job).
> Use this file for the real instructions.

## Purpose: what you'll learn

No coding experience needed. By the end you will have:

1. Built **three Claude Code subagents** (reviewer, test-writer, docs-writer), each a small markdown file that gives Claude a focused job.
2. Run them **in parallel** as a team on a real code change.
3. Used them to **find and fix** about 30 planted bugs, then scored the result.

The point isn't Blackjack. It's learning how to split work across specialized agents.
You don't need to read the Python yourself. Let your agents do that.

## 1. Setup (5 min)

You need three things installed: **git**, **Python 3.8+** and **Claude Code**.
Check them by typing these into a terminal (Terminal on Mac, PowerShell or WSL on Windows):

```
git --version
python3 --version        # Windows: python --version
claude --version
```

If one says "command not found", install it first. For Claude Code, follow
https://docs.claude.com/en/docs/claude-code. Nothing to `pip install`.

Then download the project and start the game:

```
git clone https://github.com/UncurledGuide/buggy-blackjack.git
cd buggy-blackjack
python3 main.py          # Windows: python main.py
```

You should see a menu with `1` play, `2` high scores, `3` quit. Type `3` to leave.

## 2. Play it and spot bugs yourself (5 min)

Menu: `1` play, `2` high scores, `3` quit. In a round: type a bet, then `h` (hit) or `s` (stand).

Three ways to play:

| Command | What it does |
|---|---|
| `python main.py` | Normal game |
| `python main.py --seed 42` | Same shuffle every time, so you can replay a bug |
| `python main.py --deck "A,K,A,7"` | You choose the cards |

With `--deck`, cards are dealt in this order: **you, dealer, you, dealer**, then any
hits (you first, then the dealer). So `"A,K,A,7"` gives you A + A and the dealer K + 7.

Try these. Each one shows at least one bug:

| Command | Then type | What should happen |
|---|---|---|
| `--deck "A,K,A,7"` | `1`, name, `10`, `s` | Two aces = 12, not 22 |
| `--deck "10,10,7,6,5"` | `1`, name, `10`, `s` | Dealer has 16, so must hit (draws 5 = 21) |
| `--deck "10,10,8,8"` | `1`, name, `10`, `s` | Tie = push, you keep your $10 |
| `--deck "K,10,5,7,6"` | `1`, name, `10`, `h` | You hit to exactly 21. That's not a bust |
| `--deck "A,10,K,7"` | `1`, name, `10` | Blackjack pays 3:2 → balance should be $115 |
| `--deck "J,9,5,7"` | `1`, name, `10` | J + 5 = 15 |
| `--deck "K,7"` | `1`, name, `10` | Short deck. Game should reshuffle, not crash |
| *(no flags)* | bet `abc` | Should ask again, not crash |
| *(no flags, first run)* | `2` | Should say "no scores yet", not crash |

Also look for: things the dealer shows that it shouldn't, messages that don't match
your balance, what happens at $0, and whether two new games deal the same cards.

<details>
<summary>Stuck? Hints (open one at a time)</summary>

- **Hint 1:** Bugs come in four flavors: wrong rules, wrong payouts, crashes and security holes. Test one of each.
- **Hint 2:** Security bugs hide in anything that takes **input from a user**: the bet and the player name.
- **Hint 3:** Try typing odd things: a letter, a negative number, `0`, a huge number, a name with `/` or `..` in it.
- **Hint 4:** Give your reviewer agent a ranking job ("most severe first") and tell it to cite file and line.
- **Hint 5:** If your agent isn't being used, check the `description` line in its file. Claude picks agents based on it.

</details>

## 3. Build your squad (10 min)

Start Claude Code in this folder (type `claude`). The easiest way to make an agent is to
type `/agents`, choose **Create new agent**, and pick **Project**. Or just ask Claude to
write the files for you. Create three project subagents in `.claude/agents/`:

- **reviewer**: read-only (`Read, Grep, Glob`). Finds bugs, security risks and confusing code, ranked by severity.
- **test-writer**: writes and runs tests (`python -m unittest`), then reports what passed and failed.
- **docs-writer**: makes the README match what the code really does.

Restart Claude Code once (`/exit`, then `claude`) so it loads the new agents.

## 4. Make a change, then orchestrate (10 min)

The squad reviews "my latest changes" (`git diff`). Apply the new feature:

```
git apply lab/double-down.patch
git diff
```

Then paste this into Claude Code:

> Review my latest changes as a team. Run the reviewer and test-writer in parallel,
> then have the docs-writer fix anything out of date. Summarize what each agent found.

Bonus: ask the squad to review **the whole project**, not just the diff, and fix what it finds.

## 5. Score your squad

The `answers` branch has the full bug list and a test suite that only passes when
the bugs are fixed:

```
git checkout answers -- tests/test_answer_key.py
python -m unittest -v
```

Count how many tests pass. No peeking at `ANSWER_KEY.md` until the end!
