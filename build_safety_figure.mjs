import { writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import * as k from "/Users/bombermac/.agents/skills/anatomy/kit/iso-kit.mjs";
import { kitScript } from "/Users/bombermac/.agents/skills/anatomy/scripts/inline-kit.mjs";

const theme = process.argv.includes("--light") ? "light" : "dark";
const WIDTH = 760;
const HEIGHT = 480;

// Base Surface Plate
const PLATE = { x: -145, y: -80, w: 290, d: 160, r: 8 };
const PLATE_H = 14;
const FOOT_H = 6;

// FalkorDB Graph Matrix Platform
const MATRIX = { x: -130, y: -64, w: 104, d: 94, r: 4 };
const MATRIX_H = 5;

// Graph Nodes [x, y, r, h, name]
const NODES = {
  agent:   { x: -110, y: -42, r: 7.5, h: 8, label: "a:Agent" },
  intent:  { x: -110, y: 8,   r: 7,   h: 7, label: "i:Intent" },
  falkor:  { x: -78,  y: -18, r: 12,  h: 11, label: "FalkorDB Engine" },
  policy:  { x: -46,  y: -42, r: 7,   h: 8, label: "c:Policy" },
  gate:    { x: -46,  y: 8,   r: 7.5, h: 9, label: "s:SafetyGate" },
};

// Guide Rails & Gantry
const RAIL_X0 = -20;
const RAIL_X1 = 120;
const RAIL_Y1 = -22;
const RAIL_Y2 = 22;
const RAIL_Z = 0;
const RAIL_H = 4;

// Carriage parameters (centered at rest x = 0)
const CARRIAGE = { x: -18, y: -26, w: 36, d: 52, r: 2.5 };
const CARRIAGE_Z = 4;
const CARRIAGE_TOP = 11;

// Dial Indicator (Inspection gauge)
const POST = [48, 48];
const POST_H = 68;
const CLAMP_Z = 52;
const DIAL = [48, 16];
const DIAL_R = 16;
const DIAL_Z = 34;
const DIAL_H = 8;
const DIAL_TOP = DIAL_Z + DIAL_H;

// Target Anatomy Workpiece
const WORKPIECE = { x: 78, y: -58, w: 46, d: 42, r: 2 };
const WORKPIECE_Z = 0;
const WORKPIECE_H = 6;

// Evaluation Stops (Scanning positions along rails)
const STOPS = [-4, 38, 80];
const REACH = [-8, 86];

// Setup Camera Projection
const P = k.fitProjection(
  [
    ...k.boxCorners(PLATE, -PLATE_H - FOOT_H, 0),
    [POST[0] - 12, POST[1] + 12, POST_H + 4],
    [DIAL[0] + DIAL_R + 4, DIAL[1] + DIAL_R, DIAL_TOP + 8],
    [PLATE.x + PLATE.w, PLATE.y + PLATE.d, 0]
  ],
  WIDTH,
  HEIGHT,
  { pad: 30, azimuth: 44, elevation: 31 }
);

const at = (point) => k.iso(point, P);
const S = (paths, style) => k.solidSvg(paths, style);
const L = (d, style) => k.lineSvg(d, style);
const D = (points, style) => k.dotsSvg(points, style);
const byDepth = (points) => [...points].sort((a, b) => k.depthOf([a[0], a[1], 0], P) - k.depthOf([b[0], b[1], 0], P));

// 1. Heavy Cast Base Plate & Feet
function renderBasePlate() {
  const out = [];
  // Soft ambient halo under base
  out.push(`<path class="iso-halo" d="${k.haloOf(PLATE, -PLATE_H - FOOT_H, PLATE_H, P)}"/>`);

  // Four precision mounting feet with dampener collars
  for (const [x, y] of byDepth(k.corners(PLATE, 24))) {
    out.push(S(k.cylinder(x, y, 8, -PLATE_H - FOOT_H, 2.2, P, 28), { tone: "lo" }));
    out.push(S(k.cylinder(x, y, 6.2, -PLATE_H - FOOT_H + 2.2, FOOT_H - 2.2, P, 28), { tone: "mid" }));
  }

  // Heavy beveled granite/steel surface plate
  out.push(S(k.slabOf(PLATE, -PLATE_H, PLATE_H, P, 8, 1.6), { tone: "mid" }));

  // Perimeter oil groove
  out.push(L(k.planOutline(k.insetPlan(PLATE, 5.5), 0, P), { tone: "lo" }));

  // Corner socket-head clamping screws
  const screws = k.corners(PLATE, 11);
  out.push(L(screws.map(([x, y]) => k.ring(x, y, 2.4, 0, P, 16)).join(""), { tone: "lo" }));
  out.push(D(screws.map(([x, y]) => at([x, y, 0])), { size: 0.52 }));

  // Front engraved millimeter ruler strip
  const strip = { x: -125, y: PLATE.y + PLATE.d - 14, w: 250, d: 7.5, r: 1.2 };
  out.push(S(k.slabOf(strip, 0, 0.7, P, 3), { tone: "lo", crease: "none" }));
  const ticks = k.topTicks(strip.x + 5, strip.x + strip.w - 5, 4, 5, strip.y + 0.8, 0.7, [2, 3.8], P);
  out.push(L(ticks.minor, { tone: "lo" }), L(ticks.major, { tone: "mid" }));
  out.push(D([at([strip.x + 3, strip.y + 3.8, 0.7]), at([strip.x + strip.w - 3, strip.y + 3.8, 0.7])], { size: 0.45 }));

  // Brass Specification Plate on the left front
  const labelPlan = { x: -128, y: PLATE.y + 8, w: 44, d: 15, r: 1.5 };
  out.push(S(k.slabOf(labelPlan, 0, 0.8, P, 3), { tone: "lo", crease: "none" }));
  out.push(L(k.planOutline(k.insetPlan(labelPlan, 1.8), 0.8, P), { tone: "faint" }));
  out.push(L(k.lineOnTop([labelPlan.x + 4, labelPlan.y + 4.5], [labelPlan.x + 38, labelPlan.y + 4.5], 0.8, P), { tone: "lo", free: true }));
  out.push(L(k.lineOnTop([labelPlan.x + 4, labelPlan.y + 8.5], [labelPlan.x + 32, labelPlan.y + 8.5], 0.8, P), { tone: "lo", free: true }));
  out.push(L(k.lineOnTop([labelPlan.x + 4, labelPlan.y + 11.5], [labelPlan.x + 24, labelPlan.y + 11.5], 0.8, P), { tone: "lo", free: true }));
  out.push(D([at([labelPlan.x + 2, labelPlan.y + 7.5, 0.8]), at([labelPlan.x + labelPlan.w - 2, labelPlan.y + 7.5, 0.8])], { size: 0.45 }));

  return out.join("");
}

// 2. FalkorDB Graph Matrix Platform & Connected Nodes
function renderGraphMatrix() {
  const out = [];

  // Stepped insulated substrate
  out.push(S(k.slabOf(MATRIX, 0, MATRIX_H, P, 6, 0.8), { tone: "mid" }));
  out.push(S(k.slabOf(k.insetPlan(MATRIX, 2), MATRIX_H, 1.4, P, 6, 0.5), { tone: "hi", crease: "lo" }));
  out.push(L(k.planOutline(k.insetPlan(MATRIX, 4.5), MATRIX_H + 1.4, P), { tone: "faint" }));

  // Corner mounting screws of substrate
  const matScrews = k.corners(MATRIX, 6);
  out.push(D(matScrews.map(([x, y]) => at([x, y, MATRIX_H + 1.4])), { size: 0.45, tone: "lo" }));

  // Graph Edges (Conductive Bus-Bars) connecting nodes
  const edgeZ = MATRIX_H + 1.4;
  const edges = [
    [NODES.agent, NODES.intent],
    [NODES.agent, NODES.falkor],
    [NODES.intent, NODES.falkor],
    [NODES.falkor, NODES.policy],
    [NODES.falkor, NODES.gate],
    [NODES.policy, NODES.gate],
  ];

  for (const [from, to] of edges) {
    // Bus-bar copper strip
    out.push(L(k.lineOnTop([from.x, from.y], [to.x, to.y], edgeZ + 0.1, P), { tone: "mid" }));
    out.push(L(k.lineOnTop([from.x + 0.6, from.y + 0.6], [to.x + 0.6, to.y + 0.6], edgeZ + 0.1, P), { tone: "lo" }));
  }

  // Render individual Graph Nodes
  for (const key of Object.keys(NODES)) {
    const node = NODES[key];
    const isCore = key === "falkor";
    const zBase = edgeZ;

    // Node pedestal
    out.push(S(k.cylinder(node.x, node.y, node.r, zBase, node.h, P, isCore ? 40 : 28, 0.5), { tone: isCore ? "hi" : "mid", crease: "lo" }));

    // Cooling ribs / knurled bezel on FalkorDB core
    if (isCore) {
      out.push(L(k.knurl(node.x, node.y, node.r, zBase + 2, zBase + node.h - 1.5, 48, P, 0.3), { tone: "lo" }));
      out.push(L(k.sideArc(node.x, node.y, node.r, zBase + 2, P, 32), { tone: "faint" }));
      out.push(L(k.sideArc(node.x, node.y, node.r, zBase + node.h - 1.5, P, 32), { tone: "faint" }));
    }

    // Top contact plate
    const zTop = zBase + node.h;
    out.push(L(k.ring(node.x, node.y, node.r - 1.4, zTop, P, isCore ? 36 : 24), { tone: "lo" }));
    out.push(L(k.ring(node.x, node.y, 2.2, zTop, P, 16), { tone: "mid" }));

    // Core terminal contact pin
    out.push(S(k.cylinder(node.x, node.y, 1.6, zTop, 2.2, P, 18), { tone: "hi", lit: isCore }));
    out.push(D([at([node.x, node.y, zTop + 2.2])], { size: 0.5, tone: isCore ? "lit" : "hi" }));
  }

  // Interconnect bus-bar jumping to rail gantry
  out.push(L(k.lineOnTop([NODES.gate.x + NODES.gate.r, NODES.gate.y], [RAIL_X0 - 2, 0], edgeZ + 0.2, P), { tone: "hi" }));
  out.push(D([at([RAIL_X0 - 2, 0, edgeZ + 0.2])], { size: 0.5, tone: "lit" }));

  return out.join("");
}

// 3. Precision Guide Rails & Lead Screw Mechanism
function renderRails() {
  const out = [];

  // Twin hardened ground guide rails (horizontal steel prismatic ways)
  for (const y of [RAIL_Y1, RAIL_Y2]) {
    // Rail base riser
    out.push(S(k.slabOf({ x: RAIL_X0, y: y - 2.5, w: RAIL_X1 - RAIL_X0, d: 5, r: 0.8 }, 0, 2.5, P, 3, 0.3), { tone: "lo", crease: "none" }));
    // Ground precision rail slab
    out.push(S(k.slabOf({ x: RAIL_X0, y: y - 2, w: RAIL_X1 - RAIL_X0, d: 4, r: 1.2 }, 2.5, 3.5, P, 4, 0.4), { tone: "hi", crease: "lo" }));
    // Rail mounting screws
    for (let rx = RAIL_X0 + 8; rx < RAIL_X1 - 4; rx += 28) {
      out.push(D([at([rx, y, 6])], { size: 0.42, tone: "lo" }));
    }
  }

  // Rail End-Stop Blocks
  for (const x of [RAIL_X0 - 5, RAIL_X1]) {
    out.push(S(k.slabOf({ x, y: -29, w: 5.5, d: 58, r: 1.5 }, 0, 8.5, P, 4, 0.6), { tone: "mid" }));
    out.push(D([at([x + 2.7, RAIL_Y1, 8.5]), at([x + 2.7, RAIL_Y2, 8.5])], { size: 0.45 }));
  }

  // Center Lead Screw running between rails
  out.push(S(k.slabOf({ x: RAIL_X0, y: -1.5, w: RAIL_X1 - RAIL_X0, d: 3, r: 0.8 }, 2, 2.5, P, 3, 0.2), { tone: "mid", crease: "none" }));
  // Lead screw threads
  const threadLines = [];
  for (let sx = RAIL_X0 + 6; sx < RAIL_X1 - 6; sx += 4) {
    threadLines.push(k.lineOnTop([sx, -1.2], [sx, 1.2], 4.5, P));
  }
  out.push(L(threadLines.join(""), { tone: "lo" }));

  // Vernier Lead Screw Dial Knob on the right end
  const knobX = RAIL_X1 + 5.5;
  out.push(S(k.cylinder(knobX, 0, 6.5, 1, 7, P, 32, 0.6), { tone: "mid" }));
  out.push(L(k.knurl(knobX, 0, 6.5, 1, 8, 36, P, 0.3), { tone: "lo" }));
  out.push(L(k.sideArc(knobX, 0, 6.5, 4.5, P, 24), { tone: "faint" }));
  out.push(L(k.ring(knobX, 0, 4.5, 8, P, 24), { tone: "lo" }));
  out.push(D([at([knobX, 0, 8])], { size: 0.5, tone: "hi" }));

  return out.join("");
}

// 4. Dial Indicator & Heavy Riser Post (Graph Safety Tolerance Gauge)
function renderDialIndicator() {
  const out = [];

  // Heavy magnetic mounting base on surface plate
  const basePlan = { x: POST[0] - 10, y: POST[1] - 10, w: 20, d: 20, r: 3 };
  out.push(S(k.slabOf(basePlan, 0, 12, P, 4, 0.8), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(basePlan, 2), 12, P), { tone: "faint" }));
  out.push(D(k.corners(basePlan, 4).map(([x, y]) => at([x, y, 12])), { size: 0.45 }));

  // Post collar and vertical hardened steel post
  out.push(S(k.cylinder(POST[0], POST[1], 5, 12, 3.5, P, 28), { tone: "mid" }));
  out.push(S(k.cylinder(POST[0], POST[1], 3.4, 15.5, POST_H - 15.5, P, 28), { tone: "mid", crease: "none" }));
  out.push(L([30, 45, 60].map((z) => k.sideArc(POST[0], POST[1], 3.4, z, P, 16)).join(""), { tone: "faint" }));

  // Clamping block on post
  const clamp = { x: POST[0] - 6, y: POST[1] - 6, w: 12, d: 12, r: 2 };
  out.push(S(k.slabOf(clamp, CLAMP_Z - 5, 10, P, 4, 0.6), { tone: "mid" }));
  out.push(S(k.cylinder(clamp.x + 6, clamp.y + clamp.d + 2.5, 2.5, CLAMP_Z - 2, 5, P, 20), { tone: "mid" }));
  out.push(L(k.knurl(clamp.x + 6, clamp.y + clamp.d + 2.5, 2.5, CLAMP_Z - 2, CLAMP_Z + 3, 18, P), { tone: "lo" }));

  // Extension arm reaching out towards the dial position
  const arm = { x: POST[0] - 2.5, y: DIAL[1] + DIAL_R + 2, w: 5, d: POST[1] - (DIAL[1] + DIAL_R + 2), r: 1.5 };
  out.push(S(k.slabOf(arm, CLAMP_Z - 2, 4, P, 3, 0.5), { tone: "mid" }));

  // Dial Housing
  const [dx, dy] = DIAL;
  out.push(S(k.cylinder(dx, dy, 3.2, DIAL_Z - 6, 6, P, 20), { tone: "mid" }));
  out.push(S(k.cylinder(dx, dy, DIAL_R, DIAL_Z, DIAL_H, P, 64, 0.8), { tone: "hi", crease: "lo" }));
  out.push(L(k.knurl(dx, dy, DIAL_R, DIAL_TOP - 2.6, DIAL_TOP, 72, P, 0.3), { tone: "lo" }));
  out.push(L(k.sideArc(dx, dy, DIAL_R, DIAL_TOP - 2.6, P, 36), { tone: "faint" }));
  out.push(L(k.ring(dx, dy, DIAL_R - 2.0, DIAL_TOP, P, 64), { tone: "lo" }));

  // Radial dial calibration ticks (Minor & Major)
  const ticks = k.radialTicks(dx, dy, DIAL_R - 2.8, 48, 6, DIAL_TOP, [1.4, 2.6], P);
  out.push(L(ticks.minor, { tone: "lo" }), L(ticks.major, { tone: "mid" }));

  // Dial center jewel / hub
  out.push(L(k.ring(dx, dy, 2.0, DIAL_TOP, P, 18), { tone: "mid" }));
  out.push(D([at([dx, dy, DIAL_TOP])], { size: 0.5, tone: "lit" }));

  // Engraved dial label (PASS / FAIL scale notation)
  out.push(k.faceTextSvg(k.topMatrix([dx, dy + 7], DIAL_TOP, P, "x"), "FALKOR·μs", { size: 2.2, tone: "lo", anchor: "middle" }));

  return out.join("");
}


