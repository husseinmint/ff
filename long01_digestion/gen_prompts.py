ENG = """Vintage 19th-century steel-plate anatomical / scientific engraving in the manner of Gray's Anatomy (1858) plates, reproduced as a two-colour risograph print: deep navy blue (#1E2A78) for all outlines, hatching and cross-hatching, and bright vermilion (#F2361D) ONLY on the parts named in RED PARTS, as flat fills with fine hatching, perfectly in register (no offset, no colour outside the outline).
The object is ONE single isolated element, closed by a bold continuous unbroken navy outline about 3 times thicker than the inner lines (no gaps anywhere in this outer outline); inside that outline, unshaded areas are solid warm cream paper (#F1EADC), never pure white. Any small gap enclosed by the object (inside a ring or handle, between an arm and the body, between branches) is also filled with the same cream, so the ONLY pure white in the image is the open background around the object. Every part is attached to the main object: nothing floats loose beside it. Clean, calm, educational, not gory: no blood, no wounds, no gore, no realistic flesh tones (the cut surfaces of organs are cream with navy hatching, never pink).
BACKGROUND: everything outside the object is flat pure white (#FFFFFF), perfectly uniform, no paper texture, no vignette, no shadow, no ground, no reflection."""
FR = {"1:1":"FRAMING: square 1:1, the object centred and floating in empty space, occupying about {w}% of the image width, with at least 20% empty white margin on every side; nothing touches or approaches the edges.",
      "9:16":"FRAMING: vertical 9:16, the object centred and floating in empty space, occupying about {w}% of the image height, with at least 12% empty white margin on every side; nothing touches or approaches the edges.",
      "16:9":"FRAMING: horizontal 16:9, the object centred and floating in empty space, occupying about {w}% of the image width, with at least 12% empty white margin on every side; nothing touches or approaches the edges."}
EDITFR = "FRAMING: same aspect ratio, same camera distance, same object size and same margins as the attached image; do not crop, do not zoom, do not move, do not redraw or restyle – edit in place, keeping the same line weight, hatching density and colours; every part not named in the change stays pixel-for-pixel identical."
SOLID = "Shapes are solid and compact; no thin wisps, loose threads, sprays of dots or detached fragments."
FORB = "FORBIDDEN: no text, letters, numbers, labels, leader lines, arrows, figure numbers, captions, plate titles, Latin names, borders, frames, logos, watermark; unlabelled, purely pictorial; no cartoon, no mascot, no 3D render, no photo look, no gradients, no glow."
FORB = FORB.replace("unlabelled, purely pictorial;", "unlabelled, purely pictorial; no writing or fake lettering on any object (books, papers, films, signs, clothing);")
FORB_PEOPLE = FORB + " People are drawn as serious, realistic adult figures in the fine-line style of 19th-century wood-engraved book illustrations, with natural proportions, realistic faces and calm expressions – no caricature, no big heads, no big eyes, no exaggerated features, no comic look. Every person has exactly two arms and two hands, each hand with exactly five correctly formed fingers; no extra or merged limbs. A figure cropped at the waist or chest ends in a clean, closed horizontal outline (no fading, no ragged edge)."
PHOTO = """Photorealistic studio photograph, 85 mm lens, soft even shadowless lighting from the front and both sides, true natural colours, razor-sharp focus on the whole subject, strong clear contrast, no motion blur, no depth-of-field blur.
BACKGROUND: one seamless flat warm cream colour (#F1EADC) edge to edge, perfectly uniform, no gradient, no floor line, no cast shadow, no vignette.
FORBIDDEN: no text, no letters, no numbers, no logos, no brand marks, no watermark, no labels, no illustration look, no cartoon, no 3D render look."""

A = []  # (id, title, aspect, width%, edit_of, people, subject, red)
def e(*a): A.append(a)

