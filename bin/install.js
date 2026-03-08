#!/usr/bin/env node

/**
 * DevAgent Installer
 * Installs DevAgent skills and commands into Claude Code global or local config.
 *
 * Usage:
 *   npx devagent-cc@latest              # interactive
 *   npx devagent-cc --global            # install globally (~/.claude/)
 *   npx devagent-cc --local             # install locally (./.claude/)
 *   npx devagent-cc --global --update   # update existing install
 *   npx devagent-cc --global --uninstall
 */

const fs   = require('fs');
const path = require('path');
const os   = require('os');
const readline = require('readline');

// ─── Config ────────────────────────────────────────────────────────────────

const REPO     = 'https://github.com/IAZ-A3/DevAgent';
const VERSION  = require('../package.json').version;
const PKG_ROOT = path.resolve(__dirname, '..');   // root of the npm package

// What gets installed where
// [sourcePath (in package), targetPath (relative to claudeDir)]
const INSTALL_MAP = [
  // Commands — every file in deva-commands/ → .claude/commands/
  { src: 'deva-commands', dest: 'commands', type: 'dir' },

  // Skills — entire skills/ tree → .claude/skills/deva/
  { src: 'skills',        dest: 'skills/deva', type: 'dir' },

  // Registry
  { src: 'registry.md',  dest: 'registry.md', type: 'file' },
];

// CLAUDE.md goes to project root (global) or project root (local) — NOT inside .claude/
// PROJECT templates go alongside CLAUDE.md
const ROOT_FILES = [
  'CLAUDE.md',
  'PROJECT-base-template.md',
  'PROJECT-web-template.md',
  'PROJECT-macos-template.md',
];

// ─── CLI args ───────────────────────────────────────────────────────────────

const args       = process.argv.slice(2);
const isGlobal   = args.includes('--global') || args.includes('-g');
const isLocal    = args.includes('--local')  || args.includes('-l');
const isUpdate   = args.includes('--update');
const isUninstall = args.includes('--uninstall');
const isInteractive = !isGlobal && !isLocal;

// ─── Helpers ────────────────────────────────────────────────────────────────

function ask(rl, question) {
  return new Promise(resolve => rl.question(question, resolve));
}

function ensureDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

function copyFile(src, dest) {
  ensureDir(path.dirname(dest));
  fs.copyFileSync(src, dest);
}

function copyDir(srcDir, destDir) {
  ensureDir(destDir);
  const entries = fs.readdirSync(srcDir, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath  = path.join(srcDir, entry.name);
    const destPath = path.join(destDir, entry.name);
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      copyFile(srcPath, destPath);
    }
  }
}

function countFiles(dirPath) {
  if (!fs.existsSync(dirPath)) return 0;
  let count = 0;
  const entries = fs.readdirSync(dirPath, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.isDirectory()) {
      count += countFiles(path.join(dirPath, entry.name));
    } else {
      count++;
    }
  }
  return count;
}

function removeDir(dirPath) {
  if (fs.existsSync(dirPath)) {
    fs.rmSync(dirPath, { recursive: true, force: true });
  }
}