// 5. Target Workpiece: Anatomy Drafting Test Surface & Precision Clamps
function renderWorkpiece() {
  const out = [];

  // Workpiece granite mount plate
  out.push(S(k.slabOf(WORKPIECE, 0, WORKPIECE_H, P, 4, 0.8), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(WORKPIECE, 2), WORKPIECE_H, P), { tone: "faint" }));

  // Concentric engraved inspection framing and calibration rings on workpiece face (closed outlines, zero floating ends)
  const topZ = WORKPIECE_H;
  out.push(L(k.planOutline(k.insetPlan(WORKPIECE, 4.5), topZ, P), { tone: "faint" }));
  out.push(L(k.planOutline(k.insetPlan(WORKPIECE, 8.5), topZ, P), { tone: "faint" }));
  const wcMidX = WORKPIECE.x + WORKPIECE.w / 2;
  const wcMidY = WORKPIECE.y + WORKPIECE.d / 2;
  out.push(L(k.ring(wcMidX, wcMidY, 7.5, topZ, P, 32), { tone: "faint" }));
  out.push(L(k.ring(wcMidX, wcMidY, 2.5, topZ, P, 16), { tone: "faint" }));
  out.push(D([at([wcMidX, wcMidY, topZ])], { size: 0.45, tone: "lo" }));

  // Hold-down step clamps at corners
  const clamp1 = { x: WORKPIECE.x - 3, y: WORKPIECE.y + 4, w: 6, d: 8, r: 1 };
  const clamp2 = { x: WORKPIECE.x - 3, y: WORKPIECE.y + WORKPIECE.d - 12, w: 6, d: 8, r: 1 };
  for (const c of [clamp1, clamp2]) {
    out.push(S(k.slabOf(c, 0, WORKPIECE_H + 2.5, P, 3, 0.5), { tone: "mid" }));
    out.push(D([at([c.x + 3, c.y + 4, WORKPIECE_H + 2.5])], { size: 0.45 }));
  }

  return out.join("");
}