# ---------- GLOBAL ----------
e("G1","Digestive tract map (navigator)","9:16",80,None,False,
 "a frontal (facing the viewer) anatomical view of an adult human head, neck and torso down to the hips, the body drawn only as a clean smooth outline silhouette with cream inside: a plain oval head with NO facial features except a simple open mouth cavity outline, the neck, rounded shoulders that end in smooth closed curves (no arms at all), ribcage hinted with a few light lines, waist and hips; no nipples, no navel, no genitals – the silhouette closes in a smooth curve across the hips. Inside it, the complete digestive tract drawn clearly in front, in correct anatomical position (the person's left side is on the VIEWER'S RIGHT): the mouth cavity and throat in the head and neck, the oesophagus running straight down just left of the midline behind the breastbone, the J-shaped stomach on the VIEWER'S RIGHT under the ribs with its outlet (pylorus) curving back toward the centre, the large liver on the VIEWER'S LEFT under the ribs with the small gallbladder tucked beneath it, the pancreas lying horizontally just below and behind the stomach, the small intestine as a dense neat coil filling the centre of the belly, and the large intestine framing it like an upside-down U: caecum low on the VIEWER'S LEFT, ascending colon up the viewer's left, transverse colon across the top under the stomach and liver, descending colon down the VIEWER'S RIGHT, an S-shaped sigmoid loop at the lower right, and the short straight rectum ending at the bottom centre. Each organ has a crisp outline and light hatching so every station is clearly distinguishable; organs touch each other naturally with no gaps of pure white.",
 "none. This image is navy only.")
e("G2","Old open anatomy textbook","16:9",70,None,False,
 "one heavy antique leather-bound anatomy book lying open, seen from slightly above at about 30 degrees. The left page shows one small engraved drawing of a coiled intestine; the right page shows one small engraved top-down plan of a tennis court; all the rest of both pages is blank cream paper – no printed text, no lines of writing, no captions, no page numbers. Thick page block, rounded blank spine, one short wide ribbon bookmark lying on the right page and hanging over the bottom edge of the book, attached at the spine.",
 "ONLY the ribbon bookmark.")
e("G3","Brass microscope","1:1",45,None,False,
 "one 19th-century brass compound microscope seen from the side: horseshoe foot, curved arm, tall single tube with eyepiece at the top, objective lens above a round stage with two clips, small mirror below the stage.",
 "none. This image is navy only.")
e("G4","Pocket watch without hands","1:1",50,None,False,
 "one antique open-face pocket watch seen perfectly face-on: round case with crown and a thick bow ring at the top (the hole inside the ring is cream, not white), clean dial with twelve plain tick marks (no numerals), and NO hands at all (the centre of the dial is empty except a small centre pin).",
 "ONLY the small centre pin.")

# ---------- CH1 MOUTH ----------
e("M1","Head cross-section (base – generate first)","1:1",60,None,False,
 "a midline sagittal (side) anatomical cross-section of an adult human head and neck, the FACE POINTING TO THE VIEWER'S LEFT and the back of the head and spine on the VIEWER'S RIGHT, cut exactly down the middle: forehead, nose, closed relaxed lips, the upper and lower front teeth, the hard palate and the soft palate with its small uvula, the large muscular tongue resting flat on the floor of the mouth, the throat (pharynx) behind the tongue, the small leaf-shaped epiglottis standing upright behind the root of the tongue, then the windpipe running down the FRONT of the neck (viewer's left) and the oesophagus running down directly BEHIND it (viewer's right), in front of the stacked neck vertebrae. The skull and brain area are simplified to calm light hatching. The neck ends at its base in one clean straight horizontal cut, closed by the bold outline. Clean Gray's-Anatomy-style textbook diagram, no blood, no pink.",
 "none. This image is navy only.")
e("M2","Head – salivary glands lit (EDIT of M1)","1:1",None,"M1",False,
 "Keep exactly the same head section: same outline, size, position and hatching. Change ONLY this: overlay the three salivary glands as if seen through the cheek, each a small compact lobed cluster with one short duct that connects it to the mouth cavity: the largest (parotid) just in front of where the ear would be, at the angle of the jaw, its duct running forward across the cheek to the upper back teeth; a smaller one under the back of the lower jaw (submandibular), its duct running forward under the tongue; and the smallest, almond-shaped one under the front of the tongue (sublingual). All three stay inside the head outline. Everything else stays identical.",
 "ONLY the three salivary glands and their ducts.")
e("M3","Head – tongue pushes bite back (EDIT of M1)","1:1",None,"M1",False,
 "Keep exactly the same head section: same outline, size, position and hatching. Change ONLY this: the front and middle of the tongue are now raised and pressed up against the hard palate, and one small round soft ball of chewed food (about the size of a grape) sits on the back of the tongue, touching it, just in front of the throat. The lips, teeth, palate, throat, neck and outline do not move. Everything else stays identical.",
 "ONLY the ball of chewed food.")
e("M4","Bread piece","1:1",40,None,False,
 "one torn piece of rustic white bread, about the size of a palm, with a crisp crust on two sides and an open airy crumb with irregular holes on the torn face; one compact solid piece with no loose crumbs around it.",
 "none. This image is navy only.")
