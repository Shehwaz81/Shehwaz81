"""Builds the animated SVGs for the profile README.  Run: python3 build.py

GitHub strips CSS and JS from READMEs, but an SVG shown through <img> keeps its
own <style>, so all motion lives inside the SVGs. No web fonts load in that
mode, hence the system font stacks.
"""
import random
from pathlib import Path

THEMES = {
    "light": dict(ink="#1f2328", muted="#59636e", body="#1b1f24", body_edge="#1b1f24"),
    "dark": dict(ink="#f0f6fc", muted="#9198a1", body="#010409", body_edge="#3d444d"),
}
SANS = "system-ui,-apple-system,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"
EASE_OUT = "cubic-bezier(0.23,1,0.32,1)"
REDUCED = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"

# ---------- cube: a real scramble, solved move by move ----------
FACE = {(0, 1, 0): "#f4f5f7", (0, -1, 0): "#ffd60a", (0, 0, 1): "#2db55d",
        (0, 0, -1): "#2f6fed", (1, 0, 0): "#e5383b", (-1, 0, 0): "#ff8a1f"}
VISIBLE = [(0, 1, 0), (0, 0, 1), (1, 0, 0)]  # top, front, right


def rot(v, axis, k):
    x, y, z = v
    for _ in range(k % 4):
        x, y, z = [(x, -z, y), (z, y, -x), (-y, x, z)][axis]
    return (x, y, z)


def solved():
    s = {}
    for p in [(x, y, z) for x in (-1, 0, 1) for y in (-1, 0, 1) for z in (-1, 0, 1)]:
        for n in FACE:
            if all(p[i] == n[i] for i in range(3) if n[i]):
                s[(p, n)] = FACE[n]
    return s


def turn(state, move):
    axis, layer, k = move
    return {((rot(p, axis, k), rot(n, axis, k)) if p[axis] == layer else (p, n)): c
            for (p, n), c in state.items()}


def cube_states(n_moves=20, seed=9):
    rng, moves = random.Random(seed), []
    while len(moves) < n_moves:
        m = (rng.randrange(3), rng.choice((-1, 1)), rng.choice((1, 2, 3)))
        if not moves or m[:2] != moves[-1][:2]:
            moves.append(m)
    state = solved()
    for m in moves:
        state = turn(state, m)
    states = [state]
    for axis, layer, k in reversed(moves):  # the solve is the scramble undone
        states.append(turn(states[-1], (axis, layer, 4 - k)))
    assert states[-1] == solved(), "cube did not end solved"
    assert states[0] != solved()
    return states


# One loop: 0-0.6s scramble, 2-11s solve (9 seconds), then rest. Plays 3 times and stops solved.
CYCLE, SCRAMBLE_END, SOLVE_START, SOLVE_LEN, PLAYS = 14.0, 0.6, 2.0, 9.0, 3


def pct(t):
    return f"{100 * t / CYCLE:.3f}%"