// 6. Sliding Cypher Evaluation Carriage with Safety Solenoid & Trip Latch
function renderCarriage() {
  const out = [];

  // Shadow halo under carriage
  out.push(`<path class="iso-halo" d="${k.haloOf(k.insetPlan(CARRIAGE, 2), CARRIAGE_Z, 0.1, P)}" style="filter:blur(3.5px)"/>`);

  // Heavy carriage body
  out.push(S(k.slabOf(CARRIAGE, CARRIAGE_Z, CARRIAGE_TOP - CARRIAGE_Z, P, 5, 0.8), { tone: "mid" }));

  // Bronze guide bushings at 4 rail contact corners
  const bushingW = 7;
  const bushingD = 8;
  const bushings = [
    { x: CARRIAGE.x, y: RAIL_Y1 - bushingD / 2, w: bushingW, d: bushingD, r: 1.2 },
    { x: CARRIAGE.x + CARRIAGE.w - bushingW, y: RAIL_Y1 - bushingD / 2, w: bushingW, d: bushingD, r: 1.2 },
    { x: CARRIAGE.x, y: RAIL_Y2 - bushingD / 2, w: bushingW, d: bushingD, r: 1.2 },
    { x: CARRIAGE.x + CARRIAGE.w - bushingW, y: RAIL_Y2 - bushingD / 2, w: bushingW, d: bushingD, r: 1.2 },
  ];
  for (const b of bushings) {
    out.push(S(k.slabOf(b, CARRIAGE_Z - 1.5, CARRIAGE_TOP - CARRIAGE_Z + 3, P, 3, 0.5), { tone: "hi", crease: "lo" }));
    out.push(D([at([b.x + bushingW / 2, b.y + bushingD / 2, CARRIAGE_TOP + 1.5])], { size: 0.4 }));
  }

  // Carriage top plate detail & corner rivets
  out.push(L(k.planOutline(k.insetPlan(CARRIAGE, 2.5), CARRIAGE_TOP, P), { tone: "faint" }));
  out.push(D([-12, -4, 4, 12].map((cx) => at([cx, CARRIAGE.y + CARRIAGE.d - 3, CARRIAGE_TOP])), { size: 0.4, tone: "lo" }));

  // FalkorDB Safety Solenoid Housing
  const solX = -4;
  const solY = 9;
  const solR = 7.5;
  const solZ0 = CARRIAGE_TOP;
  const solH = 18;
  out.push(S(k.cylinder(solX, solY, solR, solZ0, solH, P, 32, 0.6), { tone: "mid", crease: "lo" }));
  // Winding grooves & copper coil arcs
  for (let sz = solZ0 + 3; sz <= solZ0 + solH - 3; sz += 3) {
    out.push(L(k.sideArc(solX, solY, solR, sz, P, 24), { tone: "lo" }));
  }
  // Solenoid top terminal cap
  out.push(S(k.cylinder(solX, solY, solR - 1.5, solZ0 + solH, 2.5, P, 24), { tone: "hi" }));
  out.push(D([at([solX, solY, solZ0 + solH + 2.5])], { size: 0.5, tone: "lit" }));

  // Latch Pivot Stand & Trip Lever
  const pivotBlock = { x: 6, y: -10, w: 8, d: 8, r: 1.5 };
  out.push(S(k.slabOf(pivotBlock, CARRIAGE_TOP, 10, P, 3, 0.5), { tone: "mid" }));
  out.push(D([at([pivotBlock.x + 4, pivotBlock.y + 4, CARRIAGE_TOP + 10])], { size: 0.45 }));

  // Knurled thumb screw lock on front of carriage
  const lockX = CARRIAGE.x + CARRIAGE.w / 2;
  const lockY = CARRIAGE.y + CARRIAGE.d + 3;
  out.push(S(k.slabOf({ x: lockX - 2, y: CARRIAGE.y + CARRIAGE.d - 1, w: 4, d: 4, r: 0.8 }, CARRIAGE_Z + 1, 3.5, P, 2), { tone: "mid", crease: "none" }));
  out.push(S(k.cylinder(lockX, lockY + 1.2, 3.2, CARRIAGE_Z, 5.5, P, 20), { tone: "mid" }));
  out.push(L(k.knurl(lockX, lockY + 1.2, 3.2, CARRIAGE_Z, CARRIAGE_Z + 5.5, 18, P), { tone: "lo" }));

  return out.join("");
}