e("M5","Food ball (bolus sprite)","1:1",30,None,False,
 "one small soft round ball of chewed food, slightly irregular, like a ball of moist dough, with a few small bumps pressed into its surface; the outline is smooth and closed, nothing sticks out, any shine is a small cream highlight (not white).",
 "the whole ball (flat vermilion fill with navy hatching for shading).")

# ---------- CH2 THROAT ----------
e("T1","Throat – airway open (base – generate first)","1:1",55,None,False,
 "a close-up midline sagittal anatomical cross-section of the human throat, seen from the side with the FRONT OF THE NECK ON THE VIEWER'S LEFT and the spine on the VIEWER'S RIGHT (the same orientation as a head facing left), from the soft palate and back of the tongue down to the base of the neck: the back of the tongue on the upper left, the open pharynx behind it, the leaf-shaped epiglottis standing UPRIGHT and open, the larynx (voice box) below it with the windpipe running down at the FRONT (viewer's left), and the oesophagus running down directly BEHIND it (viewer's right), in front of a column of neck vertebrae on the far right. The two tubes are clearly separate and parallel. The section ends in one clean straight cut at the top and one at the bottom, closed by the bold outline. No blood, no pink, clean textbook look.",
 "none. This image is navy only.")
e("T2","Throat – swallowing (EDIT of T1)","1:1",None,"T1",False,
 "Keep exactly the same throat section: same outline, size, position and hatching. Change ONLY this: the epiglottis is now tipped DOWN and backward like a lid, covering the entrance of the windpipe, and one small round ball of chewed food sits on top of the folded epiglottis, sliding over it into the opening of the oesophagus behind (viewer's right). The larynx may sit a little higher, but the outer outline, the vertebrae, the tongue and both tubes keep their size and position. Everything else stays identical.",
 "ONLY the ball of chewed food.")
e("T3","Lungs (small prop)","1:1",45,None,False,
 "a pair of human lungs seen from the front with the windpipe and its two main branches on top, lobes clearly outlined, light hatching for volume.",
 "none. This image is navy only.")

# ---------- CH3 OESOPHAGUS ----------
e("E1","Tall oesophagus (base – generate first)","9:16",85,None,False,
 "a straight vertical anatomical drawing of the human oesophagus as a long muscular tube, seen from the front, from a clean rounded cut at the top (just below the throat) down to where it joins the top of the stomach at the bottom; only the upper rounded part of the stomach is shown, bulging out to the VIEWER'S RIGHT and closed below by a clean curved cut. The tube has an even width along its whole length; its wall shows rings of circular muscle drawn as evenly spaced fine bands, and a slightly thicker ring (the lower sphincter) just above the stomach, drawn closed.",
 "none. This image is navy only.")
e("E2","Vintage astronaut eating in orbit","1:1",55,None,True,
 "one adult astronaut in a generic plain 1960s-style pressure suit with no badges, no flags, no patches and no lettering, helmet off and held firmly under his left arm, drifting weightless with his whole body tilted at about 30 degrees and his legs loosely bent, using his right hand to squeeze a small plain unlabelled food tube into his mouth. Three-quarter side view, full body, calm realistic face. No floating objects, no spacecraft, no stars.",
 "ONLY the food tube.")
e("E3","Person eating while lying down","16:9",70,None,True,
 "one adult man in plain trousers and a plain shirt lying relaxed flat on his back on a simple old-fashioned wooden couch, head on a cushion at the viewer's left, legs stretched out to the right, holding a slice of bread with one hand just above his mouth and taking a bite; the other arm rests on his chest. Side view, full body; the man, cushion and couch form one connected shape, no floor.",
 "ONLY the slice of bread.")

e("E4","Oesophagus – squeeze wave (EDIT of E1)","9:16",None,"E1",False,
 "Keep exactly the same oesophagus and stomach top: same outline, size, position and hatching. Change ONLY this: one round ball of chewed food now sits inside the tube about two-thirds of the way down, making the tube bulge gently around it; directly ABOVE the ball, a short band of the tube is squeezed narrow by tightened muscle rings (the squeeze wave pushing it down); BELOW the ball the tube is relaxed and slightly wider. Everything else stays identical.",
 "ONLY the ball of chewed food.")
