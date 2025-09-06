# Nano Agent MCP Server - Windows Installation Script
# PowerShell script for Windows users

param(
    [switch]$Quick,
    [switch]$NoClaudeDesktop
)

# Colors and formatting
function Write-Header { Write-Host $args[0] -ForegroundColor Blue -BackgroundColor White }
function Write-Step { Write-Host "▶ $($args[0])" -ForegroundColor Blue }
function Write-Success { Write-Host "✅ $($args[0])" -ForegroundColor Green }
function Write-Warning { Write-Host "⚠️  $($args[0])" -ForegroundColor Yellow }
function Write-Error { Write-Host "❌ $($args[0])" -ForegroundColor Red }

# Configuration
$InstallDir = "$env:USERPROFILE\.nano-agent"
$ConfigDir = "$env:USERPROFILE\.nano-cli"

Write-Header "🤖 Nano Agent MCP Server - Windows Installation"
Write-Host "=================================================" -ForegroundColor Blue
Write-Host ""

function Test-Requirements {
    Write-Step "Checking system requirements..."
    
    # Check Python
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python (\d+\.\d+)") {
            $version = [version]$matches[1]
            if ($version -ge [version]"3.9") {
                Write-Success "Python $($matches[1]) found"
                return $true
            } else {
                Write-Error "Python 3.9+ required. Found: $($matches[1])"
                Write-Host "Please install Python 3.9+ from https://python.org"
                return $false
            }
        }
    } catch {
        Write-Error "Python not found"
        Write-Host "Please install Python 3.9+ from https://python.org"
        return $false
    }
}

function Install-UV {
    Write-Step "Installing uv package manager..."
    
    if (Get-Command uv -ErrorAction SilentlyContinue) {
        Write-Success "uv already installed"
        return
    }
    
    try {
        # Download and run uv installer
        Invoke-WebRequest -Uri "https://astral.sh/uv/install.ps1" -UseBasicParsing | Invoke-Expression
        
        # Add to PATH for current session
        $uvPath = "$env:USERPROFILE\.cargo\bin"
        if (Test-Path $uvPath) {
            $env:PATH = "$uvPath;$env:PATH"
        }
        
        if (Get-Command uv -ErrorAction SilentlyContinue) {
            Write-Success "uv installed successfully"
        } else {
            Write-Error "uv installation failed"
            exit 1
        }
    } catch {
        Write-Error "Failed to install uv: $($_.Exception.Message)"
        exit 1
    }
}

function Install-NanoAgent {
    Write-Step "Installing Nano Agent..."
    
    # Create directories
    New-Item -Path $InstallDir -ItemType Directory -Force | Out-Null
    New-Item -Path $ConfigDir -ItemType Directory -Force | Out-Null
    
    # Copy current directory to install location (for development)
    $currentDir = Get-Location
    if (Test-Path "$currentDir\pyproject.toml") {
        Write-Step "Copying nano-agent files..."
        Copy-Item -Path $currentDir -Destination "$InstallDir\nano-agent" -Recurse -Force
    } else {
        Write-Error "Unable to find nano-agent source. Please run from nano-agent directory."
        exit 1
    }
    
    # Change to install directory
    Set-Location "$InstallDir\nano-agent\apps\nano_agent_mcp_server"
    
    # Copy environment file
    if ((Test-Path ".env.sample") -and !(Test-Path ".env")) {
        Copy-Item ".env.sample" ".env"
        Write-Success "Created .env file"
    }
    
    # Install dependencies and tool
    Write-Step "Installing dependencies..."
    uv sync
    uv tool install --force .
    
    Write-Success "Nano Agent installed"
}

function Setup-Configuration {
    Write-Step "Setting up configuration..."
    
    # Create default config
    $config = @{
        default_model = "gpt-oss:20b"
        default_provider = "ollama"
        default_temperature = 0.7
        default_max_tokens = 4000
    } | ConvertTo-Json -Depth 3
    
    $config | Out-File -FilePath "$ConfigDir\config.json" -Encoding UTF8
    Write-Success "Configuration created at $ConfigDir\config.json"
}

