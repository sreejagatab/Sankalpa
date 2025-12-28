
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import os
from agents.base import BaseAgent

class VsCodeExtensionAgent(BaseAgent):
    """
    Enhanced VS Code extension generator that creates a fully-featured VS Code extension 
    for integrating with Sankalpa agents and workflows.
    """
    
    def run(self, input_data):
        extension_name = input_data.get("name", "sankalpa-extension")
        display_name = input_data.get("display_name", "Sankalpa AI Agents")
        description = input_data.get("description", "Integrate Sankalpa AI agents directly in your editor")
        publisher = input_data.get("publisher", "sankalpa")
        version = input_data.get("version", "0.1.0")
        
        # Create extension directory structure
        os.makedirs(f"vscode-extension/src", exist_ok=True)
        os.makedirs(f"vscode-extension/.vscode", exist_ok=True)
        
        package_json = f"""{{
  "name": "{extension_name}",
  "displayName": "{display_name}",
  "description": "{description}",
  "publisher": "{publisher}",
  "version": "{version}",
  "engines": {{
    "vscode": "^1.60.0"
  }},
  "categories": [
    "Other",
    "Machine Learning",
    "Snippets",
    "Programming Languages"
  ]],
  "activationEvents": [
    "onCommand:sankalpa.run",
    "onCommand:sankalpa.runChain",
    "onCommand:sankalpa.createAgent",
    "onCommand:sankalpa.showMemory",
    "onCommand:sankalpa.openComposer",
    "onView:sankalpaAgents"
  ],
  "main": "./dist/extension.js",
  "contributes": {{
    "commands": [
      {{
        "command": "sankalpa.run",
        "title": "Sankalpa: Run Agent"
      }},
      {{
        "command": "sankalpa.runChain",
        "title": "Sankalpa: Run Agent Chain"
      }},
      {{
        "command": "sankalpa.createAgent",
        "title": "Sankalpa: Create New Agent"
      }},
      {{
        "command": "sankalpa.showMemory",
        "title": "Sankalpa: Show Agent Memory"
      }},
      {{
        "command": "sankalpa.openComposer",
        "title": "Sankalpa: Open Workflow Composer"
      }}
    ],
    "viewsContainers": {{
      "activitybar": [
        {{
          "id": "sankalpa-sidebar",
          "title": "Sankalpa AI",
          "icon": "resources/icon.svg"
        }}
      ]
    }},
    "views": {{
      "sankalpa-sidebar": [
        {{
          "id": "sankalpaAgents",
          "name": "Available Agents"
        }},
        {{
          "id": "sankalpaWorkflows",
          "name": "Workflows"
        }},
        {{
          "id": "sankalpaMemory",
          "name": "Agent Memory"
        }}
      ]
    }},
    "menus": {{
      "editor/context": [
        {{
          "command": "sankalpa.run",
          "group": "sankalpa"
        }}
      ],
      "view/title": [
        {{
          "command": "sankalpa.createAgent",
          "when": "view == sankalpaAgents",
          "group": "navigation"
        }}
      ]
    }},
    "configuration": {{
      "title": "Sankalpa",
      "properties": {{
        "sankalpa.apiEndpoint": {{
          "type": "string",
          "default": "http://localhost:8000",
          "description": "The Sankalpa API endpoint URL"
        }},
        "sankalpa.pythonPath": {{
          "type": "string",
          "default": "python3",
          "description": "Path to Python executable for CLI commands"
        }},
        "sankalpa.cliPath": {{
          "type": "string",
          "default": "cli/cli.py",
          "description": "Path to Sankalpa CLI script"
        }}
      }}
    }}
  }},
  "scripts": {{
    "vscode:prepublish": "npm run package",
    "compile": "webpack",
    "watch": "webpack --watch",
    "package": "webpack --mode production --devtool hidden-source-map",
    "lint": "eslint src --ext ts",
    "test": "jest"
  }},
  "devDependencies": {{
    "@types/glob": "^7.1.4",
    "@types/node": "^16.11.7",
    "@types/vscode": "^1.60.0",
    "@typescript-eslint/eslint-plugin": "^5.30.0",
    "@typescript-eslint/parser": "^5.30.0",
    "eslint": "^8.13.0",
    "ts-loader": "^9.3.1",
    "typescript": "^4.7.4",
    "webpack": "^5.76.0",
    "webpack-cli": "^4.10.0"
  }},
  "dependencies": {{
    "axios": "^0.27.2"
  }}
}}
"""

        tsconfig_json = """{
  "compilerOptions": {
    "module": "commonjs",
    "target": "ES2020",
    "outDir": "dist",
    "lib": ["ES2020"],
    "sourceMap": true,
    "rootDir": "src",
    "strict": true
  },
  "exclude": ["node_modules", ".vscode-test"]
}
"""

        extension_ts = """import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import axios from 'axios';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

interface Agent {
  id: string;
  name: string;
  description: string;
  category: string;
}

interface AgentOutputChannel {
  channel: vscode.OutputChannel;
  showing: boolean;
}

export async function activate(context: vscode.ExtensionContext) {
  console.log('Sankalpa extension is now active');
  
  // Setup API client
  const getApiEndpoint = () => {
    return vscode.workspace.getConfiguration('sankalpa').get('apiEndpoint') as string;
  };

  // Setup output channel for agent results
  const outputChannels: Map<string, AgentOutputChannel> = new Map();
  
  const getAgentOutputChannel = (agentName: string): AgentOutputChannel => {
    if (!outputChannels.has(agentName)) {
      outputChannels.set(agentName, {
        channel: vscode.window.createOutputChannel(`Sankalpa: ${agentName}`),
        showing: false
      });
    }
    return outputChannels.get(agentName)!;
  };
  
  // Agent data provider for the sidebar
  class AgentDataProvider implements vscode.TreeDataProvider<AgentItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<AgentItem | undefined | null | void> = new vscode.EventEmitter<AgentItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<AgentItem | undefined | null | void> = this._onDidChangeTreeData.event;
    
    private _agents: Agent[] = [];
    
    constructor() {
      this.refreshAgents();
    }
    
    async refreshAgents() {
      try {
        const response = await axios.get(`${getApiEndpoint()}/agents`);
        this._agents = response.data;
        this._onDidChangeTreeData.fire();
      } catch (error) {
        console.error('Failed to fetch agents:', error);
        this._agents = [];
        this._onDidChangeTreeData.fire();
      }
    }
    
    getTreeItem(element: AgentItem): vscode.TreeItem {
      return element;
    }
    
    getChildren(element?: AgentItem): Thenable<AgentItem[]> {
      if (element) {
        return Promise.resolve([]);
      }
      
      return Promise.resolve(this._agents.map(agent => new AgentItem(
        agent.name,
        agent.description,
        agent.category,
        vscode.TreeItemCollapsibleState.None,
        {
          command: 'sankalpa.run',
          title: 'Run Agent',
          arguments: [agent.id]
        }
      )));
    }
  }
  
  class AgentItem extends vscode.TreeItem {
    constructor(
      public readonly label: string,
      public readonly description: string,
      public readonly category: string,
      public readonly collapsibleState: vscode.TreeItemCollapsibleState,
      public readonly command?: vscode.Command
    ) {
      super(label, collapsibleState);
      this.tooltip = `${description}\\nCategory: ${category}`;
      this.contextValue = 'agent';
    }
    
    iconPath = {
      light: path.join(__filename, '..', '..', 'resources', 'light', 'agent.svg'),
      dark: path.join(__filename, '..', '..', 'resources', 'dark', 'agent.svg')
    };
  }
  
  const agentDataProvider = new AgentDataProvider();
  vscode.window.registerTreeDataProvider('sankalpaAgents', agentDataProvider);
  
  // Command: Run Agent
  const runAgentCommand = async (agentId?: string) => {
    try {
      if (!agentId) {
        const agents = await axios.get(`${getApiEndpoint()}/agents`);
        const agentNames = agents.data.map((agent: Agent) => ({
          label: agent.name,
          description: agent.description,
          id: agent.id
        }));
        
        const selectedAgent = await vscode.window.showQuickPick(agentNames, {
          placeHolder: 'Select an agent to run'
        });
        
        if (!selectedAgent) {
          return;
        }
        
        agentId = selectedAgent.id;
      }
      
      // Get input from user
      const input = await vscode.window.showInputBox({
        prompt: 'Enter input for the agent',
        placeHolder: 'Agent input'
      });
      
      if (input === undefined) {
        return;
      }
      
      // Get selected text if any
      let selectedText = '';
      const editor = vscode.window.activeTextEditor;
      if (editor) {
        const selection = editor.selection;
        if (!selection.isEmpty) {
          selectedText = editor.document.getText(selection);
        }
      }
      
      // Show progress
      await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: `Running Sankalpa agent: ${agentId}`,
        cancellable: true
      }, async (progress, token) => {
        progress.report({ increment: 0 });
        
        try {
          // Try the API first
          const response = await axios.post(`${getApiEndpoint()}/agents/${agentId}/run`, {
            input: input,
            selected_text: selectedText
          });
          
          progress.report({ increment: 100 });
          
          // Show output
          const outputChannel = getAgentOutputChannel(agentId);
          outputChannel.channel.clear();
          outputChannel.channel.appendLine(`Agent: ${agentId}`);
          outputChannel.channel.appendLine(`Input: ${input}`);
          outputChannel.channel.appendLine('\\nResult:');
          outputChannel.channel.appendLine(JSON.stringify(response.data, null, 2));
          
          if (!outputChannel.showing) {
            outputChannel.channel.show();
            outputChannel.showing = true;
          }
          
          // If there are generated files, offer to open them
          if (response.data.files && Object.keys(response.data.files).length > 0) {
            const openFiles = await vscode.window.showQuickPick(
              ['Yes', 'No'],
              { placeHolder: 'Open generated files?' }
            );
            
            if (openFiles === 'Yes') {
              for (const filePath of Object.keys(response.data.files)) {
                const uri = vscode.Uri.file(path.resolve(filePath));
                const doc = await vscode.workspace.openTextDocument(uri);
                await vscode.window.showTextDocument(doc);
              }
            }
          }
          
        } catch (error) {
          // Fall back to CLI
          try {
            const pythonPath = vscode.workspace.getConfiguration('sankalpa').get('pythonPath') as string;
            const cliPath = vscode.workspace.getConfiguration('sankalpa').get('cliPath') as string;
            
            // Escape the input for CLI
            const escapedInput = input.replace(/"/g, '\\\\"');
            
            const { stdout, stderr } = await execAsync(
              `${pythonPath} ${cliPath} run-agent ${agentId} "${escapedInput}"`
            );
            
            progress.report({ increment: 100 });
            
            // Show output
            const outputChannel = getAgentOutputChannel(agentId);
            outputChannel.channel.clear();
            outputChannel.channel.appendLine(`Agent: ${agentId}`);
            outputChannel.channel.appendLine(`Input: ${input}`);
            outputChannel.channel.appendLine('\\nResult (via CLI):');
            outputChannel.channel.appendLine(stdout);
            
            if (stderr) {
              outputChannel.channel.appendLine('\\nErrors:');
              outputChannel.channel.appendLine(stderr);
            }
            
            if (!outputChannel.showing) {
              outputChannel.channel.show();
              outputChannel.showing = true;
            }
            
          } catch (cliError: any) {
            vscode.window.showErrorMessage(`Failed to run agent via CLI: ${cliError.message}`);
          }
        }
      });
      
    } catch (error: any) {
      vscode.window.showErrorMessage(`Error running agent: ${error.message}`);
    }
  };
  
  // Command: Run Agent Chain
  const runChainCommand = async () => {
    try {
      // Get agents
      const agents = await axios.get(`${getApiEndpoint()}/agents`);
      const agentItems = agents.data.map((agent: Agent) => ({
        label: agent.name,
        description: agent.description,
        id: agent.id
      }));
      
      // Multi-select agents for chain
      const selectedAgents = await vscode.window.showQuickPick(agentItems, {
        placeHolder: 'Select agents for the chain',
        canPickMany: true
      });
      
      if (!selectedAgents || selectedAgents.length === 0) {
        return;
      }
      
      // Get chain input
      const input = await vscode.window.showInputBox({
        prompt: 'Enter input for the agent chain',
        placeHolder: 'Chain input'
      });
      
      if (input === undefined) {
        return;
      }
      
      // Get selected text if any
      let selectedText = '';
      const editor = vscode.window.activeTextEditor;
      if (editor) {
        const selection = editor.selection;
        if (!selection.isEmpty) {
          selectedText = editor.document.getText(selection);
        }
      }
      
      // Show progress
      await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: 'Running Sankalpa agent chain',
        cancellable: true
      }, async (progress, token) => {
        progress.report({ increment: 0 });
        
        try {
          // Try API first
          const agentIds = selectedAgents.map(a => a.id);
          const response = await axios.post(`${getApiEndpoint()}/chains/run`, {
            agents: agentIds,
            input: input,
            selected_text: selectedText
          });
          
          progress.report({ increment: 100 });
          
          // Show output
          const outputChannel = getAgentOutputChannel('Chain');
          outputChannel.channel.clear();
          outputChannel.channel.appendLine(`Chain: ${agentIds.join(' -> ')}`);
          outputChannel.channel.appendLine(`Input: ${input}`);
          outputChannel.channel.appendLine('\\nResult:');
          outputChannel.channel.appendLine(JSON.stringify(response.data, null, 2));
          
          if (!outputChannel.showing) {
            outputChannel.channel.show();
            outputChannel.showing = true;
          }
          
        } catch (error) {
          // Fall back to CLI
          try {
            const pythonPath = vscode.workspace.getConfiguration('sankalpa').get('pythonPath') as string;
            const cliPath = vscode.workspace.getConfiguration('sankalpa').get('cliPath') as string;
            
            // Escape the input for CLI
            const escapedInput = input.replace(/"/g, '\\\\"');
            const agentIds = selectedAgents.map(a => a.id).join(' ');
            
            const { stdout, stderr } = await execAsync(
              `${pythonPath} ${cliPath} run-chain ${agentIds} "${escapedInput}"`
            );
            
            progress.report({ increment: 100 });
            
            // Show output
            const outputChannel = getAgentOutputChannel('Chain');
            outputChannel.channel.clear();
            outputChannel.channel.appendLine(`Chain: ${agentIds}`);
            outputChannel.channel.appendLine(`Input: ${input}`);
            outputChannel.channel.appendLine('\\nResult (via CLI):');
            outputChannel.channel.appendLine(stdout);
            
            if (stderr) {
              outputChannel.channel.appendLine('\\nErrors:');
              outputChannel.channel.appendLine(stderr);
            }
            
            if (!outputChannel.showing) {
              outputChannel.channel.show();
              outputChannel.showing = true;
            }
            
          } catch (cliError: any) {
            vscode.window.showErrorMessage(`Failed to run chain via CLI: ${cliError.message}`);
          }
        }
      });
      
    } catch (error: any) {
      vscode.window.showErrorMessage(`Error running agent chain: ${error.message}`);
    }
  };
  
  // Command: Create New Agent
  const createAgentCommand = async () => {
    try {
      // Get agent details from user
      const name = await vscode.window.showInputBox({
        prompt: 'Enter agent name (lowercase, underscore separated)',
        placeHolder: 'custom_agent',
        validateInput: (value) => {
          if (!/^[a-z][a-z0-9_]*$/.test(value)) {
            return 'Agent name must be lowercase, start with a letter, and contain only letters, numbers, and underscores';
          }
          return null;
        }
      });
      
      if (!name) {
        return;
      }
      
      const description = await vscode.window.showInputBox({
        prompt: 'Enter agent description',
        placeHolder: 'A custom agent that...'
      });
      
      if (!description) {
        return;
      }
      
      const category = await vscode.window.showQuickPick(
        ['custom', 'utility', 'builder', 'testing', 'deployment', 'enhanced', 'marketing'],
        { placeHolder: 'Select agent category' }
      );
      
      if (!category) {
        return;
      }
      
      // Show progress
      await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: 'Creating new agent',
        cancellable: true
      }, async (progress, token) => {
        progress.report({ increment: 0 });
        
        try {
          // Call the self-replicator agent
          const response = await axios.post(`${getApiEndpoint()}/agents/self_replicator/run`, {
            name: name,
            description: description,
            category: category,
            logic: "# TODO: Implement agent logic\\n        result = {\\n            'message': 'Hello from custom agent',\\n            'status': 'success'\\n        }\\n"
          });
          
          progress.report({ increment: 100 });
          
          vscode.window.showInformationMessage(`Agent '${name}' created successfully`);
          
          // Refresh the agent list
          agentDataProvider.refreshAgents();
          
          // Offer to open the agent file
          if (response.data.files) {
            const agentFile = Object.keys(response.data.files).find(f => f.includes(name));
            if (agentFile) {
              const openFile = await vscode.window.showQuickPick(
                ['Yes', 'No'],
                { placeHolder: 'Open generated agent file?' }
              );
              
              if (openFile === 'Yes') {
                const uri = vscode.Uri.file(path.resolve(agentFile));
                const doc = await vscode.workspace.openTextDocument(uri);
                await vscode.window.showTextDocument(doc);
              }
            }
          }
          
        } catch (error: any) {
          vscode.window.showErrorMessage(`Failed to create agent: ${error.message}`);
        }
      });
      
    } catch (error: any) {
      vscode.window.showErrorMessage(`Error creating agent: ${error.message}`);
    }
  };
  
  // Command: Show Agent Memory
  const showMemoryCommand = async () => {
    try {
      const response = await axios.get(`${getApiEndpoint()}/memory`);
      
      const outputChannel = getAgentOutputChannel('Memory');
      outputChannel.channel.clear();
      outputChannel.channel.appendLine('Agent Memory:');
      outputChannel.channel.appendLine(JSON.stringify(response.data, null, 2));
      
      if (!outputChannel.showing) {
        outputChannel.channel.show();
        outputChannel.showing = true;
      }
      
    } catch (error: any) {
      vscode.window.showErrorMessage(`Error fetching memory: ${error.message}`);
    }
  };
  
  // Command: Open Workflow Composer
  const openComposerCommand = async () => {
    try {
      const apiEndpoint = getApiEndpoint();
      const composerUrl = `${apiEndpoint}/composer`;
      vscode.env.openExternal(vscode.Uri.parse(composerUrl));
    } catch (error: any) {
      vscode.window.showErrorMessage(`Error opening composer: ${error.message}`);
    }
  };
  
  // Register all commands
  context.subscriptions.push(
    vscode.commands.registerCommand('sankalpa.run', runAgentCommand),
    vscode.commands.registerCommand('sankalpa.runChain', runChainCommand),
    vscode.commands.registerCommand('sankalpa.createAgent', createAgentCommand),
    vscode.commands.registerCommand('sankalpa.showMemory', showMemoryCommand),
    vscode.commands.registerCommand('sankalpa.openComposer', openComposerCommand),
    
    // Refresh command for the tree view
    vscode.commands.registerCommand('sankalpa.refreshAgents', () => {
      agentDataProvider.refreshAgents();
    })
  );
  
  // Status bar item
  const statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
  statusBarItem.text = "$(rocket) Sankalpa";
  statusBarItem.tooltip = "Open Sankalpa Commands";
  statusBarItem.command = "sankalpa.run";
  statusBarItem.show();
  context.subscriptions.push(statusBarItem);
  
  // Context for when we're editing Python files
  vscode.window.onDidChangeActiveTextEditor(editor => {
    if (editor && editor.document.languageId === 'python') {
      statusBarItem.show();
    } else {
      statusBarItem.hide();
    }
  });
  
  // Show welcome info
  vscode.window.showInformationMessage('Sankalpa AI extension activated. Run agents from the sidebar or command palette.');
}

export function deactivate() {
  // Clean up resources if needed
}
"""

        launch_json = """{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Launch Extension",
      "type": "extensionHost",
      "request": "launch",
      "args": ["--extensionDevelopmentPath=${workspaceFolder}"],
      "outFiles": ["${workspaceFolder}/dist/**/*.js"],
      "preLaunchTask": "${defaultBuildTask}"
    }
  ]
}"""

        tasks_json = """{
  "version": "2.0.0",
  "tasks": [
    {
      "type": "npm",
      "script": "watch",
      "problemMatcher": ["$ts-webpack-watch"],
      "isBackground": true,
      "presentation": {
        "reveal": "never"
      },
      "group": {
        "kind": "build",
        "isDefault": true
      }
    }
  ]
}"""

        webpack_config = """const path = require('path');

module.exports = {
  entry: './src/extension.ts',
  target: 'node',
  mode: 'development',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'extension.js',
    libraryTarget: 'commonjs2'
  },
  externals: {
    vscode: 'commonjs vscode'
  },
  resolve: {
    extensions: ['.ts', '.js']
  },
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: 'ts-loader'
      }
    ]
  }
};"""

        # Create SVG icons
        icon_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"></circle>
  <path d="M8 14s1.5 2 4 2 4-2 4-2"></path>
  <line x1="9" y1="9" x2="9.01" y2="9"></line>
  <line x1="15" y1="9" x2="15.01" y2="9"></line>