e("E5","Toothpaste tube (plain)","1:1",45,None,False,
 "one plain old-fashioned metal toothpaste tube lying diagonally, completely blank with no label and no printing: a round screw cap at the lower-left end, the back end flattened and rolled up two turns, the middle visibly squeezed in, and a short thick ribbon of paste coming out of the open nozzle, still attached to it (cap off and lying touching the tube).",
 "ONLY the ribbon of paste.")

# ---------- CH4 STOMACH ----------
e("S1","Stomach cross-section (base – generate first)","1:1",60,None,False,
 "an anatomical cross-section of the human stomach seen from the front with its front wall cut away, in correct body orientation as in a textbook (the person's left is on the VIEWER'S RIGHT): a short stub of oesophagus enters at the top, slightly left of centre; the rounded dome (fundus) bulges up to the VIEWER'S RIGHT of that entry; the long outer curve sweeps down the right side and along the bottom; the bag narrows toward the LOWER LEFT into the thick ring-shaped pyloric valve, which opens into a short stub of the small intestine leaving to the VIEWER'S LEFT. The thick muscular wall is shown in three layers, and the inner lining is thrown into long wavy parallel folds (rugae). The two tube stubs end in clean cuts closed by the bold outline. Empty inside (cream).",
 "none. This image is navy only.")
e("S2","Stomach – full and churning (EDIT of S1)","1:1",None,"S1",False,
 "Keep exactly the same stomach section: same outline, size, position and hatching. Change ONLY this: the lower two-thirds of the stomach cavity is now filled with a thick churning mass of food mixed with liquid, its upper surface rippled in waves; the mass stays fully inside the stomach wall and touches the inner lining. Everything else stays identical.",
 "ONLY the food mass.")
e("S3","Stomach wall micro-section (base – generate first)","16:9",80,None,False,
 "a magnified microscope-style cross-section of a small wide rectangular block of stomach lining, its sides and bottom cut straight: in the lower part, a row of tall column-shaped cells with nuclei, the surface dipping down into a few narrow pits (gastric pits) lined by the same cells; directly on top of the cells, a thick smooth protective layer of mucus drawn as a gently wavy band with soft stippling, which forms the TOP edge of the block (nothing is drawn above it). Clear, simple, educational.",
 "none. This image is navy only.")
e("S4","Wall micro-section – new cells (EDIT of S3)","16:9",None,"S3",False,
 "Keep exactly the same micro-section: same outline, size, position and hatching. Change ONLY this: the top row of surface cells directly under the mucus is highlighted as freshly renewed cells. Everything else stays identical.",
 "ONLY the top row of surface cells.")
e("S5","Pyloric valve – closed (base – generate first)","1:1",45,None,False,
 "a close-up anatomical cross-section of the pyloric valve: the narrow lower end of the stomach on the VIEWER'S RIGHT (with a few rugae folds) joining the start of the small intestine on the VIEWER'S LEFT (matching the stomach drawing, where the pylorus is at the lower left), with a thick ring of muscle in between squeezed tightly CLOSED. Both ends are clean cuts closed by the bold outline.",
 "none. This image is navy only.")
e("S6","Pyloric valve – open (EDIT of S5)","1:1",None,"S5",False,
 "Keep exactly the same valve section: same outline, size, position and hatching. Change ONLY this: the muscle ring has relaxed and opened slightly, and a small continuous stream of smooth liquefied food passes through it from the stomach (right) into the intestine (left), staying inside the tubes. Everything else stays identical.",
 "ONLY the liquefied food stream.")
e("S7","Raw steak","1:1",45,None,False,
 "one thick raw beef steak seen from slightly above, with clear muscle grain and a thin rim of fat along one edge.",
 "the meat surface only (not the fat rim).")
e("S8","Frontier fort, 1820s","16:9",80,None,False,
 "a small early-19th-century frontier military fort on a rounded limestone bluff above a lake: pale stone walls, one square blockhouse, a few low buildings, a short sturdy flagpole with a plain flag, a few pine trees growing against the walls, and a narrow band of calm hatched water along the foot of the bluff. The whole scene is ONE compact island-like mass: bluff, fort, trees and water band are joined and closed together by one bold continuous outline with crisp edges (NOT a vignette, nothing fades out); no sky is drawn, no clouds, no birds, no boats.",
 "ONLY the plain flag.")
