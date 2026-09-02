// Refreshes pachete.js / site/pachete.js from the RapidAPI football feed.
// Plain deterministic script — no AI involved, so no hallucination risk and
// no API-token cost. Run daily by .github/workflows/refresh-fixtures.yml.
//
// For each tracked competition, if every currently-listed match has already
// been played, this fetches the next upcoming round and replaces that
// competition's block. If the current round still has matches in the
// future, that competition is left untouched this run — we never overwrite
// a round while its packs might still be getting built.
//
// Requires Node 18+ (global fetch) and env var RAPIDAPI_KEY.

import { readFileSync, writeFileSync } from 'node:fs';
import vm from 'node:vm';

const HOST = 'https://free-api-live-football-data.p.rapidapi.com';
const API_KEY = process.env.RAPIDAPI_KEY;
if (!API_KEY) {
  console.error('Missing RAPIDAPI_KEY env var.');
  process.exit(1);
}
const HEADERS = {
  'x-rapidapi-host': 'free-api-live-football-data.p.rapidapi.com',
  'x-rapidapi-key': API_KEY,
};

// Tracked competitions: RapidAPI leagueId -> manifest `comp` label + file-slug prefix.
const COMPS = [
  { id: 47, comp: 'Premier League', abbr: 'pl' },
  { id: 53, comp: 'Ligue 1', abbr: 'l1' },
  { id: 87, comp: 'LaLiga', abbr: 'laliga' },
  { id: 55, comp: 'Serie A', abbr: 'seriea' },
  { id: 54, comp: 'Bundesliga', abbr: 'bundesliga' },
  { id: 189, comp: 'Superliga', abbr: 'sl' },
];
const DAYS_AHEAD = 21; // scan window when a competition's round has finished

const ROOT_FILE = new URL('../pachete.js', import.meta.url);
const SITE_FILE = new URL('../site/pachete.js', import.meta.url);

function slugify(s) {
  return s
    .normalize('NFD').replace(/[̀-ͯ]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-+|-+$)/g, '');
}

function roundLabel(stage) {
  if (stage == null || stage === '') return 'n/d';
  const raw = String(stage).trim();
  if (/^\d+$/.test(raw)) return 'Etapa ' + raw;
  const k = raw.toLowerCase().replace(/[-_/]+/g, ' ').replace(/\s+/g, ' ').trim();
  const exact = {
    final: 'Finala', 'semi final': 'Semifinale', 'semi finals': 'Semifinale',
    'quarter final': 'Sferturi de finală', 'quarter finals': 'Sferturi de finală',
    'round of 16': 'Optimi de finală', 'round of 32': 'Șaisprezecimi',
    'group stage': 'Faza grupelor', 'play off': 'Baraj', playoffs: 'Baraj',
    qualification: 'Preliminarii', qualifying: 'Preliminarii',
  };
  if (exact[k]) return exact[k];
  const m = k.match(/^(?:round|matchday|round no) (\d+)$/);
  if (m) return 'Etapa ' + m[1];
  return raw || 'n/d';
}

function roundNumber(et) {
  const m = /Etapa (\d+)/.exec(et || '');
  return m ? m[1] : slugify(et || 'runda');
}

function key(d) {
  const p = (n) => String(n).padStart(2, '0');
  return d.getFullYear() + p(d.getMonth() + 1) + p(d.getDate());
}

function localDate(utc) {
  return new Date(utc).toLocaleDateString('en-CA', { timeZone: 'Europe/Bucharest' });
}
function localTime(utc) {
  return new Date(utc).toLocaleTimeString('ro-RO', {
    hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Bucharest', hour12: false,
  });
}

async function fetchDay(d) {
  const url = `${HOST}/football-get-matches-by-date?date=${key(d)}`;
  const r = await fetch(url, { headers: HEADERS });
  if (!r.ok) throw new Error(`API ${r.status} for ${key(d)}`);
  const j = await r.json();
  if (j.status !== 'success') throw new Error(j.message || 'API returned non-success');
  return j.response.matches || [];
}

function loadManifest(fileUrl) {
  const src = readFileSync(fileUrl, 'utf8');
  const sandbox = { window: {} };
  vm.createContext(sandbox);
  vm.runInContext(src, sandbox);
  return sandbox.window.PM_PACHETE || [];
}