def hero(t):
    states = cube_states()
    n = len(states) - 1
    cx, cy, a = 734, 100, 30

    def proj(x, y, z):
        return f"{cx + 0.866 * a * (x - z):.1f},{cy + 0.5 * a * (x + z) - a * y:.1f}"

    css, polys = [], []
    for i, key in enumerate(k for k in solved() if k[1] in VISIBLE):
        p, nrm = key
        u, v = [ax for ax in range(3) if not nrm[ax]]
        c = [p[j] + 0.5 * nrm[j] for j in range(3)]
        pts = []
        for su, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            q = c[:]
            q[u] += 0.36 * su
            q[v] += 0.36 * sv
            pts.append(proj(*q))
        frames = [(0, states[n][key]), (SCRAMBLE_END, states[0][key])]
        for k in range(1, n + 1):
            if states[k][key] != states[k - 1][key]:
                tk = SOLVE_START + SOLVE_LEN * k / n
                frames += [(tk - 0.1, states[k - 1][key]), (tk, states[k][key])]
        frames.append((CYCLE, states[n][key]))
        css.append(f"@keyframes s{i}{{" + "".join(f"{pct(ts)}{{color:{col}}}" for ts, col in frames) + "}")
        css.append(f".s{i}{{animation:s{i} {CYCLE}s linear {PLAYS} forwards}}")
        polys.append(f'<polygon class="s{i}" color="{states[n][key]}" points="{" ".join(pts)}"/>')

    e = 1.5
    hexagon = " ".join(proj(*q) for q in [(-e, e, -e), (e, e, -e), (e, -e, -e), (e, -e, e), (-e, -e, e), (-e, e, e)])

    # stopwatch: digits are vertical strips moved in steps
    ty, lh, xs = 232, 34, (708, 742, 760)  # seconds, tenths, hundredths
    strip = lambda x: "".join(f'<text x="{x}" y="{ty + j * lh}">{j}</text>' for j in range(10))
    a0, a1 = pct(SOLVE_START), pct(SOLVE_START + SOLVE_LEN)
    secs = "".join(f"{pct(SOLVE_START + k)}{{transform:translateY(-{k * lh}px)}}" for k in range(1, 10))
    css += [
        f"@keyframes secs{{0%{{transform:translateY(0)}}{secs}100%{{transform:translateY(-{9 * lh}px)}}}}",
        f"@keyframes spin{{to{{transform:translateY(-{10 * lh}px)}}}}",
        f"@keyframes run{{0%{{opacity:0}}{a0}{{opacity:1}}{a1},100%{{opacity:0}}}}",
        f"@keyframes rest{{0%{{opacity:1}}{a0}{{opacity:0}}{a1},100%{{opacity:1}}}}",
        f".secs{{animation:secs {CYCLE}s step-end {PLAYS} forwards}}",
        f".t1{{animation:spin 1s steps(10) infinite,run {CYCLE}s step-end {PLAYS} forwards}}",
        f".t2{{animation:spin .1s steps(10) infinite,run {CYCLE}s step-end {PLAYS} forwards}}",
        f".rest{{animation:rest {CYCLE}s step-end {PLAYS} forwards}}",
        "@keyframes rise{from{opacity:0;transform:translateY(12px)}}",
        "@keyframes arrive{from{opacity:0;transform:scale(.96)}}",
        f".l1,.l2,.l3{{animation:rise .6s {EASE_OUT} both}}.l2{{animation-delay:70ms}}.l3{{animation-delay:130ms}}",
        f".cube{{transform-box:fill-box;transform-origin:center;animation:arrive .7s {EASE_OUT} .15s both}}",
        REDUCED,
    ]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 250" role="img" aria-labelledby="h">
<title id="h">Shehwaz Saini. Co-founder of Lemma. I build software people use. A Rubik's cube solves itself in 9 seconds.</title>
<style>{"".join(css)}</style>
<clipPath id="win"><rect x="690" y="{ty - 26}" width="90" height="{lh}"/></clipPath>
<g font-family="{SANS}" fill="{t['ink']}">
<text class="l1" x="0" y="92" font-size="68" font-weight="700" letter-spacing="-2.4">Shehwaz Saini</text>
<g font-size="34" font-weight="500" letter-spacing="-.7" fill="{t['muted']}">
<text class="l2" x="2" y="150">Co-founder of Lemma.</text>
<text class="l3" x="2" y="194">I build software people use.</text></g></g>
<g class="cube">
<polygon points="{hexagon}" fill="{t['body']}" stroke="{t['body_edge']}" stroke-width="7" stroke-linejoin="round"/>
<g fill="currentColor" stroke="currentColor" stroke-width="5" stroke-linejoin="round">{"".join(polys)}</g>
<g clip-path="url(#win)" font-family="{MONO}" font-size="28" font-weight="600" fill="{t['ink']}" text-anchor="middle">
<g class="secs" transform="translate(0,-{9 * lh})">{strip(xs[0])}</g>
<text x="725" y="{ty}">.</text>
<g class="t1" opacity="0">{strip(xs[1])}</g><g class="t2" opacity="0">{strip(xs[2])}</g>
<g class="rest"><text x="{xs[1]}" y="{ty}">0</text><text x="{xs[2]}" y="{ty}">0</text></g>
</g></g></svg>
'''


if __name__ == "__main__":
    out = Path(__file__).parent / "assets"
    out.mkdir(exist_ok=True)
    for name, theme in THEMES.items():
        (out / f"hero-{name}.svg").write_text(hero(theme))
    print("built", sorted(p.name for p in out.glob("*.svg")))
