# The Spaghetti Test: "Maestra Ottavia" Edition

Five text-to-video prompts. Each one is harder than the last and tests the same things the "eating spaghetti" meme tests: **hands, fork, noodle physics, chewing, identity stability**. The subject is an original character, not a celebrity.

Every prompt below is **self-contained and copy-paste ready**: the character, setting and dish are written out in full each time, so the model gets the same description at every level, and identity drift is the model's fault, not the prompt's.

---

## Identity anchors (what to check in every clip)

These details are chosen because models tend to lose them. Check all of them in the first frame and the last frame.

| Anchor | Value |
|---|---|
| Hair | Silver, loose chignon, two strands loose at the temples |
| Face mark | Small mole above the **left corner of her mouth (her left, viewer's right)** |
| Lips | Bold crimson lipstick |
| Hands | Three thin gold rings on the **right** hand only; fork is always in the right hand |
| Clothing | Plum velvet shawl, cream silk blouse, gold cameo brooch at the throat |
| Room | Red-and-white checked cloth, straw-wrapped Chianti bottle, blue-and-yellow tile wall, faded *Carmen* poster |

## What each level adds

| | L1 | L2 | L3 | L4 | L5 |
|---|:-:|:-:|:-:|:-:|:-:|
| Camera | locked | locked | slow push-in | lateral dolly | handheld |
| Fork motion | held | twirl | twirl + lift | twirl + gesture | fast twirl |
| Noodle physics | resting | wrapping | slurp | swinging strand | splash + chin slap |
| Mouth | closed | closed | bite + chew | chew + short speech | laugh + lip-synced dialogue |
| People | 1 | 1 | 1 | 2 | 2 + diners |
| Extra | steam | — | napkin, sauce on lip | wine pour | sauce stains, audio |
| Length | 5 s | 6 s | 8 s | 10 s | 10–15 s |

---

## Level 1 — The Still Portrait

**Prompt:**
> Static medium shot, locked-off tripod, eye level, 50mm lens, shallow depth of field. A 72-year-old retired opera singer named Ottavia sits alone at a small table in a tiny, four-table trattoria in the Quartieri Spagnoli, Naples. She has silver hair swept up into a loose chignon with two strands loose at the temples, a strong Roman nose, deep laugh lines, dark brown eyes, a small mole above the left corner of her mouth, and bold crimson lipstick. She wears a plum velvet shawl over a cream silk blouse with a gold cameo brooch at the throat, and three thin gold rings on her right hand. In front of her: a chipped white plate of spaghetti al pomodoro with fresh basil and grated Parmigiano, untouched, steam rising. She holds a silver four-tined fork loosely in her right hand, its tips resting on the rim of the plate; her left hand lies flat on the red-and-white checked tablecloth. Behind her: a blue-and-yellow hand-painted tile wall and a faded 1970s *Carmen* opera poster. A straw-wrapped Chianti bottle with a candle stub stands on the table. Warm afternoon light from an open doorway on the left. She looks down at the plate, smiles softly and takes one slow breath. Nothing else moves. Photorealistic, 24fps, 5 seconds.

**Negative prompt:** extra fingers, fused fingers, deformed hands, bent fork, melted cutlery, cartoon, looping steam, text artifacts.

**What it tests:** baseline identity, hand anatomy at rest, a rigid object held in a hand, spaghetti that reads as individual strands.

**Failures to watch for:**
- **Hand anatomy:** 4 or 6 fingers; fingers fused to the fork handle; rings jump to the left hand or vanish.
- **Fork:** 2, 3 or 5 tines; the fork bends, sinks into the plate or merges with the rim.
- **Pasta as texture:** spaghetti looks like a flat printed pattern, a single blob, or a nest of worms with no separate strands.
- **Micro-drift during the breath:** mole moves or disappears, lipstick changes shade, hair darkens or turns blonde.
- **Steam:** loops visibly, rises from the tablecloth, or stays frozen.

---

## Level 2 — The First Twirl

**Prompt:**
> Static medium close-up on a tripod, slightly above eye level, framed from her chest to the plate. In a tiny four-table trattoria in Naples, Ottavia, a 72-year-old retired opera singer with silver hair in a loose chignon, a small mole above the left corner of her mouth, crimson lipstick, a plum velvet shawl, a cream silk blouse and three gold rings on her right hand, eats spaghetti al pomodoro from a chipped white plate on a red-and-white checked tablecloth. She lowers a silver four-tined fork into the spaghetti with her right hand, presses the tines against the plate and slowly twirls three full turns. Individual strands lift from the plate and wrap around the tines into a neat nest; two or three strands hang loose from it. The pile on the plate visibly gets smaller. She lifts the twirled bite a few centimetres and pauses to admire it. Her left hand stays flat on the tablecloth the whole time. Warm afternoon light from a doorway on the left. Photorealistic, natural speed, 6 seconds.

**Negative prompt:** noodles moving on their own, fork turning into a spoon, two forks, extra hands, wrist rotating 360 degrees.

**What it tests:** fork rotation, strands that stay attached and follow the fork, wrist mechanics, conservation of mass.

**Failures to watch for:**
- **Noodles not attached:** the nest forms by itself, or strands pass through the tines like smoke.
- **Impossible wrist:** the fork spins while the hand stays still, or the wrist turns a full 360°.
- **Mass not conserved:** the nest grows but the pile on the plate stays the same (or grows).
- **Utensil morphing:** the fork becomes a spoon, gains tines, or a second fork appears.
- **The idle hand:** the "resting" left hand creeps, twitches or melts into the checked pattern.

---

## Level 3 — The Bite and the Chew

**Prompt:**
> Medium close-up with a slow dolly push-in from chest level to a tight shot of her face, ending just below the eyes. In a tiny trattoria in Naples, Ottavia, a 72-year-old retired opera singer with silver hair in a loose chignon, deep laugh lines, dark brown eyes, a small mole above the left corner of her mouth, bold crimson lipstick, a plum velvet shawl and a gold cameo brooch, eats spaghetti al pomodoro. Timing: 0–2 s, she lifts a twirled forkful to her mouth with her right hand (three gold rings) and takes the bite; the fork comes out of her mouth empty. 2–4 s, one long strand still hangs from her lips; she slurps it in with a small theatrical flourish and the strand flicks a tiny drop of sauce onto her lower lip. 4–6 s, she chews slowly with her lips closed, jaw moving up and down, cheeks shifting, then swallows and her throat moves. 6–8 s, with her left hand she dabs the corner of her mouth with a white linen napkin and the sauce mark is gone. Warm side light from a doorway on the left. Photorealistic, 8 seconds.

**Negative prompt:** food passing through skin, open-mouth chewing, extra teeth, fork merging with lips, face changing age.

**What it tests:** food entering the mouth (the classic meme failure), chewing mechanics, a shrinking strand, sauce on skin, a second hand with a second object, identity under a big facial deformation, all seen close up.

**Failures to watch for:**
- **Clipping:** pasta goes through the cheek or chin, or disappears a few centimetres before the lips.
- **Fork in the face:** tines merge with teeth or lips; the fork comes out still full.
- **Chewing:** mouth stays open; jaw grinds sideways like a cow; chewing keeps going after the swallow; teeth multiply or turn into a white bar.
- **Slurp:** the strand gets longer instead of shorter, snaps back to the plate, or turns into a different shape.
- **Sauce continuity:** the drop appears before the flick, stays after the napkin passes, or moves around the lip.
- **Identity under deformation:** with the mouth wide open she becomes a younger or different woman; the mole disappears; the push-in changes her bone structure.

---

## Level 4 — Conversation Between Bites

**Prompt:**
> Medium two-shot, slow lateral dolly from left to right that reveals a waiter. A tiny four-table trattoria in the Quartieri Spagnoli, Naples: red-and-white checked tablecloth, blue-and-yellow tile wall, a faded *Carmen* poster, warm afternoon light. Ottavia, a 72-year-old retired opera singer with silver hair in a loose chignon, a small mole above the left corner of her mouth, crimson lipstick, a plum velvet shawl over a cream silk blouse and three gold rings on her right hand, is halfway through a plate of spaghetti al pomodoro. Timing: 0–3 s, the waiter Gennaro enters from the right: a stocky man in his 40s, thick black moustache, short dark hair, white shirt with rolled sleeves, black waistcoat, long white apron. He pours red wine from a straw-wrapped Chianti bottle into her glass; the level rises. 3–7 s, Ottavia keeps twirling spaghetti with her right hand, turns her head toward him and says "Grazie, tesoro," while gesturing with the fork; a long strand dangles from the fork and swings back and forth with the movement. 7–10 s, Gennaro laughs and puts the bottle down; she turns back and eats the bite. Photorealistic, 10 seconds.

**Negative prompt:** merged faces, third arm, wine passing through glass, rigid noodles, plate refilling, changing poster text.

**What it tests:** two people with four hands in frame, a liquid pour, pendulum physics on a moving fork, a head turn that keeps identity, background stability under parallax, plate continuity.

**Failures to watch for:**
- **Identity blending:** Ottavia gets a moustache shadow, Gennaro gets silver hair, or their faces average out during the head turn.
- **Hand count and ownership:** a third arm appears; the bottle hand belongs to nobody; hands swap owners.
- **Wine:** the stream goes through the glass, the level does not rise, the liquid is a solid red rod, or the bottle refills.
- **Swinging strand:** the noodle is rigid like wire, floats against gravity, or stays still while the fork moves.
- **Plate continuity:** the half-eaten plate becomes full again.
- **Short speech:** "Grazie, tesoro" is spoken with a mouth that does not move, or lips move while the jaw is still chewing.
- **Parallax:** the tile pattern slides, the poster text changes, or tables appear and disappear during the dolly.

---

## Level 5 — The Aria at the Table (Full Chaos)

**Prompt:**
> Handheld camera, documentary style, natural shake, moving freely around the table: from a three-quarter front angle into a close-up and back out. A tiny, busy four-table trattoria in the Quartieri Spagnoli, Naples, with a few other diners in the background, a red-and-white checked tablecloth, a blue-and-yellow tile wall, a faded *Carmen* poster and a straw-wrapped Chianti bottle. Ottavia, a 72-year-old retired opera singer with silver hair in a loose chignon, a small mole above the left corner of her mouth, bold crimson lipstick, a plum velvet shawl over a cream silk blouse, a gold cameo brooch and three gold rings on her right hand, sits at the table. Gennaro the waiter stands next to her: stocky, 40s, thick black moustache, white shirt with rolled sleeves, black waistcoat, white apron. Timing: 0–3 s, she twirls a big forkful of spaghetti al pomodoro fast with her right hand; sauce flicks off the strands and lands as small red dots on the tablecloth and on her cream blouse, and the dots stay there. 3–6 s, she says to Gennaro in Italian, clearly lip-synced: "Gennaro! Questo sugo è meglio della Scala!", then throws her head back in a deep, full-bellied laugh. 6–9 s, Gennaro laughs and answers, lip-synced: "Signora, lei lo dice ogni settimana!"; she takes the bite and chews with her lips closed while he talks. 9–12 s, after swallowing, she sings one short, full-voiced operatic note, "Ah!", gesturing with the fork; a strand slips off and slaps against her chin, leaving a smear of sauce. 12–15 s, she laughs again and wipes her chin with her thumb; diners at the next table turn to look and smile. Audio: clinking plates, a Neapolitan song on a radio, the dialogue and the note in sync. Photorealistic, 24fps, 15 seconds.
>
> *If the model only supports 10 seconds: drop the 9–12 s beat (the sung note and the chin slap).*

**Negative prompt:** talking with a full mouth, frozen droplets, sauce flying upward, stains vanishing, duplicated faces, extra limbs, warping room.

**What it tests:** everything at once: camera motion, fast fork action, sauce particles that leave permanent marks, an extreme expression (laughing with the head back), real lip-sync in Italian for two speakers, a sung vowel, eating between lines, a crowd, and identity held for 15 seconds.

**Failures to watch for:**
- **Lip-sync:** mouth shapes do not match the Italian syllables (watch the "m" in "meglio" and "settimana", which should close the lips); Gennaro's line comes out of Ottavia's mouth; she "talks" with a full mouth.
- **The sung note:** an open "Ah!" that looks like a yawn, the jaw opens too far, or the face does not tense the way a singer's would.
- **Laugh deformation:** with her head thrown back the jaw unhinges, the teeth fuse, or a different woman comes back down.
- **Sauce splashes:** droplets fly upward, freeze mid-air, or loop; stains appear before the splash or fade a second later; the whole blouse turns pink instead of getting spotted.
- **Chin slap:** the strand passes through the chin; the smear does not appear or does not go away after the thumb; the thumb has two nails or no nail.
- **Handheld instability:** camera shake warps the table, the plate slides, the Chianti bottle duplicates, the four-table room grows to twenty.
- **Identity over time:** by second 12 the chignon has come down, the rings have moved to the left hand, the mole has moved, or she looks 20 years younger.
- **Background diners:** melted or mirrored faces; every diner has the same face; diners copy Ottavia's features.

---

## Scoring sheet

Score each criterion **0 = broken, 1 = noticeable glitch, 2 = clean**. A level **passes** at ≥ 80% of its maximum with no 0 on the bold criterion.

| Level | Criteria (bold = must not be 0) | Max |
|---|---|:-:|
| 1 | **Hand anatomy**, fork shape, strand definition, identity anchors, steam | 10 |
| 2 | **Strands attached to fork**, wrist motion, plate pile shrinks, utensil stable, idle hand | 10 |
| 3 | **No clipping at the mouth**, closed-mouth chewing, slurp shortens strand, sauce appears/disappears correctly, identity in close-up | 10 |
| 4 | **No identity blend**, hand count and ownership, wine pour, swinging strand, plate continuity, background parallax | 12 |
| 5 | **Lip-sync (both speakers)**, laugh without deformation, sauce stains stay, chin slap, room stable under handheld, identity at 15 s, background diners | 14 |

**Reading the result:** the highest level a model passes is its "spaghetti level". Level 3 is the original meme; Levels 1–2 are the warm-up that a decent model should pass. Level 5 needs a model with native audio and lip-sync; otherwise run it without audio and skip the lip-sync criterion (max 12).