e("S9","Army surgeon and patient, 1820s","16:9",75,None,True,
 "a quiet historical scene: on the viewer's left, a 19th-century army surgeon in a dark buttoned uniform coat sits on a stool, facing right; on the viewer's right, a young man in a plain loose light-coloured shirt (cream with navy hatching, fully outlined) sits on a wooden chair facing him. The young man's shirt is lifted on his left side (the side toward the surgeon), showing a small neat bandage pad below the ribs (no wound shown). The surgeon calmly holds up a short thread between his thumb and finger, with a small piece of food tied to its lower end. A small wooden table behind them, touching both chairs, holds one glass vial and one closed plain notebook. All figures and furniture overlap into one connected group with no floor. Respectful, calm, documentary mood; no blood.",
 "ONLY the tiny piece of food on the thread.")
e("S10","Antique book, 1833","1:1",40,None,False,
 "one small antique cloth-bound book standing slightly open, seen at three-quarter view, worn corners, plain cover with only a thin decorative border line, blank spine, blank visible pages – no lettering, no title, no date anywhere.",
 "ONLY the thin decorative border line on the cover.")

# ---------- CH5 SMALL INTESTINE + PIT CREW ----------
e("I1","Small intestine coil (base – generate first)","1:1",60,None,False,
 "the human small intestine shown alone as a dense, neat, rounded coil of tube folded back and forth on itself, seen from the front in body orientation, with a short cut stub where the tube starts at the UPPER RIGHT (viewer's right) and a short cut stub where it ends at the LOWER LEFT (viewer's left); each loop clearly outlined, touching its neighbours, and shaded with hatching, so the whole coil reads as one compact rounded mass with no holes of white between loops.",
 "none. This image is navy only.")
e("I2","Intestine fold section","16:9",75,None,False,
 "a magnified cross-section of a short piece of small-intestine wall cut lengthwise: the outer muscle layers forming a straight band along the bottom, and on top the inner lining raised into four or five large rounded folds, each fold covered with a dense, even carpet of short finger-like projections (villi) standing side by side and touching, so the top edge reads as one continuous fringed outline.",
 "none. This image is navy only.")
e("I3","Single villus (base – generate first)","9:16",75,None,False,
 "one single intestinal villus greatly magnified: a tall upright finger-shaped projection with a rounded tip, rising from a short flat strip of lining at its base (the base is a clean straight cut closed by the outline); its surface is covered with a single neat layer of column cells; inside the finger, a fine net of tiny blood capillaries and one central lymph vessel (lacteal) running up the middle, both entering from the base.",
 "none. This image is navy only.")
e("I4","Villus – absorbing (EDIT of I3)","9:16",None,"I3",False,
 "Keep exactly the same villus: same outline, size, position and hatching. Change ONLY this: the capillary net and the central lymph vessel are now highlighted to show nutrients being carried away. Everything else stays identical.",
 "ONLY the capillary net and the central lymph vessel.")
e("I5","Microvilli brush border","16:9",80,None,False,
 "an extreme magnification of the top edge of three neighbouring intestinal cells: three tall cells side by side with nuclei visible, their bottom closed by a straight cut; their upper surfaces are covered with a dense, even row of short, thick, upright finger-like projections (microvilli) of equal height, packed side by side like the bristles of a brush.",
 "none. This image is navy only.")
e("I6","Tennis court, top-down","16:9",80,None,False,
 "a full tennis court seen exactly from directly above (flat orthographic plan, no perspective), long side horizontal, as a clean plan drawing: the outer doubles boundary forms the bold closed outline, with singles lines, service boxes, centre mark and the net across the middle drawn as a thin hatched band that stays within the boundary; the court surface lightly hatched. No players, no balls, no surroundings.",
 "none. This image is navy only.")
e("I7","Badminton court, top-down","16:9",60,None,False,
 "a full badminton court seen exactly from directly above (flat orthographic plan, no perspective), long side horizontal, as a clean plan drawing: the outer boundary forms the bold closed outline, with all standard lines and the net across the middle drawn as a thin hatched band within the boundary; the surface lightly hatched. No players, no shuttlecock, no surroundings.",
 "none. This image is navy only.")
e("I8","Studio apartment floor plan","1:1",55,None,False,
 "a small rectangular studio apartment seen exactly from directly above as an architect's plan drawing: thick solid outer walls forming one continuous closed rectangle (no openings that break the outer outline); the entrance door shown only as a door leaf with a quarter-circle swing arc drawn inside the room, one window shown as a thin double line within the wall thickness; inside: a bed, a small sofa, a tiny kitchen counter with a sink, and a small bathroom corner with a shower tray; furniture drawn in light hatching. Absolutely no room names, no dimensions, no measurement lines, no scale bar, no north arrow, no title block.",
 "none. This image is navy only.")