function Show-ClaudeDesktopInstructions {
    if ($NoClaudeDesktop) {
        return
    }
    
    Write-Step "Claude Desktop Integration Instructions"
    
    # Get nano-agent path
    $nanoAgentPath = Get-Command nano-agent -ErrorAction SilentlyContinue
    if ($nanoAgentPath) {
        $nanoAgentCmd = "nano-agent"
    } else {
        $toolDir = uv tool dir
        $nanoAgentCmd = "$toolDir\Scripts\nano-agent.exe"
    }
    
    # Create sample config for reference
    $configDir = "$env:USERPROFILE\.nano-cli"
    New-Item -Path $configDir -ItemType Directory -Force | Out-Null
    
    $sampleConfig = @{
        mcpServers = @{
            "nano-agent" = @{
                command = $nanoAgentCmd
                args = @()
                env = @{
                    NANO_AGENT_MCP_MODE = "true"
                }
            }
        }
    } | ConvertTo-Json -Depth 4
    
    $sampleConfig | Out-File -FilePath "$configDir\claude_desktop_sample.json" -Encoding UTF8
    Write-Success "Sample configuration saved to: $configDir\claude_desktop_sample.json"
    
    Write-Host ""
    Write-Host "📋 Manual Claude Desktop Setup Instructions" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To use nano-agent with Claude Desktop, you need to manually add it to your configuration:"
    Write-Host ""
    Write-Host "1. Locate your Claude Desktop configuration file:" -ForegroundColor Cyan
    Write-Host "   $env:APPDATA\Claude\claude_desktop_config.json"
    Write-Host ""
    Write-Host "2. Add the nano-agent server configuration:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "   If the file doesn't exist, create it with this content:" -ForegroundColor White
    Write-Host $sampleConfig -ForegroundColor Blue
    Write-Host ""
    Write-Host "   If the file exists, add the 'nano-agent' section to the existing 'mcpServers' object." -ForegroundColor White
    Write-Host ""
    Write-Host "   ⚠️  IMPORTANT: Be careful not to overwrite existing server configurations!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "3. Restart Claude Desktop" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "4. Verify the connection:" -ForegroundColor Cyan
    Write-Host "   • Look for the 🔌 icon in Claude Desktop"
    Write-Host "   • Nano-agent tools should appear in the MCP section"
    Write-Host ""
    Write-Host "Reference configuration saved at:" -ForegroundColor Green
    Write-Host "   $configDir\claude_desktop_sample.json"
    Write-Host ""
}

function Show-Completion {
    Clear-Host
    Write-Host ""
    Write-Host "🎉 Installation Complete!" -ForegroundColor Green -BackgroundColor Black
    Write-Host ""
    Write-Host "Nano Agent MCP Server has been successfully installed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📍 Installation Locations:" -ForegroundColor White
    Write-Host "• Program files: $InstallDir\nano-agent"
    Write-Host "• Configuration: $ConfigDir"
    Write-Host "• Command: nano-agent"
    Write-Host ""
    Write-Host "🚀 What's Next:" -ForegroundColor White
    Write-Host ""
    Write-Host "For Claude Desktop users:"
    Write-Host "  • Restart Claude Desktop"
    Write-Host "  • Look for the 🔌 icon to access nano-agent"
    Write-Host "  • Try: 'Use nano-agent to analyze this project'"
    Write-Host ""
    Write-Host "For CLI users:"
    Write-Host "  • Run: nano-cli run 'your prompt here'"
    Write-Host "  • Example: nano-cli run 'Create a Python script'"
    Write-Host ""
    Write-Host "📝 Configure API Keys:"
    Write-Host "  Edit: $InstallDir\nano-agent\apps\nano_agent_mcp_server\.env"
    Write-Host ""
    Write-Host "Happy coding! 🤖✨" -ForegroundColor Green
    Write-Host ""
}

# Main installation flow
function Main {
    if (!$Quick) {
        $continue = Read-Host "Continue with installation? (y/N)"
        if ($continue -ne 'y' -and $continue -ne 'Y') {
            Write-Host "Installation cancelled."
            exit 0
        }
    }
    
    if (!(Test-Requirements)) {
        exit 1
    }
    
    Install-UV
    Install-NanoAgent
    Setup-Configuration
    Show-ClaudeDesktopInstructions
    Show-Completion
}

# Handle Ctrl+C gracefully
try {
    Main
} catch {
    Write-Error "Installation interrupted: $($_.Exception.Message)"
    exit 1
}