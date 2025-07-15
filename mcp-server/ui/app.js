// MCP Server UI - Simple and Functional
let serverTools = {};

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('UI loaded, initializing...');
    checkServerStatus();
    loadAvailableTools();
});

// Check server status
async function checkServerStatus() {
    try {
        console.log('Checking server status...');
        const response = await fetch('/health');
        const data = await response.json();
        
        console.log('Server status:', data);
        
        // Update status
        const statusElement = document.getElementById('status');
        if (data.status === 'healthy') {
            statusElement.textContent = 'Online';
            statusElement.className = 'text-green-600 font-medium';
        } else {
            statusElement.textContent = 'Offline';
            statusElement.className = 'text-red-600 font-medium';
        }
        
        // Update server info
        let infoText = '';
        infoText += 'Status: ' + data.status + '\n';
        infoText += 'Version: ' + (data.version || 'Unknown') + '\n';
        infoText += 'Timestamp: ' + new Date(data.timestamp).toLocaleString() + '\n';
        infoText += 'Tools Available: ' + Object.keys(data.tools || {}).length + '\n';
        
        if (data.tools) {
            infoText += '\nTools:\n';
            for (const [toolName, toolStatus] of Object.entries(data.tools)) {
                infoText += '  - ' + toolName + ': ' + toolStatus + '\n';
            }
        }
        
        if (data.api_checks) {
            infoText += '\nAPI Status:\n';
            for (const [api, status] of Object.entries(data.api_checks)) {
                infoText += '  - ' + api + ': ' + status + '\n';
            }
        }
        
        document.getElementById('serverInfo').innerHTML = '<pre>' + infoText + '</pre>';
        
    } catch (error) {
        console.error('Error checking server status:', error);
        document.getElementById('status').textContent = 'Error: ' + error.message;
        document.getElementById('status').className = 'text-red-600 font-medium';
        document.getElementById('serverInfo').innerHTML = '<pre>Error loading server info: ' + error.message + '</pre>';
    }
}

// Load available tools
async function loadAvailableTools() {
    try {
        console.log('Loading available tools...');
        const response = await fetch('/capabilities');
        const data = await response.json();
        
        console.log('Capabilities:', data);
        
        serverTools = data.tools || {};
        
        // Update tools list display
        const toolsList = document.getElementById('toolsList');
        let html = '';
        
        if (Object.keys(serverTools).length === 0) {
            html = '<div class="text-center py-4 text-gray-500 text-sm">No tools available</div>';
        } else {
            for (const [toolName, toolInfo] of Object.entries(serverTools)) {
                html += '<div class="p-3 bg-white rounded-lg border border-gray-200">';
                html += '<h3 class="font-bold text-sm mb-1">' + toolName + '</h3>';
                html += '<p class="text-gray-600 text-xs mb-2">' + (toolInfo.description || 'No description available') + '</p>';
                
                if (toolInfo.parameters) {
                    html += '<div class="text-xs text-gray-500">';
                    html += '<strong>Params:</strong> ';
                    html += Object.keys(toolInfo.parameters).join(', ');
                    html += '</div>';
                }
                
                html += '</div>';
            }
        }
        
        toolsList.innerHTML = html;
        
        // Update tool selector dropdown
        const toolSelect = document.getElementById('toolSelect');
        toolSelect.innerHTML = '<option value="">Select a tool...</option>';
        
        for (const toolName of Object.keys(serverTools)) {
            const option = document.createElement('option');
            option.value = toolName;
            option.textContent = toolName;
            toolSelect.appendChild(option);
        }
        
        // Add change event listener to show parameter examples
        toolSelect.addEventListener('change', showParameterExamples);
        
    } catch (error) {
        console.error('Error loading tools:', error);
        document.getElementById('toolsList').innerHTML = '<div class="text-center py-4 text-red-500">Error loading tools: ' + error.message + '</div>';
    }
}