e("I9","Two researchers at a microscope","16:9",70,None,True,
 "two modern adult scientists in lab coats (the coats drawn cream with navy hatching and fully outlined, never pure white), one man and one woman, standing side by side and overlapping slightly behind a lab bench: the woman on the left looks into a modern laboratory microscope standing on the bench; the man on the right holds up one plain rectangular X-ray film with both hands, the film showing only a soft abstract shadow of looped intestine, with no markings, letters, numbers or labels. Three-quarter view, from the waist up, the bench edge closing the bottom of the group; calm focused expressions.",
 "ONLY the X-ray film.")
e("L1","Liver, gallbladder and pancreas (base – generate first)","16:9",75,None,False,
 "an anatomical drawing of the liver, gallbladder and pancreas together with the C-shaped first part of the small intestine (duodenum), seen from the front in body orientation (the person's right on the VIEWER'S LEFT), with the stomach removed: the large liver across the top, its big right lobe on the VIEWER'S LEFT and its smaller left lobe tapering to the viewer's right; the small pear-shaped gallbladder tucked under the right lobe (viewer's left); the bile duct running down from it; below, the C-shaped duodenum on the viewer's left, opening toward the viewer's right; the long tapering pancreas lying horizontally with its broad head nestled inside the C of the duodenum and its body and tail stretching to the VIEWER'S RIGHT; the pancreatic duct running along inside the pancreas and joining the bile duct where both enter the inner wall of the duodenum. All organs touch or overlap into one connected group.",
 "none. This image is navy only.")
e("L2","Liver group – ducts lit (EDIT of L1)","16:9",None,"L1",False,
 "Keep exactly the same organs: same outline, size, position and hatching. Change ONLY this: the bile duct, the gallbladder and the pancreatic duct are highlighted, showing their path into the duodenum. Everything else stays identical.",
 "ONLY the gallbladder, the bile duct and the pancreatic duct.")
e("L3","Bar of soap","1:1",40,None,False,
 "one simple plain rectangular bar of soap with rounded edges and no engraved brand or lettering, seen at three-quarter view, with one compact mound of round foam bubbles sitting on its top, all bubbles touching each other and the bar (no loose bubbles).",
 "none. This image is navy only.")

# ---------- CH6 COLON + BACTERIA ----------
e("C1","Colon cross-section (base – generate first)","1:1",60,None,False,
 "an anatomical cut-away view of one short, horizontal, gently curved segment of the large intestine (transverse colon) seen from the front, with the front half of the wall cut away lengthwise to show the interior: the wide tube with its characteristic row of bulging pouches (haustra) along the outside, a flat longitudinal muscle band (taenia) running along its length, the inner lining smooth without finger-like villi but crossed by crescent-shaped folds between the pouches, and one compact soft mass of content resting in the lower half. Both ends of the segment are clean oval cuts closed by the bold outline.",
 "none. This image is navy only.")
e("C2","Colon – bacterial city (EDIT of C1)","1:1",None,"C1",False,
 "Keep exactly the same colon: same outline, size, position and hatching. Change ONLY this: the content and the inner surface of the wall are now densely populated by countless tiny rod-shaped and round bacteria packed into thick continuous colonies (a dense textured carpet, not scattered dots), all strictly inside the colon's outline. Everything else stays identical.",
 "ONLY the bacteria colonies.")
e("B1","Rod bacterium","1:1",35,None,False,
 "one single rod-shaped bacterium greatly magnified: a smooth capsule-shaped cell with rounded ends, lying diagonally, with a few very short stubby pili attached along its sides (no long hairs).",
 "the whole bacterium body (flat vermilion fill with navy hatching).")
e("B2","Chain of round bacteria","1:1",45,None,False,
 "one short curved chain of six round bacteria (cocci) greatly magnified, each sphere slightly overlapping the next so the whole chain is one connected shape (no string, no gaps).",
 "the whole chain (flat vermilion fill with navy hatching).")
e("B3","Spiral bacterium","1:1",40,None,False,
 "one single spiral-shaped (corkscrew) bacterium greatly magnified, a thick solid corkscrew body with three smooth turns lying horizontally, and one short, fairly thick, gently curved whip-like tail attached at one end.",
 "the whole bacterium body (flat vermilion fill with navy hatching).")
e("B4","Human cell","1:1",40,None,False,
 "one single round human cell greatly magnified, cut open in half to show a large round nucleus in the centre and a few small organelles scattered around it.",
 "none. This image is navy only.")