function getInstalledVersion(claudeDir) {
  // Read version from the installed CLAUDE.md
  // Looks for line: # DevAgent version: X.Y.Z
  const claudeMd = path.join(path.dirname(claudeDir), 'CLAUDE.md');
  if (!fs.existsSync(claudeMd)) return null;
  const content = fs.readFileSync(claudeMd, 'utf8');
  const match = content.match(/# DevAgent version:\s*([\d.]+)/);
  return match ? match[1] : null;
}

function writeLastCheckTimestamp(claudeDir) {
  const file = path.join(claudeDir, 'skills', 'deva', 'last-update-check.txt');
  ensureDir(path.dirname(file));
  fs.writeFileSync(file, new Date().toISOString());
}

// ─── Install ────────────────────────────────────────────────────────────────

function install(claudeDir, rootDir, mode) {
  console.log('\n📦 Installing DevAgent v' + VERSION + '...\n');

  let fileCount = 0;

  // 1. Install commands and skills into .claude/
  for (const entry of INSTALL_MAP) {
    const srcPath  = path.join(PKG_ROOT, entry.src);
    const destPath = path.join(claudeDir, entry.dest);

    if (entry.type === 'dir') {
      copyDir(srcPath, destPath);
      const n = countFiles(srcPath);
      fileCount += n;
      console.log('  ✓ ' + entry.dest + '/  (' + n + ' files)');
    } else {
      copyFile(srcPath, destPath);
      fileCount++;
      console.log('  ✓ ' + entry.dest);
    }
  }

  // 2. Install CLAUDE.md and templates into rootDir
  for (const file of ROOT_FILES) {
    const srcPath  = path.join(PKG_ROOT, file);
    const destPath = path.join(rootDir, file);
    if (fs.existsSync(srcPath)) {
      copyFile(srcPath, destPath);
      fileCount++;
      console.log('  ✓ ' + file);
    }
  }

  // 3. Write last-update-check timestamp
  writeLastCheckTimestamp(claudeDir);

  console.log('\n✅ DevAgent v' + VERSION + ' installed successfully!');
  console.log('   ' + fileCount + ' files installed to: ' + claudeDir);
  console.log('\n🚀 Get started:');

  if (mode === 'global') {
    console.log('   Open any project in Claude Code and type /deva:new or /deva:onboard');
  } else {
    console.log('   Open this project in Claude Code and type /deva:new or /deva:onboard');
  }

  console.log('\n📖 Docs: ' + REPO);
  console.log('');
}

// ─── Uninstall ──────────────────────────────────────────────────────────────

function uninstall(claudeDir, rootDir) {
  console.log('\n🗑  Uninstalling DevAgent...\n');

  // Remove commands
  const commandsDir = path.join(claudeDir, 'commands');
  if (fs.existsSync(commandsDir)) {
    const files = fs.readdirSync(commandsDir).filter(f => f.startsWith('deva:'));
    for (const file of files) {
      fs.unlinkSync(path.join(commandsDir, file));
      console.log('  ✓ Removed commands/' + file);
    }
  }

  // Remove skills/deva
  const skillsDevaDir = path.join(claudeDir, 'skills', 'deva');
  if (fs.existsSync(skillsDevaDir)) {
    removeDir(skillsDevaDir);
    console.log('  ✓ Removed skills/deva/');
  }

  // Remove registry.md
  const registry = path.join(claudeDir, 'registry.md');
  if (fs.existsSync(registry)) {
    fs.unlinkSync(registry);
    console.log('  ✓ Removed registry.md');
  }

  // Remove CLAUDE.md and templates from root
  for (const file of ROOT_FILES) {
    const filePath = path.join(rootDir, file);
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
      console.log('  ✓ Removed ' + file);
    }
  }

  console.log('\n✅ DevAgent uninstalled.');
  console.log('   Your project files (docs/, PROJECT.md, .claude/skills/state/) were not touched.\n');
}

// ─── Main ───────────────────────────────────────────────────────────────────

async function main() {
  console.log('');
  console.log('  ██████╗ ███████╗██╗   ██╗ █████╗ ');
  console.log('  ██╔══██╗██╔════╝██║   ██║██╔══██╗');
  console.log('  ██║  ██║█████╗  ██║   ██║███████║');
  console.log('  ██║  ██║██╔══╝  ╚██╗ ██╔╝██╔══██║');
  console.log('  ██████╔╝███████╗ ╚████╔╝ ██║  ██║');
  console.log('  ╚═════╝ ╚══════╝  ╚═══╝  ╚═╝  ╚═╝');
  console.log('');
  console.log('  DevAgent v' + VERSION + ' — Claude Code Development Agent');
  console.log('  ' + REPO);
  console.log('');

  let scope; // 'global' | 'local'

  if (isGlobal) {
    scope = 'global';
  } else if (isLocal) {
    scope = 'local';
  } else {
    // Interactive prompt
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

    console.log('Where would you like to install DevAgent?\n');
    console.log('  1) Global — available in ALL projects  (~/.claude/)  [recommended]');
    console.log('  2) Local  — this project only          (./.claude/)');
    console.log('');

    let choice = '';
    while (!['1', '2'].includes(choice)) {
      choice = (await ask(rl, 'Enter 1 or 2: ')).trim();
    }

    scope = choice === '1' ? 'global' : 'local';
    rl.close();
  }

  // Resolve paths
  let claudeDir, rootDir;

  if (scope === 'global') {
    rootDir   = os.homedir();
    claudeDir = path.join(os.homedir(), '.claude');
  } else {
    rootDir   = process.cwd();
    claudeDir = path.join(process.cwd(), '.claude');
  }

  // Check for existing install
  const installedVersion = getInstalledVersion(claudeDir);

  if (isUninstall) {
    uninstall(claudeDir, rootDir);
    return;
  }

  if (installedVersion && !isUpdate) {
    console.log('  ⚠️  DevAgent v' + installedVersion + ' is already installed at: ' + claudeDir);
    console.log('');

    if (installedVersion === VERSION) {
      console.log('  ✓ Already up to date (v' + VERSION + ')');
      console.log('');
      return;
    }

    console.log('  New version available: v' + installedVersion + ' → v' + VERSION);
    console.log('');

    if (isInteractive) {
      const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
      const answer = (await ask(rl, '  Update to v' + VERSION + '? (y/n): ')).trim().toLowerCase();
      rl.close();
      if (answer !== 'y' && answer !== 'yes') {
        console.log('\n  Cancelled. No changes made.\n');
        return;
      }
    }
  }

  install(claudeDir, rootDir, scope);
}

main().catch(err => {
  console.error('\n❌ Installation failed:', err.message);
  process.exit(1);
});