// Show parameter examples for selected tool
function showParameterExamples() {
    const toolName = document.getElementById('toolSelect').value;
    const examplesDiv = document.getElementById('parameterExamples');
    const examplesList = document.getElementById('examplesList');
    const paramsTextarea = document.getElementById('toolParams');
    
    if (!toolName || !serverTools[toolName]) {
        examplesDiv.classList.add('hidden');
        paramsTextarea.placeholder = 'Select a tool to see parameter examples';
        return;
    }
    
    const toolInfo = serverTools[toolName];
    
    // Define parameter examples for each tool
    const parameterExamples = {
        'file_reader': [
            '{"path": "README.md"}',
            '{"path": "./config.json"}',
            '{"path": "/home/user/document.txt"}'
        ],
        'web_search': [
            '{"query": "OpenAI GPT-4"}',
            '{"query": "Python tutorials", "count": 5}',
            '{"query": "machine learning news"}'
        ],
        'wikipedia': [
            '{"query": "Artificial Intelligence"}',
            '{"query": "Python programming language"}',
            '{"query": "Machine Learning"}'
        ],
        'llm': [
            '{"prompt": "Explain quantum computing", "max_tokens": 100}',
            '{"prompt": "Write a Python function to sort a list"}',
            '{"prompt": "What is the capital of France?"}'
        ],
        'prompt_formatter': [
            '{"template": "system", "variables": {"role": "assistant"}}',
            '{"template": "user_query", "variables": {"query": "Hello world"}}'
        ]
    };
    
    const examples = parameterExamples[toolName] || ['{"query": "example"}'];
    
    let html = '';
    examples.forEach((example, index) => {
        html += '<button data-example="' + example.replace(/"/g, '&quot;') + '" ';
        html += 'class="example-btn text-xs bg-blue-100 hover:bg-blue-200 px-2 py-1 rounded text-blue-800 mr-1 mb-1">Example ' + (index + 1) + '</button>';
    });
    
    examplesList.innerHTML = html;
    
    // Add event listeners to example buttons
    const buttons = examplesList.querySelectorAll('.example-btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const example = this.getAttribute('data-example');
            setExample(example);
        });
    });
    
    examplesDiv.classList.remove('hidden');
    paramsTextarea.placeholder = 'Click an example above or enter custom JSON parameters';
}

// Set example in textarea
function setExample(example) {
    document.getElementById('toolParams').value = example;
}

// Test a tool
async function testTool() {
    const toolName = document.getElementById('toolSelect').value;
    const paramsText = document.getElementById('toolParams').value.trim();
    
    console.log('Testing tool:', toolName, 'with params:', paramsText);
    
    if (!toolName) {
        alert('Please select a tool to test');
        return;
    }
    
    // Parse parameters
    let parameters = {};
    if (paramsText) {
        try {
            parameters = JSON.parse(paramsText);
        } catch (error) {
            alert('Invalid JSON parameters: ' + error.message);
            return;
        }
    }
    
    // Show loading state
    const resultDiv = document.getElementById('result');
    const resultContent = document.getElementById('resultContent');
    
    resultDiv.classList.remove('hidden');
    resultContent.textContent = 'Testing tool "' + toolName + '"...\n\nRequest:\n' + JSON.stringify({
        tool: toolName,
        parameters: parameters
    }, null, 2);
    
    try {
        const response = await fetch('/mcp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                tool: toolName,
                parameters: parameters
            })
        });
        
        const result = await response.json();
        
        console.log('Tool result:', result);
        
        // Display result
        let resultText = 'Tool: ' + toolName + '\n';
        resultText += 'Status: ' + (response.ok ? 'Success' : 'Error') + '\n';
        resultText += 'Response:\n';
        resultText += JSON.stringify(result, null, 2);
        
        resultContent.textContent = resultText;
        
    } catch (error) {
        console.error('Error testing tool:', error);
        resultContent.textContent = 'Error testing tool: ' + error.message;
    }
}

// Refresh data
function refreshData() {
    console.log('Refreshing data...');
    checkServerStatus();
    loadAvailableTools();
}

// Add refresh button functionality (if needed)
window.refreshData = refreshData;
