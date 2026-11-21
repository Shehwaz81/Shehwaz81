# Product

<!-- impeccable:product-schema 1 -->

This repository is public, so this file is too. Keep private facts out of it.

## Platform

web

## Users

Confirmed by Shehwaz (Nov 2026): engineers, investors, accelerator reviewers and recruiters.

They land on github.com/Shehwaz81 from a link (a résumé, an application, a hackathon, a repo) and scan the profile for well under a minute to decide whether he builds real things. That arrival path and time budget are inferred, not confirmed.

## Product Purpose

The profile README for github.com/Shehwaz81: the first thing anyone sees on Shehwaz Saini's GitHub profile.

Success, as he stated it: the visitor remembers him, and clicks through to his projects, Lemma first.

## Positioning

A builder who ships software people use: co-founder of Lemma, plus tools adopted by a school charity drive, a company and a robotics team. This comes from his own notes ("a builder first", "valuable software that people use").

Open: the hero line "I build software people use" is a draft he has seen but not explicitly approved.

## Operating Context

- GitHub renders `README.md` from the default branch of `Shehwaz81/Shehwaz81` at the top of the profile, above the pinned repositories.
- The README column is about 846px wide on desktop and far narrower on phones. Images scale with it.
- Visitors use GitHub's light or dark theme.
- Profile repo changes go live only once they reach `main`.

## Capabilities and Constraints

- GitHub strips CSS, JavaScript, `class` and `style` attributes, and iframes from READMEs. Only a small HTML subset survives (`picture`, `source`, `img`, `br`, `details`, `sub` and similar).
- Motion is possible only inside SVG files shown through `<img>`. Those keep their own `<style>` and CSS animations, but cannot load web fonts or outside files, run scripts, or respond to hover or clicks. An image can carry at most one link.
- Light and dark versions are separate SVG files switched with `<picture>` and `prefers-color-scheme`.
- Text inside an SVG shrinks with the image on phones, so anything essential must also exist as real README text.
- `build.py` (Python standard library only) generates `assets/*.svg`. Run `python3 build.py` after changing it.
- Names: Lemma; Hearth (its repo is `Brasle`); Sayara (its repo is `AI-Devfest`, on a teammate's account); Alti Guard; ACS Hacks.

### What may be public (confirmed Nov 2026)

- Allowed: his email address; his school, grade and city; awards and competition results.
- Not allowed: Lemma numbers. User counts, daily growth and the number of partner schools stay off the profile.
- Open: whether Lemma's non-numeric facts (University of Waterloo permission, League of Innovators admission) may appear.

## Brand Commitments

- Name: Shehwaz Saini. Handle: Shehwaz81. Links: lemmaprep.ca, shehwazsaini.com.
- First person, plain statements.
- His stated preference for design work done for him: unique, human, non-generic.

## Evidence on Hand

- Public repos: `Brasle` (Hearth), `alti-guard`, `acscandrive`, `WRO-Simulation`, `Signify`, `ACS-Hacks`, and `alialfoaady-cm/AI-Devfest` (Sayara).
- Hearth's Devpost page: devpost.com/software/brasle.
- Dated competition results, listed in the README.
- Figures that are fine to show: 23,533 cans collected against a 20,000 goal (2026 Can Drive); over $10,000 raised for hackathons he organized; a 9-second 3×3 cube solve.
- Not on hand, so never invent: testimonials, press, project photos or screenshots, GitHub stars or follower counts worth showing. The Lemma repo is private.

## Product Principles

1. Every claim is a fact he can back with a link, a repo or a dated result.
2. Be remembered first, then send people to the work, Lemma before anything else.
3. Lemma leads the story without its numbers.
4. The README must read completely as plain text, with images off and on a phone.
5. Remove a claim the moment it goes stale; the previous README failed by being out of date.

## Accessibility & Inclusion

- Every image has alt text that carries its content.
- Animated SVGs stop moving for visitors who ask for reduced motion.
- No information lives only inside an image.