// 7. Safety Trip Latch Arm & Stylus Head (Moves with Solenoid Activation)
function renderLatchAndStylus() {
  const out = [];

  // Trip Latch Arm (pivots down or up depending on FalkorDB safety verification)
  const armPlan = { x: 6, y: -18, w: 4, d: 24, r: 1.2 };
  out.push(S(k.slabOf(armPlan, CARRIAGE_TOP + 8, 3.2, P, 3, 0.4), { tone: "hi", crease: "lo" }));

  // Probe plunger & hardened stylus tip that contacts workpiece
  const stylusX = 8;
  const stylusY = -16;
  out.push(S(k.cylinder(stylusX, stylusY, 2.2, 2, CARRIAGE_TOP + 8, P, 18), { tone: "hi", crease: "none", lit: true }));
  // Diamond/hardened contact tip
  out.push(S(k.cylinder(stylusX, stylusY, 1.2, 0, 2, P, 16), { tone: "hi", lit: true }));
  out.push(D([at([stylusX, stylusY, 0])], { size: 0.45, tone: "lit" }));

  return out.join("");
}

// Function to calculate dial indicator needle position based on safety score
const needleAt = (score) => {
  // score from 0 (FAIL / LATCH TRIPPED) to 1.0 (SAFE / FALKORDB VERIFIED)
  const startAngle = -0.75 * Math.PI; // -135 deg
  const sweep = 1.5 * Math.PI;        // 270 deg sweep
  const angle = startAngle + score * sweep;
  const [dx, dy] = DIAL;
  const len = DIAL_R - 3.5;
  return k.lineOnTop(
    [dx - Math.sin(angle) * 2.5, dy + Math.cos(angle) * 2.5],
    [dx + Math.sin(angle) * len, dy - Math.cos(angle) * len],
    DIAL_TOP + 0.2,
    P
  );
};