e("C3","Balance scale – tipped (base – generate first)","1:1",55,None,False,
 "one antique brass balance scale with a central pillar, a horizontal beam and two hanging pans; the beam is strongly tipped: the RIGHT pan is low and heavily loaded with a large compact heap of tiny round beads, the LEFT pan is high and holds a small compact heap of larger round beads; all beads sit packed inside the pans, none falling or lying loose. Each pan hangs from short solid rods (not thin chains).",
 "ONLY the heap of tiny beads in the right pan.")
e("C4","Balance scale – nearly level (EDIT of C3)","1:1",None,"C3",False,
 "Keep exactly the same scale: same outline, size, position and hatching. Change ONLY this: the beam is now almost level, tipped only very slightly toward the right, and the two pans hang at nearly the same height; the right pan holds a moderate compact heap of tiny beads and the left pan a similar-sized compact heap of larger beads. The base, the pillar and the pivot keep exactly the same size and position. Everything else stays identical.",
 "ONLY the heap of tiny beads in the right pan.")
e("C5","Tiny city skyline","16:9",70,None,False,
 "a small, dense city skyline sitting on a gently curved mound-shaped base whose bottom is closed by the bold outline: rows of narrow towers, domes and rounded rooftops of different heights packed tightly together and touching, with tiny windows; no antennas, no spires, no flags; its silhouette is soft and rounded like a colony.",
 "ONLY the domes.")

# ---------- CH7 CONTROL ROOM ----------
e("N1","Intestine wrapped in nerve net (EDIT of I1)","1:1",None,"I1",False,
 "Keep exactly the same intestine coil: same outline, size, position and hatching. Change ONLY this: a fine branching net of nerve fibres with small knot-like nerve clusters now wraps over the whole surface of the coil like a lace web, following the loops and staying strictly inside the coil's outer outline (nothing sticks out past it). Everything else stays identical.",
 "ONLY the nerve net and its knots.")
e("N2","Single neuron","1:1",55,None,False,
 "one single nerve cell greatly magnified: a star-shaped cell body with a round nucleus, five or six short, fairly thick branching dendrites spreading out on the left, and one long smooth axon leaving to the right and ending in a few small knob-tipped branching terminals; every branch stays attached to the cell and no branch reaches the margins.",
 "ONLY the cell body.")
e("N3","Brain + top of spinal cord, side view","9:16",70,None,False,
 "one human brain seen from its left side, the front pointing to the VIEWER'S LEFT, with clear folds (gyri) and grooves, the cerebellum at the back bottom (viewer's right), and the brainstem continuing straight down into a length of spinal cord about as long as the brain is tall, ending in a clean rounded cut; a few short stubs of spinal nerves attached along the cord. No skull, no vertebrae.",
 "none. This image is navy only.")
e("N4","Hungry man","1:1",55,None,True,
 "one adult man shown from the waist up in a plain shirt, three-quarter front view, one open hand resting flat on his belly and the other hand raised slightly beside his chest, palm out, glancing down at his stomach with a mildly embarrassed, natural expression (subtle, not comic). No room, no furniture – the figure alone, closed at the waist by a clean horizontal outline.",
 "none. This image is navy only.")
e("N5","Street sweeper (base – generate first)","1:1",55,None,True,
 "one adult street sweeper in plain work overalls and a cap, full body, side view facing right, standing with feet apart, holding a long wooden push-broom with both hands, the broom head touching the level of his feet just behind his heels. No ground line, no shadow, no street.",
 "ONLY the broom head.")
e("N6","Street sweeper – mid-sweep (EDIT of N5)","1:1",None,"N5",True,
 "Keep exactly the same man, same face, same clothes, same size and same position; his feet, legs and body stay where they are. Change ONLY this: his arms have moved so the broom is now pushed forward, with the broom head just in front of his feet (to the right), and one small compact solid heap of dust pressed against the front of the bristles, touching them. Everything else stays identical.",
 "ONLY the broom head.")

# ---------- OUTRO ----------
e("O1","Man taking a bite (base – generate first)","1:1",55,None,True,
 "one adult man, head and shoulders, clean side profile facing the VIEWER'S LEFT (matching the head cross-section), one hand raised holding a piece of rustic bread at his slightly open mouth just about to bite it, calm natural expression; the shoulders are closed at the bottom by a clean horizontal outline.",
 "ONLY the piece of bread.")
