// 🚀 Secure Local SQL Chatbot - Interactive Frontend
class SecureChatbot {
    constructor() {
        this.queryCount = 0;
        this.isLoading = false;
        this.lastSqlQuery = '';
        
        this.initializeElements();
        this.bindEvents();
        this.checkSystemHealth();
        
        console.log('🔐 Secure Local SQL Chatbot initialized');
    }
    
    initializeElements() {
        // Core elements
        this.chatForm = document.getElementById('chatForm');
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.chatMessages = document.getElementById('chatMessages');
        this.connectionStatus = document.getElementById('connectionStatus');
        
        // Sidebar elements
        this.queryCountElement = document.getElementById('queryCount');
        this.sqlQueryCard = document.getElementById('sqlQueryCard');
        this.lastSqlQueryElement = document.getElementById('lastSqlQuery');
        
        // Modal elements
        this.schemaBtn = document.getElementById('schemaBtn');
        this.schemaModal = new bootstrap.Modal(document.getElementById('schemaModal'));
        this.schemaContent = document.getElementById('schemaContent');
    }
    
    bindEvents() {
        // Chat form submission
        this.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSendMessage();
        });
        
        // Schema button click
        this.schemaBtn.addEventListener('click', () => {
            this.loadDatabaseSchema();
        });
        
        // Enter key handling
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.handleSendMessage();
            }
        });
        
        // Auto-focus message input
        this.messageInput.focus();
    }
    
    async checkSystemHealth() {
        try {
            const response = await fetch('/health');
            const data = await response.json();
            
            if (data.status === 'healthy') {
                this.updateConnectionStatus(true, data.groq_connected);
            } else {
                this.updateConnectionStatus(false, false);
            }
        } catch (error) {
            console.error('Health check failed:', error);
            this.updateConnectionStatus(false, false);
        }
    }
    
    updateConnectionStatus(isHealthy, groqConnected) {
        if (isHealthy && groqConnected) {
            this.connectionStatus.innerHTML = '<i class="fas fa-check-circle me-1"></i> Connected';
            this.connectionStatus.className = 'badge bg-success';
        } else if (isHealthy && !groqConnected) {
            this.connectionStatus.innerHTML = '<i class="fas fa-exclamation-triangle me-1"></i> Limited';
            this.connectionStatus.className = 'badge bg-warning';
        } else {
            this.connectionStatus.innerHTML = '<i class="fas fa-times-circle me-1"></i> Offline';
            this.connectionStatus.className = 'badge bg-danger';
        }
    }
    
    async handleSendMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message || this.isLoading) {
            return;
        }
        
        // Clear input and show user message
        this.messageInput.value = '';
        this.addUserMessage(message);
        this.showTypingIndicator();
        
        // Set loading state
        this.setLoadingState(true);
        
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            this.hideTypingIndicator();
            
            if (data.success) {
                this.addBotMessage(data, 'success');
                this.updateSqlDisplay(data.generated_sql);
                this.updateQueryCount();
            } else {
                this.addBotMessage(data, 'error');
                if (data.generated_sql) {
                    this.updateSqlDisplay(data.generated_sql);
                }
            }
            
        } catch (error) {
            console.error('Chat error:', error);
            this.hideTypingIndicator();
            this.addBotMessage({
                error: '🚨 Connection error. Please check your network and try again.',
                message: 'System Error'
            }, 'error');
        } finally {
            this.setLoadingState(false);
        }
    }
    
    addUserMessage(message) {
        const messageWrapper = document.createElement('div');
        messageWrapper.className = 'message-wrapper mb-3';
        
        messageWrapper.innerHTML = `
            <div class="message user-message">
                <div class="message-avatar">
                    <i class="fas fa-user"></i>
                </div>
                <div class="message-content">
                    <div class="message-bubble">
                        <p class="mb-0">${this.escapeHtml(message)}</p>
                    </div>
                    <div class="message-time">
                        <small class="text-muted">
                            <i class="fas fa-clock me-1"></i>
                            ${new Date().toLocaleTimeString()}
                        </small>
                    </div>
                </div>
            </div>
        `;
        
        this.chatMessages.appendChild(messageWrapper);
        this.scrollToBottom();
    }
    
    addBotMessage(data, type) {
        const messageWrapper = document.createElement('div');
        messageWrapper.className = 'message-wrapper mb-3';
        
        let content = '';
        let bubbleClass = 'message-bubble';
        
        if (type === 'success') {
            bubbleClass += ' success-message';
            content = `
                <div class="d-flex align-items-center mb-2">
                    <i class="fas fa-check-circle text-success me-2"></i>
                    <strong>${data.message}</strong>
                </div>
                ${data.results && data.results.length > 0 ? this.formatResults(data.results) : '<p class="mb-0 text-muted">No results found.</p>'}
            `;
        } else {
            bubbleClass += ' error-message';
            content = `
                <div class="d-flex align-items-center mb-2">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    <strong>Query Error</strong>
                </div>
                <p class="mb-0">${this.escapeHtml(data.error)}</p>
                ${data.suggestion ? `<small class="text-muted mt-2 d-block"><i class="fas fa-lightbulb me-1"></i>${data.suggestion}</small>` : ''}
            `;
        }
        
        messageWrapper.innerHTML = `
            <div class="message bot-message">
                <div class="message-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <div class="${bubbleClass}">
                        ${content}
                    </div>
                    <div class="message-time">
                        <small class="text-muted">
                            <i class="fas fa-clock me-1"></i>
                            ${new Date().toLocaleTimeString()}
                            ${data.timestamp ? `• ${data.result_count || 0} result(s)` : ''}
                        </small>
                    </div>
                </div>
            </div>
        `;
        
        this.chatMessages.appendChild(messageWrapper);
        this.scrollToBottom();
    }
    
    formatResults(results) {
        if (!results || results.length === 0) {
            return '<p class="text-muted mb-0">No results found.</p>';
        }
        
        const columns = Object.keys(results[0]);
        const maxRows = 10; // Limit display to prevent overwhelming UI
        const displayResults = results.slice(0, maxRows);
        const hasMore = results.length > maxRows;
        
        let tableHtml = `
            <div class="results-table-container">
                <table class="table table-sm results-table mb-0">
                    <thead>
                        <tr>
                            ${columns.map(col => `<th>${this.formatColumnName(col)}</th>`).join('')}
                        </tr>
                    </thead>
                    <tbody>
        `;
        
        displayResults.forEach(row => {
            tableHtml += '<tr>';
            columns.forEach(col => {
                let value = row[col];
                if (value === null || value === undefined) {
                    value = '<span class="text-muted">null</span>';
                } else if (typeof value === 'number') {
                    value = this.formatNumber(value);
                } else {
                    value = this.escapeHtml(String(value));
                }
                tableHtml += `<td>${value}</td>`;
            });
            tableHtml += '</tr>';
        });
        
        tableHtml += `
                    </tbody>
                </table>
            </div>
        `;
        
        if (hasMore) {
            tableHtml += `
                <div class="mt-2">
                    <small class="text-muted">
                        <i class="fas fa-info-circle me-1"></i>
                        Showing first ${maxRows} of ${results.length} results
                    </small>
                </div>
            `;
        }
        
        return tableHtml;
    }
    
    formatColumnName(columnName) {
        return columnName
            .split('_')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }
    
    formatNumber(num) {
        if (num % 1 === 0) {
            return num.toLocaleString();
        } else {
            return parseFloat(num.toFixed(2)).toLocaleString();
        }
    }
    
    showTypingIndicator() {
        const typingWrapper = document.createElement('div');
        typingWrapper.className = 'message-wrapper mb-3 typing-indicator-wrapper';
        typingWrapper.id = 'typingIndicator';
        
        typingWrapper.innerHTML = `
            <div class="message bot-message">
                <div class="message-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <div class="message-bubble">
                        <div class="typing-indicator">
                            <i class="fas fa-brain me-2"></i>
                            Processing query
                            <div class="typing-dots ms-2">
                                <span></span>
                                <span></span>
                                <span></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        this.chatMessages.appendChild(typingWrapper);
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    setLoadingState(loading) {
        this.isLoading = loading;
        
        if (loading) {
            this.sendBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            this.sendBtn.disabled = true;
            this.messageInput.disabled = true;
        } else {
            this.sendBtn.innerHTML = '<i class="fas fa-paper-plane"></i>';
            this.sendBtn.disabled = false;
            this.messageInput.disabled = false;
            this.messageInput.focus();
        }
    }
    
    updateSqlDisplay(sqlQuery) {
        if (sqlQuery) {
            this.lastSqlQuery = sqlQuery;
            this.lastSqlQueryElement.textContent = sqlQuery;
            this.sqlQueryCard.style.display = 'block';
            
            // Re-highlight syntax
            if (typeof Prism !== 'undefined') {
                Prism.highlightElement(this.lastSqlQueryElement);
            }
        }
    }
    
    updateQueryCount() {
        this.queryCount++;
        if (this.queryCountElement) {
            this.queryCountElement.textContent = this.queryCount;
        }
    }
    
    async loadDatabaseSchema() {
        this.schemaContent.innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading schema...</span>
                </div>
                <p class="mt-2">Loading database schema...</p>
            </div>
        `;
        
        this.schemaModal.show();
        
        try {
            const response = await fetch('/schema');
            const data = await response.json();
            
            if (data.success) {
                this.displaySchema(data.schema);
            } else {
                this.schemaContent.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="fas fa-exclamation-triangle me-2"></i>
                        Error loading schema: ${data.error}
                    </div>
                `;
            }
        } catch (error) {
            this.schemaContent.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Connection error: ${error.message}
                </div>
            `;
        }
    }
    
    displaySchema(schema) {
        let schemaHtml = '';
        
        Object.entries(schema).forEach(([tableName, tableInfo]) => {
            schemaHtml += `
                <div class="card mb-3">
                    <div class="card-header bg-primary text-white">
                        <h6 class="mb-0">
                            <i class="fas fa-table me-2"></i>
                            ${tableName.toUpperCase()}
                        </h6>
                    </div>
                    <div class="card-body p-0">
                        <table class="table table-sm schema-table mb-0">
                            <thead>
                                <tr>
                                    <th>Column</th>
                                    <th>Type</th>
                                    <th>Constraints</th>
                                </tr>
                            </thead>
                            <tbody>
            `;
            
            tableInfo.columns.forEach(column => {
                const constraints = [];
                if (column.primary_key) constraints.push('<span class="badge bg-warning text-dark">PK</span>');
                if (column.not_null) constraints.push('<span class="badge bg-info">NOT NULL</span>');
                
                schemaHtml += `
                    <tr>
                        <td><strong>${column.name}</strong></td>
                        <td><code>${column.type}</code></td>
                        <td>${constraints.join(' ')}</td>
                    </tr>
                `;
            });
            
            schemaHtml += `
                            </tbody>
                        </table>
            `;
            
            // Add foreign key information
            if (tableInfo.foreign_keys && tableInfo.foreign_keys.length > 0) {
                schemaHtml += `
                    <div class="border-top p-3 bg-light">
                        <h6 class="mb-2">
                            <i class="fas fa-link me-1"></i>
                            Foreign Keys
                        </h6>
                `;
                
                tableInfo.foreign_keys.forEach(fk => {
                    schemaHtml += `
                        <div class="d-flex align-items-center mb-1">
                            <code class="me-2">${fk.column}</code>
                            <i class="fas fa-arrow-right mx-2 text-muted"></i>
                            <code>${fk.references_table}.${fk.references_column}</code>
                        </div>
                    `;
                });
                
                schemaHtml += '</div>';
            }
            
            schemaHtml += `
                    </div>
                </div>
            `;
        });
        
        this.schemaContent.innerHTML = schemaHtml;
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, (m) => map[m]);
    }
}