// Assemble the Complete Technical Figure
const startX = STOPS[1]; // Start at Verified Safe State
const initialScore = 0.96; // 96% verification score

const svg = k.figureSvg({
  width: WIDTH,
  height: HEIGHT,
  label:
    "An electromechanical graph safety interlock rig for AI coding agents. A heavy surface plate carries a FalkorDB Graph Matrix with nodes for Agent, Intent, FalkorDB Engine, Policy and SafetyGate. A Cypher evaluation gantry slides along twin ground rails; as graph queries verify safety invariants, a solenoid lifts the trip latch to allow the Anatomy drafting stylus to engage the target workpiece.",
  body: [
    renderBasePlate(),
    renderGraphMatrix(),
    renderRails(),
    renderDialIndicator(),
    renderWorkpiece(),
    // Animated Gantry Carriage
    `<g data-part="carriage" transform="${k.translateAlong(P, [startX, 0, 0])}">${renderCarriage()}</g>`,
    // Animated Latch Arm & Tool Stylus
    `<g data-part="stylus" transform="${k.translateAlong(P, [startX, 0, 0])}">${renderLatchAndStylus()}</g>`,
    // Live Dial Indicator Needle
    `<path data-part="needle" class="iso-line" data-tone="lit" data-free="start" d="${needleAt(initialScore)}" style="stroke-width:1.2"/>`,
  ],
});

