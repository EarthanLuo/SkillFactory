param(
    [switch]$All
)

$ErrorActionPreference = "Stop"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$skillsRoot = Join-Path $repoRoot "skills"

function Add-SourceSkill([hashtable]$sources, [string]$skillName, [string]$sourceDir) {
    if ($sources.ContainsKey($skillName) -and $sources[$skillName] -ne $sourceDir) {
        throw "Skill '$skillName' has multiple sources: '$($sources[$skillName])' and '$sourceDir'. Rename one source before committing."
    }
    $sources[$skillName] = $sourceDir
}

function Get-ChangedPaths {
    if ($All) {
        $allPaths = @()
        foreach ($factoryDir in @(Get-ChildItem -LiteralPath (Join-Path $repoRoot "factory") -Directory)) {
            $allPaths += "factory/$($factoryDir.Name)/SKILL.md"
        }
        foreach ($projectDir in @(Get-ChildItem -LiteralPath (Join-Path $repoRoot "workspace") -Directory)) {
            $skillRoot = Join-Path $projectDir.FullName "skill"
            if (Test-Path -LiteralPath $skillRoot -PathType Container) {
                foreach ($skillDir in @(Get-ChildItem -LiteralPath $skillRoot -Directory)) {
                    $allPaths += "workspace/$($projectDir.Name)/skill/$($skillDir.Name)/SKILL.md"
                }
            }
        }
        return $allPaths
    }

    $lines = @(git -C $repoRoot status --porcelain=v1 --untracked-files=all)
    if ($LASTEXITCODE -ne 0) {
        throw "Unable to read Git status."
    }

    $paths = @()
    foreach ($line in $lines) {
        if ([string]::IsNullOrWhiteSpace($line) -or $line.Length -lt 4) {
            continue
        }
        $rawPath = $line.Substring(3).Trim()
        if ($rawPath -match " -> ") {
            $rawPath = ($rawPath -split " -> ")[-1]
        }
        $paths += $rawPath.Trim('"')
    }
    return $paths
}

function Get-SourceSkills([string[]]$changedPaths) {
    $sources = @{}
    foreach ($path in $changedPaths) {
        $normalized = $path.Replace("\", "/")
        $parts = $normalized.Split("/", [System.StringSplitOptions]::RemoveEmptyEntries)

        if ($parts.Length -ge 2 -and $parts[0] -eq "factory") {
            $skillName = $parts[1]
            $sourceDir = Join-Path $repoRoot (Join-Path "factory" $skillName)
            Add-SourceSkill $sources $skillName $sourceDir
            continue
        }

        if ($parts.Length -ge 4 -and $parts[0] -eq "workspace") {
            $skillIndex = [Array]::IndexOf($parts, "skill")
            if ($skillIndex -ge 0 -and $skillIndex + 1 -lt $parts.Length) {
                $skillName = $parts[$skillIndex + 1]
                $projectParts = $parts[0..($skillIndex + 1)]
                $sourceDir = $repoRoot
                foreach ($part in $projectParts) {
                    $sourceDir = Join-Path $sourceDir $part
                }
                Add-SourceSkill $sources $skillName $sourceDir
            }
        }
    }
    return $sources
}

function Sync-Skill([string]$skillName, [string]$sourceDir) {
    $destinationDir = Join-Path $skillsRoot $skillName
    if (Test-Path -LiteralPath $sourceDir -PathType Container) {
        if (Test-Path -LiteralPath $destinationDir) {
            Remove-Item -LiteralPath $destinationDir -Recurse -Force
        }
        New-Item -ItemType Directory -Force $skillsRoot | Out-Null
        Copy-Item -LiteralPath $sourceDir -Destination $destinationDir -Recurse -Force
        Write-Output "Synced $skillName from $sourceDir"
    } elseif (Test-Path -LiteralPath $destinationDir) {
        Remove-Item -LiteralPath $destinationDir -Recurse -Force
        Write-Output "Removed deleted Skill $skillName"
    }

    & git -C $repoRoot add -A -- (Join-Path "skills" $skillName)
    if ($LASTEXITCODE -ne 0) {
        throw "Unable to stage skills/$skillName."
    }
}

$sources = Get-SourceSkills (Get-ChangedPaths)
foreach ($skillName in ($sources.Keys | Sort-Object)) {
    Sync-Skill $skillName $sources[$skillName]
}
