# Bug Hunt Lab: Buggy Blackjack

This repo is a small terminal Blackjack game with **lots of planted bugs**:
wrong rules, wrong payouts, crashes, security holes, missing features, weak tests
and an out-of-date README. Your job is to build a squad of Claude Code subagents
that finds and fixes them.

> Note: `README.md` is **wrong on purpose** (that's the docs-writer's job).
> Use this file for the real instructions.

## 1. Setup (2 min)

You need Python 3.8+ and git. Nothing to `pip install`.

```
git clone <this-repo-url>
cd buggy-blackjack
python main.py          # Windows: python main.py  |  Mac/Linux: python3 main.py
```

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

## 3. Build your squad (10 min)

Start Claude Code in this folder (`claude`) and create three project subagents in
`.claude/agents/`:

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