// Interactive JavaScript runtime for the Blank Page
const live = `
const P = ${JSON.stringify(P)};
const STOPS = ${JSON.stringify(STOPS)};
const REACH = ${JSON.stringify(REACH)};
const DIAL = ${JSON.stringify(DIAL)};
const DIAL_R = ${DIAL_R}, DIAL_TOP = ${DIAL_TOP};

const stage = document.querySelector(".iso-stage");
const svg = stage.querySelector("svg");
const carriage = svg.querySelector('[data-part="carriage"]');
const stylus = svg.querySelector('[data-part="stylus"]');
const needle = svg.querySelector('[data-part="needle"]');
const readout = document.querySelector("[data-readout]");
const still = matchMedia("(prefers-reduced-motion: reduce)");

const needleAt = ${needleAt.toString().replace("k.lineOnTop", "lineOnTop")};
const clamp = (v, min, max) => Math.min(max, Math.max(min, v));

// State definitions: [targetX, cypherQuery, latency, latchStatus, needleScore]
const STATES = [
  {
    x: STOPS[0],
    query: "MATCH (a:Agent)-[:PLANS]->(op:Anatomy)",
    latency: "0.4ms",
    status: "AST PARSE · EVALUATING",
    score: 0.45,
    lift: 0
  },
  {
    x: STOPS[1],
    query: "MATCH (a)-[:PERMITTED]->(w:Workpiece) WHERE c.isolated=true",
    latency: "0.9ms",
    status: "FALKORDB VERIFIED · LATCH OPEN [SAFE]",
    score: 0.98,
    lift: 4.5
  },
  {
    x: STOPS[2],
    query: "MATCH (a)-[r:UNCHECKED]->(fs:System) RETURN VIOLATION",
    latency: "1.4ms",
    status: "INVARIANT VIOLATION · LATCH TRIPPED [BLOCKED]",
    score: 0.12,
    lift: -1.5
  }
];

let curX = ${startX}, targetX = curX;
let curLift = 4.5, targetLift = curLift;
let curScore = ${initialScore}, targetScore = curScore;
let stateIdx = 1;
let frame = 0, last = 0, clock = 0, touring = true, visible = false, idleTimer = 0;

function updateState(idx) {
  stateIdx = clamp(idx, 0, STATES.length - 1);
  const s = STATES[stateIdx];
  targetX = s.x;
  targetLift = s.lift;
  targetScore = s.score;
  const text = s.latency + " · " + s.status;
  if (readout.textContent !== text) readout.textContent = text;
  stage.setAttribute("aria-valuenow", String(stateIdx));
  stage.setAttribute("aria-valuetext", text);
}

function draw() {
  carriage.setAttribute("transform", translateAlong(P, [curX, 0, 0]));
  stylus.setAttribute("transform", translateAlong(P, [curX, 0, curLift]));
  needle.setAttribute("d", needleAt(curScore));
}

function tick(now) {
  const dt = last ? Math.min((now - last) / 1000, 1 / 30) : 1 / 60;
  last = now;
  const calm = still.matches;

  if (touring) {
    clock += dt;
    const cycle = Math.floor(clock / 2.8) % STATES.length;
    if (cycle !== stateIdx) updateState(cycle);
  }

  // Smooth exponential interpolation
  const speed = calm ? 1 : (1 - Math.exp(-dt / 0.22));
  curX += (targetX - curX) * speed;
  curLift += (targetLift - curLift) * speed;
  curScore += (targetScore - curScore) * speed;

  if (Math.abs(targetX - curX) < 0.02) curX = targetX;
  if (Math.abs(targetLift - curLift) < 0.02) curLift = targetLift;
  if (Math.abs(targetScore - curScore) < 0.005) curScore = targetScore;

  draw();

  const settled = !touring && curX === targetX && curLift === targetLift && curScore === targetScore;
  frame = visible && !settled ? requestAnimationFrame(tick) : 0;
}

const run = () => {
  if (!frame && visible) {
    last = 0;
    frame = requestAnimationFrame(tick);
  }
};

const steer = (nextIdx) => {
  touring = false;
  clearTimeout(idleTimer);
  updateState(nextIdx);
  idleTimer = setTimeout(() => {
    touring = !still.matches;
    clock = 0;
    run();
  }, 4200);
  run();
};

new IntersectionObserver((entries) => {
  visible = entries[entries.length - 1].isIntersecting;
  if (visible) run();
}, { rootMargin: "120px 0px" }).observe(stage);

if (still.matches) touring = false;

stage.addEventListener("pointermove", (event) => {
  const box = svg.getBoundingClientRect();
  const share = clamp((event.clientX - box.left) / box.width, 0, 1);
  const nextIdx = Math.round(share * (STATES.length - 1));
  steer(nextIdx);
});

stage.addEventListener("pointerleave", () => steer(stateIdx));

stage.addEventListener("keydown", (event) => {
  if (event.key === "ArrowRight" || event.key === "ArrowDown") {
    event.preventDefault();
    steer(Math.min(STATES.length - 1, stateIdx + 1));
  } else if (event.key === "ArrowLeft" || event.key === "ArrowUp") {
    event.preventDefault();
    steer(Math.max(0, stateIdx - 1));
  } else if (event.key === "Home") {
    event.preventDefault();
    steer(0);
  } else if (event.key === "End") {
    event.preventDefault();
    steer(STATES.length - 1);
  }
});

updateState(1);
draw();
`;