</svg>"""

        readme_md = f"""# {display_name}

{description}

## Features

- Run Sankalpa AI agents directly from VS Code
- Chain multiple agents together for complex tasks
- Create new agents with a simple wizard
- View agent memory and execution history
- Open the visual workflow composer

## Commands

- `Sankalpa: Run Agent` - Run a single agent
- `Sankalpa: Run Agent Chain` - Run multiple agents in sequence
- `Sankalpa: Create New Agent` - Generate a new custom agent
- `Sankalpa: Show Agent Memory` - View the current memory state
- `Sankalpa: Open Workflow Composer` - Open the visual workflow editor

## Requirements

- Sankalpa backend service running
- Node.js and npm for extension development

## Extension Settings

This extension contributes the following settings:

* `sankalpa.apiEndpoint`: The Sankalpa API endpoint URL (default: http://localhost:8000)
* `sankalpa.pythonPath`: Path to Python executable for CLI commands (default: python3)
* `sankalpa.cliPath`: Path to Sankalpa CLI script (default: cli/cli.py)

## Getting Started

1. Start the Sankalpa backend server
2. Install the extension
3. Configure the API endpoint in settings if needed
4. Use the Sankalpa sidebar or command palette to run agents

## Developer Notes

To build and run the extension locally:

```bash
cd vscode-extension
npm install
npm run watch
```

Then press F5 to start debugging.
"""

        # Create GitHub workflow for publishing
        github_workflow = """name: Deploy Extension

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '16'
      - run: npm ci
      - run: npm run package
      - name: Publish to VS Code Marketplace
        run: npx vsce publish -p ${{ secrets.VSCE_PAT }}
"""

        # Create the README file for VS Code Marketplace
        
        # Structure all files
        files = {
            f"vscode-extension/package.json": package_json,
            f"vscode-extension/tsconfig.json": tsconfig_json,
            f"vscode-extension/src/extension.ts": extension_ts,
            f"vscode-extension/.vscode/launch.json": launch_json,
            f"vscode-extension/.vscode/tasks.json": tasks_json,
            f"vscode-extension/webpack.config.js": webpack_config,
            f"vscode-extension/resources/icon.svg": icon_svg,
            f"vscode-extension/resources/light/agent.svg": icon_svg,
            f"vscode-extension/resources/dark/agent.svg": icon_svg,
            f"vscode-extension/README.md": readme_md,
            f"vscode-extension/.github/workflows/deploy.yml": github_workflow,
        }
        
        # Installation instructions
        install_instructions = f"""
# VS Code Extension Setup

Extension created with name: {extension_name}

## Development Setup

1. Navigate to the extension directory:
   ```
   cd vscode-extension
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Compile the extension:
   ```
   npm run compile
   ```

4. Package the extension:
   ```
   npm run package
   ```

5. Install the extension locally:
   ```
   code --install-extension {extension_name}-{version}.vsix
   ```

## Key Features

- Sidebar with all available agents
- Run agents with input and selected text
- Run agent chains for complex tasks
- Create new agents from templates
- View memory and execution history
- Open the visual workflow composer

## Configuration

Configure the extension in VS Code settings:
- API endpoint URL
- Python path for CLI fallback
- CLI script path
"""
        
        return {
            "message": "Enhanced VS Code extension generated with full TypeScript implementation, UI components, and publishing workflow.",
            "files": files,
            "instructions": install_instructions
        }