// Global Functions
function sendExampleQuery(element) {
    const query = element.textContent.trim();
    const messageInput = document.getElementById('messageInput');
    
    if (messageInput && query) {
        messageInput.value = query;
        messageInput.focus();
        
        // Add visual feedback
        element.style.transform = 'scale(0.95)';
        setTimeout(() => {
            element.style.transform = '';
        }, 150);
    }
}

function copySqlQuery() {
    const sqlQuery = document.getElementById('lastSqlQuery').textContent;
    
    if (navigator.clipboard) {
        navigator.clipboard.writeText(sqlQuery).then(() => {
            // Show success feedback
            const copyBtn = event.target;
            const originalText = copyBtn.innerHTML;
            copyBtn.innerHTML = '<i class="fas fa-check me-1"></i>Copied!';
            copyBtn.className = 'btn btn-sm btn-success mt-2';
            
            setTimeout(() => {
                copyBtn.innerHTML = originalText;
                copyBtn.className = 'btn btn-sm btn-outline-primary mt-2';
            }, 2000);
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = sqlQuery;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        
        alert('SQL query copied to clipboard!');
    }
}

// Initialize the chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.chatbot = new SecureChatbot();
});

// Handle page visibility for connection status
document.addEventListener('visibilitychange', () => {
    if (!document.hidden && window.chatbot) {
        window.chatbot.checkSystemHealth();
    }
});
