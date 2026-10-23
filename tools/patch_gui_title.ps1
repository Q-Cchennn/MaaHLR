param(
    [string]$AppDirectory = (Join-Path $PSScriptRoot '../install/MaaHLR-Windows'),
    [string]$CecilPath = (Join-Path $PSScriptRoot '../install/downloads/cecil/lib/net40/Mono.Cecil.dll')
)
$ErrorActionPreference = 'Stop'
Add-Type -Path (Resolve-Path -LiteralPath $CecilPath)
$corePath = Join-Path $AppDirectory 'libs/MFAAvalonia.Core.dll'
$backupPath = "$corePath.before-title-version.bak"
if (Test-Path -LiteralPath $backupPath) {
    Write-Output 'Title/version patch already applied.'
    exit 0
}
$reader = New-Object Mono.Cecil.ReaderParameters
$reader.InMemory = $true
$assembly = [Mono.Cecil.AssemblyDefinition]::ReadAssembly($corePath, $reader)
try {
    $type = $assembly.MainModule.Types | Where-Object FullName -EQ 'MFAAvalonia.ViewModels.Windows.RootViewModel'
    $setName = $type.Methods | Where-Object Name -EQ 'set_ResourceName'
    if (-not $setName) { throw 'Unsupported GUI: ResourceName setter not found.' }
    foreach ($name in @('ShowCustomTitle', 'ShowCustomTitleAndFallBack')) {
        $method = $type.Methods | Where-Object Name -EQ $name
        $calls = @($method.Body.Instructions | Where-Object {
            $_.Operand -is [Mono.Cecil.MethodReference] -and $_.Operand.Name -EQ 'set_IsResourceNameVisible'
        })
        if ($calls.Count -ne 1 -or $calls[0].Previous.OpCode.Code.ToString() -ne 'Ldc_I4_0') {
            throw "Unsupported GUI title method: $name"
        }
        $call = $calls[0]
        $anchor = $call.Previous.Previous
        $il = $method.Body.GetILProcessor()
        # Keep the existing subdued resource-version TextBlock visible, while
        # clearing the duplicate resource name beside the custom heading.
        $il.InsertBefore($anchor, $il.Create([Mono.Cecil.Cil.OpCodes]::Ldarg_0))
        $il.InsertBefore($anchor, $il.Create([Mono.Cecil.Cil.OpCodes]::Ldstr, ''))
        $il.InsertBefore($anchor, $il.Create([Mono.Cecil.Cil.OpCodes]::Call, $setName))
        $call.Previous.OpCode = [Mono.Cecil.Cil.OpCodes]::Ldc_I4_1
    }
    Copy-Item -LiteralPath $corePath -Destination $backupPath
    $assembly.Write($corePath)
    Write-Output 'Restored native small version text beside custom GUI heading.'
} finally {
    $assembly.Dispose()
}