e("O2","Man chewing (EDIT of O1)","1:1",None,"O1",True,
 "Keep exactly the same man, same size and same position. Change ONLY this: his lips are now closed and his cheek slightly full as he chews, and the piece of bread, still in the same hand at the same place, now has one clean bite missing from the end nearest his mouth. Head, hand and shoulders do not move. Everything else stays identical.",
 "ONLY the piece of bread.")

PH = []
def p(*a): PH.append(a)
p("P1","COLOUR HOOK: hand lifting bread","16:9",
 "FRAMING: horizontal 16:9. ONE subject centred, occupying about 45% of the image width, with generous empty margins on the top, left and right; only the forearm meets the bottom edge.",
 "a man's right hand with five natural, correctly formed fingers (only the hand and wrist with a plain shirt cuff, the forearm entering from the bottom edge of the frame) holding up one torn piece of fresh rustic white bread with a golden crust and soft airy crumb, as if about to take a bite.",
 "no face, no plate, no table, no crumbs falling, no other food, no jewellery.")
p("P2","COLOUR: bread slice","1:1",
 "FRAMING: square 1:1. ONE subject centred, occupying about 45% of the image width, with at least 25% empty margin on every side.",
 "one torn piece of fresh rustic white bread with a golden crust and soft open crumb, lying slightly tilted.",
 "no plate, no knife, no butter, no hands, no other food.")
p("P3","COLOUR: raw steak","1:1",
 "FRAMING: square 1:1. ONE subject centred, occupying about 45% of the image width, with at least 25% empty margin on every side.",
 "one thick raw beef steak, deep red with a thin rim of white fat, seen from slightly above.",
 "no plate, no board, no blood pool, no knife, no herbs, no hands.")
p("P4","COLOUR: soap foam on oil","1:1",
 "FRAMING: square 1:1. ONE subject centred, occupying about 50% of the image width, with at least 20% empty margin on every side.",
 "one shallow clear glass dish of water seen from slightly above, with a golden pool of cooking oil on the water breaking apart into many small round droplets where a dollop of white soap foam touches it.",
 "no hands, no sponge, no bottle, no sink, no other dishes.")
p("P5","COLOUR: fibre-rich food","1:1",
 "FRAMING: square 1:1. ONE subject centred, occupying about 50% of the image width, with at least 20% empty margin on every side.",
 "one small rustic ceramic bowl filled with a mix of cooked lentils, chickpeas and a few green beans, seen from slightly above.",
 "no spoon, no hands, no table, no napkin, no other bowls.")
p("P6","COLOUR: empty plate with crumbs","1:1",
 "FRAMING: square 1:1. ONE subject centred, occupying about 55% of the image width, with at least 20% empty margin on every side.",
 "one plain white round plate seen from directly above, empty except for a few scattered bread crumbs.",
 "no cutlery, no napkin, no hands, no table texture.")

out = ["# LONG-01 «رحلة لقمة داخل جسمك» — IMAGE PROMPTS (16:9 long-form, style v3)",
"",
"ORDER: generate every '(base – generate first)' image before its EDITs. For each EDIT, attach the image named in the title.",
"Generate engravings at the largest size available (≥2048 px). Check every result: anatomy correct, no text, white background, nothing touching the edges.",
"Total: %d engravings + %d colour photos = %d images." % (len(A), len(PH), len(A)+len(PH)), ""]
for (i,t,asp,w,ed,ppl,subj,red) in A:
    out.append("---------------------------------------------------------------")
    out.append("### %s – %s  (%s)" % (i,t,asp if not ed else "same as "+ed))
    out.append("---------------------------------------------------------------")
    blk=[]
    if ed: blk.append("Edit the attached image (%s)." % ed)
    blk.append(ENG)
    blk.append(EDITFR if ed else FR[asp].format(w=w))
    blk.append(SOLID)
    blk.append(FORB_PEOPLE if ppl else FORB)
    blk.append(("SUBJECT / CHANGE: " if ed else "SUBJECT: ")+subj)
    blk.append("RED PARTS: "+red)
    out.append("\n".join(blk)); out.append("")
for (i,t,asp,fr,subj,no) in PH:
    out.append("---------------------------------------------------------------")
    out.append("### %s – %s  (%s)" % (i,t,asp))
    out.append("---------------------------------------------------------------")
    out.append(PHOTO); out.append(fr); out.append("SUBJECT: "+subj); out.append("ALSO FORBIDDEN: "+no); out.append("")
open("LONG01_IMAGE_PROMPTS.md","w").write("\n".join(out))
print(len(A),len(PH))