// HTML Plate & Framed Card
const body = k.plateHtml({
  fig: "Fig 1",
  title: "FalkorDB Graph Safety Interlock",
  hint: "Hover or use arrow keys",
  readout: "0.9ms · FALKORDB VERIFIED · LATCH OPEN",
  keys: [
    { mark: "lit", label: "Hardened stylus & dial needle: live gated executor and Cypher safety score" },
    { mark: "raised", label: "FalkorDB Graph Matrix (Agent, Intent, Kernel, Policy, Gate) with conductive relation rails" },
    { mark: "lo", label: "Scanning gantry with trip-latch solenoid, ground rails, and vernier lead screw" },
  ],
  caption:
    "An electromechanical graph safety layer for AI coding agents, powered by FalkorDB. The agent's intended actions (such as generating code or executing complex geometry scripts with the anatomy skill) are mapped into an in-memory knowledge graph. FalkorDB executes sub-millisecond Cypher graph traversals (<1ms) via GraphBLAS sparse matrix operations. When invariant paths satisfy safety policies, the solenoid activates, lifting the trip-latch and allowing the anatomy tool stylus to engage the workpiece; any boundary violation trips the latch and arrests execution.",
  body: `<div class="iso-stage" tabindex="0" role="slider" aria-label="FalkorDB Safety Interlock: Arrow keys step through Cypher evaluation states" aria-valuemin="0" aria-valuemax="2" aria-valuenow="1">${svg}</div>`,
});

// Output Standalone HTML page for testing
const filename = theme === "light" ? "falkordb-safety-layer-light.html" : "falkordb-safety-layer.html";
const outputPath = `/Users/bombermac/hackathon/Warrant/${filename}`;
const page = k.pageHtml({
  title: "FalkorDB Graph-Powered Safety Layer for AI Coding Agents",
  theme,
  body,
  script: kitScript() + live,
});

writeFileSync(outputPath, page);
console.log("Successfully wrote standalone testing page to:", outputPath);
