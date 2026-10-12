# Run golden cases end-to-end with the Claude Code CLI as executor:
#   prepare (temp agent home) -> claude -p inside that home -> assert.
# Usage:
#   pwsh dev/run_cases_claude.ps1 -Ids add_inventory,eaten_up_keeps_zero [-Model haiku]
#   pwsh dev/run_cases_claude.ps1            # all dev/golden_cases
# Results: dev/.golden_results/summary.tsv plus per-case agent/assert logs (gitignored).
param(
  [string[]]$Ids,
  [string]$Model  = "haiku",
  [string]$Python = "python",
  [string]$Claude = "claude"
)
$repo = Split-Path $PSScriptRoot -Parent
$out  = Join-Path $PSScriptRoot ".golden_results"
New-Item -ItemType Directory -Force $out | Out-Null
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
if (-not $Ids) { $Ids = Get-ChildItem (Join-Path $PSScriptRoot "golden_cases\*.json") | ForEach-Object BaseName }

foreach ($id in $Ids) {
  $p = & $Python -X utf8 (Join-Path $PSScriptRoot "run_golden.py") prepare $id | ConvertFrom-Json
  New-Item -ItemType Directory -Force $p.home | Out-Null
  # The agent runs inside the temp home; the repo is added only so it can read SKILL.md and references.
  Push-Location $p.home
  $sw = [Diagnostics.Stopwatch]::StartNew()
  $p.delegation_prompt | & $Claude -p --model $Model --add-dir $repo --permission-mode acceptEdits `
      --allowedTools "Read,Write,Edit,Glob,Grep" *> (Join-Path $out "$id.agent.txt")
  $agentExit = $LASTEXITCODE
  $sw.Stop()
  Pop-Location
  & $Python -X utf8 (Join-Path $PSScriptRoot "run_golden.py") assert $id --home $p.home *> (Join-Path $out "$id.assert.txt")
  $result = if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
  $line = "{0}`t{1}`t{2}`tagent_exit={3}`t{4}s`t{5}" -f (Get-Date -Format s), $id, $result, $agentExit, [int]$sw.Elapsed.TotalSeconds, $p.home
  Add-Content -Path (Join-Path $out "summary.tsv") -Value $line -Encoding utf8
  $line
}
