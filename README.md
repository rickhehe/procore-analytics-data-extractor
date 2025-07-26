# Procore Analytics Data Extractor

A Python application for extracting data from Procore Analytics using Delta Sharing.

## Prerequisites

You must have Procore Analytics enabled.

<https://en-au.support.procore.com/products/online/user-guide/company-level/analytics/tutorials/getting-started-with-analytics#chapt2>

## Setup Instructions

### Quick Setup (Recommended)

Run the automated setup script:

```powershell
.\setup.ps1
```

This script will:

- Create `.env` file from template
- Create a Delta Sharing profile file from template
- Guide you through the configuration process

**Note**: Dependencies are automatically installed when you run `.\scripts\run.ps1`

### Manual Setup

### 1. Run Setup Script

The setup script will guide you through the configuration:

```powershell
.\setup.ps1
```

### 2. Edit Configuration Files

After running the setup script, edit the generated files:

**Edit your `.share` file** - Update with your actual Delta Sharing credentials:

- `endpoint`: Your Databricks workspace Delta Sharing endpoint
- `bearerToken`: Your Delta Sharing bearer token

### 3. Install Dependencies and Run

```powershell
.\scripts\run.ps1
```

## Security Notes

- **Never commit `.env` files or `.share` files to version control** - they contain sensitive credentials
- The `.gitignore` file is configured to exclude these files automatically
- Example files (`.env.example`, `*.share.example`) are safe to commit as they contain placeholder values

## Getting Your Delta Sharing Credentials

To get your Delta Sharing credentials:

- Contact your IT department