function render(entries) {
  const lines = [];
  lines.push('// Manifestul arhivei publice. Fiecare pachet exportat ca PDF în site/pachete/');
  lines.push('// primește o intrare aici. `ready: false` = datele sunt culese, PDF-ul nu e încă exportat.');
  lines.push('//');
  lines.push(`// Actualizat automat ${new Date().toISOString().slice(0, 10)} de refresh-fixtures.yml.`);
  lines.push('window.PM_PACHETE = [');
  let lastComp = null;
  entries.forEach((e, i) => {
    if (e.comp !== lastComp) {
      if (lastComp !== null) lines.push('');
      lines.push(`  // ---- ${e.comp} — ${e.et} ----`);
      lastComp = e.comp;
    }
    const esc = (s) => String(s).replace(/'/g, "\\'");
    lines.push(
      `  { comp: '${esc(e.comp)}', et: '${esc(e.et)}', date: '${e.date}', ko: '${esc(e.ko)}', ` +
      `home: '${esc(e.home)}', away: '${esc(e.away)}', venue: '${esc(e.venue)}', ` +
      `file: '${e.file}', ready: ${e.ready ? 'true' : 'false'} }${i < entries.length - 1 ? ',' : ''}`
    );
  });
  lines.push('];');
  lines.push('');
  return lines.join('\n');
}

async function main() {
  const manifest = loadManifest(ROOT_FILE);
  const today = new Date();
  const todayKey = key(today);

  // Venue lookup seeded from whatever the manifest already knows per team.
  const venueByTeam = {};
  manifest.forEach((e) => {
    if (e.venue && e.venue !== 'n/d') venueByTeam[e.home] = e.venue;
  });

  const out = [];
  for (const c of COMPS) {
    const current = manifest.filter((e) => e.comp === c.comp);
    const stillUpcoming = current.some((e) => e.date >= todayKey.slice(0, 4) + '-' + todayKey.slice(4, 6) + '-' + todayKey.slice(6, 8));
    if (current.length && stillUpcoming) {
      // Current round isn't finished yet — leave this competition alone.
      out.push(...current);
      continue;
    }

    // Scan forward for this competition's next round.
    let found = [];
    let windowStart = null;
    for (let i = 0; i < DAYS_AHEAD; i++) {
      const d = new Date(today.getFullYear(), today.getMonth(), today.getDate() + i);
      let matches;
      try {
        matches = await fetchDay(d);
      } catch (e) {
        console.error(`Skipping ${key(d)}: ${e.message}`);
        continue;
      }
      const mine = matches.filter((m) => m.leagueId === c.id && !(m.status && m.status.finished));
      if (mine.length) {
        if (windowStart === null) windowStart = i;
        if (i <= windowStart + 3) found.push(...mine);
        else break;
      } else if (windowStart !== null && i > windowStart + 3) {
        break;
      }
    }

    if (!found.length) {
      console.log(`No upcoming ${c.comp} fixtures found in the next ${DAYS_AHEAD} days — leaving as-is.`);
      out.push(...current);
      continue;
    }

    const byMatch = new Map(current.map((e) => [e.home + '|' + e.away + '|' + e.date, e]));
    const et = roundLabel(found[0].tournamentStage);
    const n = roundNumber(et);
    const entries = found.map((m) => {
      const date = m.status && m.status.utcTime ? localDate(m.status.utcTime) : 'n/d';
      const ko = m.status && m.status.utcTime ? localTime(m.status.utcTime) : 'n/d';
      const home = m.home.name, away = m.away.name;
      const existing = byMatch.get(home + '|' + away + '|' + date);
      return {
        comp: c.comp,
        et: roundLabel(m.tournamentStage),
        date, ko, home, away,
        venue: venueByTeam[home] || 'n/d',
        file: existing ? existing.file : `pachete/${c.abbr}-e${n}-${slugify(home)}-${slugify(away)}.pdf`,
        ready: existing ? existing.ready : false,
      };
    }).sort((a, b) => (a.date + a.ko).localeCompare(b.date + b.ko));

    out.push(...entries);
  }

  const rendered = render(out);
  const before = readFileSync(ROOT_FILE, 'utf8');
  if (rendered.trim() === before.trim()) {
    console.log('No changes.');
    return;
  }
  writeFileSync(ROOT_FILE, rendered);
  writeFileSync(SITE_FILE, rendered);
  console.log('Manifest updated.');
}

main().catch((e) => { console.error(e); process.exit(1); });
